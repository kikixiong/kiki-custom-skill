#!/usr/bin/env python3
"""Install Kiki's personal skills for Codex and/or Claude Code using stdlib only.

This copies files and renders local paths. It does not run skill code, install
dependencies/plugins, log into services, connect to other machines or run tests.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import re
import shutil
import sys
import tempfile
import uuid

REPO = Path(__file__).resolve().parent
MANIFEST = json.loads((REPO / 'manifest.json').read_text(encoding='utf-8'))
TOKEN_NAMES = set(MANIFEST['runtime_tokens'])


def present(path):
    return path.exists() or path.is_symlink()


def remove_created(path):
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def copy_rendered(source, target, replacements, client, skill_names):
    shutil.copytree(source, target, symlinks=False)
    for path in target.rglob('*'):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        original = text
        for token, value in replacements.items():
            # Preserve valid JSON if a local path contains a JSON-special character.
            rendered = json.dumps(value, ensure_ascii=False)[1:-1] if path.suffix == '.json' else value
            text = text.replace(token, rendered)
        if client == 'claude' and path.suffix == '.md':
            text = re.sub(r'\$([a-z][a-z0-9-]+)\b', lambda m: '/' + m[1] if m[1] in skill_names else m[0], text)
        if text != original:
            path.write_text(text, encoding='utf-8')


def install_client(client, agent_home, selected, profile, dry_run):
    skills_root = agent_home / 'skills'
    support_root = agent_home / 'skill-support' / 'kiki-custom-skill'
    plan = {
        'client': client,
        'agent_home': str(agent_home),
        'skills_directory': str(skills_root),
        'support_directory': str(support_root),
        'profile': profile['name'],
        'skill_count': len(selected),
        'conflicts_to_backup': [name for name in selected if present(skills_root / name)],
        'reference_plugins_and_system_skills_installed': False,
    }
    if dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return

    # Resolve only the parent installation root. Do not resolve individual skill
    # symlinks: replacing a symlink must never overwrite its external target.
    if agent_home == REPO or REPO in agent_home.parents or agent_home in REPO.parents:
        raise ValueError('Keep the checkout outside the target agent home.')
    agent_home.mkdir(parents=True, exist_ok=True)
    for parent in [skills_root, agent_home / 'skill-support', agent_home / 'skill-backups']:
        if parent.is_symlink():
            raise ValueError(f'Installation parent is a symlink; select its intended real agent home explicitly: {parent}')
    lock_path = agent_home / '.kiki-custom-install.lock'
    lock = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(lock)
    stage = None
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    backup_root = agent_home / 'skill-backups' / 'kiki-custom-skill' / timestamp
    journal = []
    try:
        stage = Path(tempfile.mkdtemp(prefix='.kiki-custom-stage-', dir=agent_home))
        latexmk = shutil.which('latexmk') or 'latexmk'
        xelatex = shutil.which('xelatex')
        texbin = str(Path(xelatex).parent) if xelatex else ('/Library/TeX/texbin' if platform.system() == 'Darwin' else '/usr/bin')
        replacements = {
            '@@KIKI_SKILLS_DIR@@': str(skills_root),
            '@@KIKI_SUPPORT_DIR@@': str(support_root),
            '@@KIKI_AGENT_HOME@@': str(agent_home),
            '@@KIKI_HOME@@': str(Path.home()),
            '@@KIKI_PYTHON@@': sys.executable,
            '@@KIKI_LATEXMK@@': latexmk,
            '@@KIKI_TEXBIN@@': texbin,
            '@@KIKI_AGENT@@': client,
            '@@KIKI_PROFILE@@': profile['name'],
        }
        if set(replacements) != TOKEN_NAMES:
            raise ValueError('Manifest token list and installer must be updated together.')
        names = {entry['name'] for entry in MANIFEST['skills']} | {entry['directory'] for entry in MANIFEST['skills']}
        copy_rendered(REPO / 'support', stage / 'support', replacements, client, names)
        for name in selected:
            copy_rendered(REPO / 'skills' / name, stage / 'skills' / name, replacements, client, names)

        # All file preparation precedes mutation of an existing installed skill.
        operations = [(stage / 'support', support_root, backup_root / 'support')]
        operations += [(stage / 'skills' / name, skills_root / name, backup_root / 'skills' / name) for name in selected]
        for prepared, destination, backup in operations:
            destination.parent.mkdir(parents=True, exist_ok=True)
            item = {'destination': destination, 'backup': backup, 'moved_old': False, 'installed_new': False}
            journal.append(item)
            if present(destination):
                backup.parent.mkdir(parents=True, exist_ok=True)
                os.replace(destination, backup)
                item['moved_old'] = True
            os.replace(prepared, destination)
            item['installed_new'] = True

        result = dict(plan, installed_at=datetime.now(timezone.utc).isoformat(),
                      source_checkout=str(REPO), backup_directory=str(backup_root),
                      skills=selected, machine=platform.node(), profile_settings=profile)
        (support_root / 'installation-state.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except BaseException:
        # Restore each replaced entry on a handled failure/interruption. The
        # uniquely named backup directory is retained for inspection.
        for item in reversed(journal):
            if item['installed_new']:
                remove_created(item['destination'])
            if item['moved_old']:
                os.replace(item['backup'], item['destination'])
        raise
    finally:
        if stage is not None and stage.exists():
            shutil.rmtree(stage)
        lock_path.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True, choices=['codex', 'claude', 'both'])
    parser.add_argument('--profile', choices=['auto', 'mac', 'a6000-4', 'a6000-8', 'generic'], default='auto')
    parser.add_argument('--skills', nargs='+', help='Optional skill directory names; default is all 200 personal skills.')
    parser.add_argument('--codex-home', type=Path, default=Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex'))
    parser.add_argument('--claude-home', type=Path, default=Path(os.environ.get('CLAUDE_CONFIG_DIR') or Path.home() / '.claude'))
    parser.add_argument('--dry-run', action='store_true', help='Print paths/conflicts only; write no files.')
    args = parser.parse_args()
    known = {entry['directory'] for entry in MANIFEST['skills']}
    selected = sorted(set(args.skills or known))
    unknown = set(selected) - known
    if unknown:
        parser.error('Unknown skill directories: ' + ', '.join(sorted(unknown)))
    profile_name = args.profile if args.profile != 'auto' else ('mac' if platform.system() == 'Darwin' else 'generic')
    profile = json.loads((REPO / 'profiles' / (profile_name + '.json')).read_text(encoding='utf-8'))
    clients = ['codex', 'claude'] if args.target == 'both' else [args.target]
    homes = {'codex': args.codex_home.expanduser().resolve(), 'claude': args.claude_home.expanduser().resolve()}
    if args.target == 'both' and homes['codex'] == homes['claude']:
        parser.error('Codex and Claude Code must have different installation homes.')
    for client in clients:
        install_client(client, homes[client], selected, profile, args.dry_run)


if __name__ == '__main__':
    main()
