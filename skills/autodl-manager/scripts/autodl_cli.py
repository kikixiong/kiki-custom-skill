#!/usr/bin/env python3
"""
AutoDL Manager - Manage AutoDL cloud GPU instances

Main CLI tool for instance management, monitoring, and quick access.
"""

import click
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple
import getpass
import os

CONFIG_FILE = Path(os.environ.get("AUTODL_CONFIG_FILE", Path("@@KIKI_AGENT_HOME@@/autodl_instances.json"))).expanduser()

def load_config() -> Dict:
    """Load instance configuration"""
    if not CONFIG_FILE.exists():
        return {"instances": {}}
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        click.echo(f"Error loading config: {e}", err=True)
        return {"instances": {}}

def save_config(config: Dict):
    """Save instance configuration"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def run_ssh_command(instance: Dict, command: str, quiet=False) -> Tuple[int, str, str]:
    """
    Run command on remote instance via SSH
    Returns: (exit_code, stdout, stderr)
    """
    ssh_cmd = [
        'sshpass', '-p', instance['password'],
        'ssh', '-p', str(instance['port']),
        '-o', 'StrictHostKeyChecking=no',
        '-o', 'UserKnownHostsFile=/dev/null',
        '-o', 'LogLevel=ERROR',
        f"{instance.get('user', 'root')}@{instance['host']}",
        command
    ]
    
    try:
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if not quiet:
            if result.returncode != 0:
                click.echo(f"SSH command failed: {result.stderr}", err=True)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "SSH command timeout"
    except FileNotFoundError:
        click.echo("Error: sshpass not installed. Install with: brew install hudochenkov/sshpass/sshpass", err=True)
        return 1, "", "sshpass not found"

@click.group()
def cli():
    """AutoDL instance manager"""
    pass

@cli.command()
@click.argument('name')
@click.option('--host', required=True, help='SSH host (e.g., gpu.example.invalid)')
@click.option('--port', required=True, type=int, help='SSH port')
@click.option('--password', help='SSH password (will prompt if not provided)')
@click.option('--user', default='root', help='SSH user (default: root)')
@click.option('--workdir', default='/root/autodl-tmp/', help='Working directory')
@click.option('--gpu', help='GPU info (e.g., "2x RTX4090")')
@click.option('--cpu', help='CPU info')
@click.option('--ram', help='RAM size')
@click.option('--disk', help='Disk size')
def add(name, host, port, password, user, workdir, gpu, cpu, ram, disk):
    """Add a new AutoDL instance"""
    config = load_config()
    
    if name in config['instances']:
        if not click.confirm(f"Instance '{name}' already exists. Overwrite?"):
            return
    
    # Prompt for password if not provided
    if not password:
        password = getpass.getpass(f"Password for {name}: ")
    
    config['instances'][name] = {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'workdir': workdir,
        'gpu': gpu,
        'cpu': cpu,
        'ram': ram,
        'disk': disk,
        'added_at': subprocess.check_output(['date', '+%Y-%m-%d']).decode().strip()
    }
    
    save_config(config)
    click.echo(f"✅ Added instance: {name}")
    click.echo(f"   Host: {host}:{port}")
    if gpu:
        click.echo(f"   GPU: {gpu}")

@cli.command()
@click.option('--verbose', '-v', is_flag=True, help='Show detailed info')
def list(verbose):
    """List all instances"""
    config = load_config()
    instances = config.get('instances', {})
    
    if not instances:
        click.echo("No instances configured. Use 'autodl add' to add one.")
        return
    
    click.echo(f"\n📋 AutoDL Instances ({len(instances)}):\n")
    
    for name, info in sorted(instances.items()):
        host_info = f"{info['host']}:{info['port']}"
        click.echo(f"  {name}")
        click.echo(f"    Host: {host_info}")
        
        if verbose:
            if info.get('gpu'):
                click.echo(f"    GPU: {info['gpu']}")
            if info.get('cpu'):
                click.echo(f"    CPU: {info['cpu']}")
            if info.get('ram'):
                click.echo(f"    RAM: {info['ram']}")
            click.echo(f"    Workdir: {info.get('workdir', 'N/A')}")
        click.echo()

@cli.command()
@click.argument('name')
def status(name):
    """Check instance status (GPU, disk, conda)"""
    config = load_config()
    
    if name not in config['instances']:
        click.echo(f"Error: Instance '{name}' not found", err=True)
        sys.exit(1)
    
    instance = config['instances'][name]
    click.echo(f"\n🔍 Checking status: {name}\n")
    
    # 1. Check GPU status
    click.echo("GPU Status:")
    code, stdout, stderr = run_ssh_command(instance, "nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits 2>/dev/null || echo 'NO_GPU'", quiet=True)
    
    if stdout.strip() == 'NO_GPU' or code != 0:
        click.echo("  ⚠️  No GPU detected (CPU-only mode)")
        gpu_available = False
    else:
        gpu_available = True
        lines = stdout.strip().split('\n')
        for line in lines:
            parts = line.split(', ')
            if len(parts) >= 5:
                gpu_id, gpu_name, util, mem_used, mem_total = parts[:5]
                click.echo(f"  ✅ GPU {gpu_id}: {gpu_name}")
                click.echo(f"     Usage: {util}%, Memory: {mem_used}/{mem_total} MB")
    
    # 2. Check disk usage
    click.echo("\nDisk Status:")
    code, stdout, stderr = run_ssh_command(instance, "df -h /root/autodl-tmp 2>/dev/null | tail -1", quiet=True)
    
    if code == 0 and stdout:
        parts = stdout.split()
        if len(parts) >= 5:
            used_pct = parts[4].rstrip('%')
            used = parts[2]
            total = parts[1]
            avail = parts[3]
            
            try:
                pct = int(used_pct)
                if pct >= 90:
                    icon = "🔴"
                elif pct >= 80:
                    icon = "⚠️"
                else:
                    icon = "✅"
                
                click.echo(f"  {icon} {used_pct}% used ({used}/{total}, {avail} available)")
            except ValueError:
                click.echo(f"  {stdout.strip()}")
    
    # 3. Check conda initialization
    click.echo("\nConda Status:")
    code, stdout, stderr = run_ssh_command(instance, "conda info --base 2>/dev/null", quiet=True)
    
    if code == 0 and stdout:
        click.echo(f"  ✅ Conda initialized: {stdout.strip()}")
    else:
        click.echo("  ⚠️  Conda not initialized")
        click.echo("     Run: autodl setup " + name)
    
    # 4. Check network turbo
    click.echo("\nNetwork Turbo:")
    code, stdout, stderr = run_ssh_command(instance, "[ -f /etc/network_turbo ] && echo 'AVAILABLE' || echo 'NOT_FOUND'", quiet=True)
    
    if 'AVAILABLE' in stdout:
        # Check if sourced in current environment
        code2, stdout2, _ = run_ssh_command(instance, "env | grep -i turbo | head -1 || echo 'NOT_ACTIVE'", quiet=True)
        if 'NOT_ACTIVE' in stdout2:
            click.echo("  ⚠️  Network turbo available but not active")
            click.echo("     Run: autodl turbo " + name)
        else:
            click.echo("  ✅ Network turbo active")
    else:
        click.echo("  ❌ Network turbo not available")
    
    click.echo()

@cli.command()
@click.argument('name')
def connect(name):
    """SSH to instance"""
    config = load_config()
    
    if name not in config['instances']:
        click.echo(f"Error: Instance '{name}' not found", err=True)
        sys.exit(1)
    
    instance = config['instances'][name]
    workdir = instance.get('workdir', '/root/autodl-tmp/')
    
    # Build SSH command with auto-cd to workdir
    ssh_cmd = [
        'sshpass', '-p', instance['password'],
        'ssh', '-p', str(instance['port']),
        '-o', 'StrictHostKeyChecking=no',
        '-o', 'UserKnownHostsFile=/dev/null',
        '-t',  # Force pseudo-terminal
        f"{instance.get('user', 'root')}@{instance['host']}",
        f"cd {workdir} && exec bash -l"
    ]
    
    click.echo(f"🔌 Connecting to {name}...")
    try:
        subprocess.run(ssh_cmd)
    except FileNotFoundError:
        click.echo("Error: sshpass not installed", err=True)
        click.echo("Install with: brew install hudochenkov/sshpass/sshpass", err=True)
        sys.exit(1)

@cli.command()
@click.argument('name')
def disk(name):
    """Check disk usage with cleanup suggestions"""
    config = load_config()
    
    if name not in config['instances']:
        click.echo(f"Error: Instance '{name}' not found", err=True)
        sys.exit(1)
    
    instance = config['instances'][name]
    click.echo(f"\n💾 Disk Usage: {name}\n")
    
    # Overall usage
    code, stdout, _ = run_ssh_command(instance, "df -h /root/autodl-tmp", quiet=True)
    if code == 0:
        click.echo(stdout)
    
    # Largest directories
    click.echo("\n📂 Largest directories:\n")
    code, stdout, _ = run_ssh_command(instance, "du -h /root/autodl-tmp/* 2>/dev/null | sort -rh | head -10", quiet=True)
    if code == 0:
        click.echo(stdout)
    
    click.echo()

@cli.command()
@click.argument('name')
def setup(name):
    """Setup new instance (conda init + network turbo)"""
    config = load_config()
    
    if name not in config['instances']:
        click.echo(f"Error: Instance '{name}' not found", err=True)
        sys.exit(1)
    
    instance = config['instances'][name]
    click.echo(f"\n⚙️  Setting up instance: {name}\n")
    
    # 1. Check conda
    click.echo("1. Checking conda...")
    code, stdout, _ = run_ssh_command(instance, "conda info --base 2>/dev/null", quiet=True)
    
    if code != 0 or not stdout:
        click.echo("   Initializing conda...")
        
        # Detect shell
        code, shell_out, _ = run_ssh_command(instance, "echo $SHELL", quiet=True)
        shell = 'bash' if 'bash' in shell_out else 'zsh' if 'zsh' in shell_out else 'bash'
        
        # Init conda
        init_cmd = f"conda init {shell} && source ~/.{shell}rc"
        code, stdout, stderr = run_ssh_command(instance, init_cmd, quiet=True)
        
        if code == 0:
            click.echo(f"   ✅ Conda initialized for {shell}")
        else:
            click.echo(f"   ⚠️  Conda init failed: {stderr}")
    else:
        click.echo(f"   ✅ Conda already initialized: {stdout.strip()}")
    
    # 2. Check network turbo
    click.echo("\n2. Checking network turbo...")
    code, stdout, _ = run_ssh_command(instance, "[ -f /etc/network_turbo ] && echo 'EXISTS' || echo 'NOT_FOUND'", quiet=True)
    
    if 'EXISTS' in stdout:
        click.echo("   ✅ Network turbo available at /etc/network_turbo")
        click.echo("   💡 Run 'autodl turbo " + name + "' to activate")
    else:
        click.echo("   ⚠️  Network turbo not found on this instance")
    
    # 3. Create workdir if not exists
    click.echo("\n3. Ensuring workdir exists...")
    workdir = instance.get('workdir', '/root/autodl-tmp/')
    code, _, _ = run_ssh_command(instance, f"mkdir -p {workdir}", quiet=True)
    if code == 0:
        click.echo(f"   ✅ Workdir ready: {workdir}")
    
    click.echo("\n✅ Setup complete!")
    click.echo(f"\nConnect with: autodl connect {name}")

@cli.command()
@click.argument('name')
def turbo(name):
    """Enable network acceleration"""
    config = load_config()
    
    if name not in config['instances']:
        click.echo(f"Error: Instance '{name}' not found", err=True)
        sys.exit(1)
    
    instance = config['instances'][name]
    
    # Check if turbo exists
    code, stdout, _ = run_ssh_command(instance, "[ -f /etc/network_turbo ] && echo 'EXISTS' || echo 'NOT_FOUND'", quiet=True)
    
    if 'NOT_FOUND' in stdout:
        click.echo("⚠️  Network turbo not available on this instance")
        return
    
    click.echo(f"🚀 Enabling network turbo on {name}...")
    click.echo("\n💡 To use turbo in your session:")
    click.echo(f"   autodl connect {name}")
    click.echo(f"   source /etc/network_turbo")
    click.echo("\n   This significantly speeds up downloads, git clone, pip install, etc.")

@cli.command()
@click.argument('name')
def remove(name):
    """Remove an instance from config"""
    config = load_config()
    
    if name not in config['instances']:
        click.echo(f"Error: Instance '{name}' not found", err=True)
        sys.exit(1)
    
    if click.confirm(f"Remove instance '{name}'?"):
        del config['instances'][name]
        save_config(config)
        click.echo(f"✅ Removed instance: {name}")

if __name__ == '__main__':
    cli()
