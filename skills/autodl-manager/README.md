# AutoDL Manager

Comprehensive management tool for AutoDL cloud GPU instances.

## Features

### Core Capabilities

- **Instance Management** - Add, list, remove instances with credentials
- **Quick Connect** - SSH with auto-login (no password typing)
- **GPU Detection** - Automatically detect GPU-enabled vs CPU-only mode
- **Disk Monitoring** - Real-time usage with color-coded alerts
- **Conda Setup** - Auto-detect and initialize conda
- **Network Turbo** - Check and enable acceleration
- **Status Dashboard** - Comprehensive instance health check

### Key Differentiators

**1. GPU Mode Detection**
- Automatically detects if instance has GPU or is CPU-only
- Critical for cost management (GPU vs CPU pricing)

**2. Conda Initialization Check**
- New instances often have conda not initialized
- Skill auto-detects and can initialize for you

**3. Multi-Instance Management**
- Manage multiple AutoDL instances from one place
- Quick switching between instances
- Track hardware specs

## Quick Start

### 1. Install sshpass (Required)

```bash
# macOS
brew install hudochenkov/sshpass/sshpass

# Linux (Debian/Ubuntu)
sudo apt-get install sshpass
```

### 2. Add Your First Instance

```bash
python3 scripts/autodl_cli.py add scbenchmark \
  --host connect.westb.seetacloud.com \
  --port 15049 \
  --password "yourpass" \
  --gpu "2x RTX4090"
```

### 3. Setup the Instance

```bash
# Initialize conda and check turbo
python3 scripts/autodl_cli.py setup scbenchmark
```

### 4. Check Status

```bash
python3 scripts/autodl_cli.py status scbenchmark
```

**Example output:**
```
🔍 Checking status: scbenchmark

GPU Status:
  ✅ GPU 0: NVIDIA GeForce RTX 4090
     Usage: 85%, Memory: 18234/24564 MB

Disk Status:
  ⚠️  82% used (41G/50G, 9.1G available)

Conda Status:
  ✅ Conda initialized: /root/miniconda3

Network Turbo:
  ✅ Network turbo active
```

### 5. Connect

```bash
python3 scripts/autodl_cli.py connect scbenchmark
# Opens SSH session in /root/autodl-tmp/
```

## Commands

### Instance Management

```bash
# Add instance
autodl_cli.py add <name> --host <host> --port <port> [options]

# List all instances
autodl_cli.py list

# List with details
autodl_cli.py list -v

# Remove instance
autodl_cli.py remove <name>
```

### Status & Monitoring

```bash
# Comprehensive status check
autodl_cli.py status <name>

# Disk usage analysis
autodl_cli.py disk <name>
```

### Connection & Setup

```bash
# SSH to instance
autodl_cli.py connect <name>

# Setup new instance
autodl_cli.py setup <name>

# Enable network turbo
autodl_cli.py turbo <name>
```

## Use Cases

### Use Case 1: First-Time Setup

**Scenario:** Just got a new AutoDL instance.

```bash
# 1. Add instance
autodl_cli.py add my-instance \
  --host connect.westb.seetacloud.com \
  --port 12345 \
  --gpu "2x A6000"

# 2. Setup (conda + turbo)
autodl_cli.py setup my-instance

# 3. Connect
autodl_cli.py connect my-instance

# 4. Inside instance: enable turbo
source /etc/network_turbo

# 5. Start work
conda activate myenv
python train.py
```

### Use Case 2: Check Before Connecting

**Scenario:** Want to verify instance state before SSH.

```bash
# Check everything
autodl_cli.py status scbenchmark

# If GPU shows "No GPU detected":
# - Instance is in CPU-only mode (saving cost)
# - Or GPU not allocated yet

# If disk >90%:
# - Clean up before starting new work
```

### Use Case 3: Managing Multiple Instances

**Scenario:** Running experiments on multiple AutoDL servers.

```bash
# Add all instances
autodl_cli.py add prep-cpu --host ... --port 10001
autodl_cli.py add train-gpu1 --host ... --port 10002
autodl_cli.py add train-gpu2 --host ... --port 10003

# List all
autodl_cli.py list
# Shows all 3 instances

# Check specific one
autodl_cli.py status train-gpu1

# Connect to the one you need
autodl_cli.py connect train-gpu2
```

### Use Case 4: Disk Space Alert

**Scenario:** Disk usage is high, need to clean up.

```bash
# Check disk
autodl_cli.py disk scbenchmark

# Shows:
# 💾 Disk Usage: scbenchmark
# 
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/vda1        50G   45G   5G  90% /root/autodl-tmp
# 
# 📂 Largest directories:
# 7.6G    /root/autodl-tmp/old-experiment/
# 2.4G    /root/autodl-tmp/cached-models/

# Connect and clean up
autodl_cli.py connect scbenchmark
# rm -rf /root/autodl-tmp/old-experiment/
```

## Configuration

**Storage:** `@@KIKI_AGENT_HOME@@/autodl_instances.json`

**Template:** See `assets/instances.json.template`

**Example config:**
```json
{
  "instances": {
    "scbenchmark": {
      "host": "connect.westb.seetacloud.com",
      "port": 15049,
      "user": "root",
      "password": "yourpass",
      "workdir": "/root/autodl-tmp/",
      "gpu": "2x RTX4090",
      "cpu": "50 cores",
      "ram": "180GB",
      "disk": "50GB"
    }
  }
}
```

## Integration

### With Memory System

Log instance status to daily entry:
```bash
autodl_cli.py status scbenchmark >> memory/daily/$(date +%Y-%m-%d).md
```

### With Notifications

Alert on disk >90%:
```bash
# In HEARTBEAT.md or cron
DISK=$(autodl_cli.py status scbenchmark | grep "used" | grep -oE "[0-9]+%")
if [[ ${DISK%\%} -gt 90 ]]; then
    message send --to telegram "⚠️ AutoDL disk ${DISK}"
fi
```

### With Cron

Periodic checks:
```bash
# Every 2 hours, check disk
0 */2 * * * autodl_cli.py disk scbenchmark | grep "9[0-9]%" && notify_user
```

## Troubleshooting

### "sshpass not installed"

**Solution:**
```bash
brew install hudochenkov/sshpass/sshpass
```

### "Connection refused"

**Solution:**
1. Check AutoDL console for new port
2. Update: `autodl_cli.py add <name> --port <new-port>`

### "Conda not initialized"

**Solution:**
```bash
autodl_cli.py setup <name>
```

### "Disk 99% full"

**Solution:**
```bash
autodl_cli.py disk <name>  # See largest dirs
autodl_cli.py connect <name>  # Clean up
```

## Documentation

- **[SKILL.md](SKILL.md)** - Complete skill reference
- **[references/common-issues.md](references/common-issues.md)** - Troubleshooting guide
- **[references/best-practices.md](references/best-practices.md)** - Advanced tips

## Best Practices

### 1. Always Check Status First

```bash
autodl_cli.py status <name>
# Know GPU mode, disk space, conda state
```

### 2. Setup New Instances Immediately

```bash
autodl_cli.py setup <name>
# Initialize conda, check turbo
```

### 3. Monitor Disk Proactively

```bash
# Don't wait for 100%
autodl_cli.py disk <name>
```

### 4. Use Network Turbo

```bash
# Inside instance, before downloads:
source /etc/network_turbo
```

### 5. Use Descriptive Names

```bash
# Good: training-rtx4090, prep-cpu
# Bad: instance1, test
```

## Examples

### Example 1: Daily Workflow

```bash
# Morning: Check before connecting
autodl_cli.py status training-gpu
# ✅ GPU available, disk 65%, conda ready

# Connect
autodl_cli.py connect training-gpu

# Inside: Enable turbo, activate env, start work
source /etc/network_turbo
conda activate myenv
python train.py
```

### Example 2: New Instance Setup

```bash
# Add
autodl_cli.py add new-instance \
  --host connect.westb.seetacloud.com \
  --port 23456

# Setup
autodl_cli.py setup new-instance
# ✅ Conda initialized
# ✅ Network turbo available

# Connect and verify
autodl_cli.py connect new-instance
conda info  # Should work
nvidia-smi  # Check GPU
```

### Example 3: Emergency Cleanup

```bash
# Disk is 95% full
autodl_cli.py disk scbenchmark
# Shows largest dirs

autodl_cli.py connect scbenchmark
# Clean up manually:
# conda clean --all
# rm -rf old-experiments/
# rm *.tar.gz
```

## Tips

- **GPU detection is automatic** - No need to manually specify mode
- **Conda check saves time** - Know if you need to initialize
- **Disk alerts prevent disasters** - Don't run out of space mid-training
- **Quick connect is fast** - No password typing
- **Multi-instance support** - Manage all AutoDL servers in one place

## Ready to Use

1. ✅ Install sshpass
2. ✅ Add your first instance
3. ✅ Run setup
4. ✅ Check status
5. ✅ Connect and work

**Start now:**
```bash
python3 scripts/autodl_cli.py --help
```
