"""检查：仅手动的 skill 是否都被某个 *-router 收录；router 引用的目录是否存在；自动列表描述总长。"""
import os, re
import sys
root = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/.claude/skills')
def fm(n):
    t = open(f'{root}/{n}/SKILL.md', encoding='utf-8', errors='ignore').read()
    m = re.match(r'^---\n(.*?)\n---', t, re.S)
    return m.group(1) if m else ''
skills = sorted(d for d in os.listdir(root) if os.path.isfile(f'{root}/{d}/SKILL.md'))
manual = {n for n in skills if re.search(r'^disable-model-invocation:\s*true', fm(n), re.M)}
routed = {}
for r in (n for n in skills if n.endswith('-router')):
    body = open(f'{root}/{r}/SKILL.md', encoding='utf-8').read()
    for x in re.findall(r'^\| `([a-z0-9-]+)`', body, re.M):
        routed.setdefault(x, []).append(r)
print('skills', len(skills), '| manual-only', len(manual), '| auto', len(skills) - len(manual))
print('orphans (manual-only, not in any router):', sorted(manual - routed.keys()) or 'none')
print('router refs to missing dirs:', sorted(set(routed) - set(skills)) or 'none')
print('router refs still auto-invocable:', sorted(set(routed) - manual) or 'none')
total = 0
for n in skills:
    if n in manual: continue
    d = re.search(r'^description:\s*(.*?)(?=^\w[\w-]*:|\Z)', fm(n), re.S | re.M)
    total += len(n) + len(' '.join(d.group(1).split()) if d else '')
print('auto-list description chars:', total)
