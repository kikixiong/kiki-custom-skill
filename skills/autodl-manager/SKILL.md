---
name: autodl-manager
description: Manage AutoDL cloud GPU instances with SSH connection, GPU status detection, disk monitoring, conda initialization, and network acceleration. Use when connecting to AutoDL, checking instance status, monitoring disk space, setting up new instances, or managing multiple AutoDL servers. Automatically detects GPU-enabled vs CPU-only instances.
disable-model-invocation: true
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# AutoDL Manager

Comprehensive management for AutoDL cloud GPU instances.

## When to Use

Use this skill when:
- Connecting to AutoDL instances
- Checking GPU availability (GPU vs CPU-only)
- Monitoring disk space
- Setting up new instances (conda init)
- Enabling network acceleration
- Managing multiple AutoDL instances
- Tracking training jobs on AutoDL

## Core Features

### 1. Instance Management
- Add/remove instances with credentials
- List all configured instances
- Quick connect with auto-login
- Track hardware specs (GPU, CPU, RAM)

### 2. GPU Status Detection
**Automatically detects two modes:**
- **GPU-enabled**: Shows GPU models, utilization, memory
- **CPU-only**: Alerts when no GPU (cost-saving mode)

### 3. Disk Monitoring
- Real-time disk usage
- Alert when >80% (warning) or >90% (critical)
- Show largest directories
- Cleanup suggestions

### 4. Conda Initialization
- Auto-detect if conda is initialized
- Initialize conda for bash/zsh
- Verify conda environment

### 5. Network Acceleration
- Check if turbo is available
- Instructions to enable
- Verify turbo status

Example hosts use the reserved `.invalid` domain. Fill `SSH_PORT` and any hardware-description placeholders from the actual instance before running a command.

## Commands

### Instance Management

#### `autodl add <name>`
Add a new AutoDL instance.

**Options:**
- `--host` - SSH host (required)
- `--port` - SSH port (required)
- `--password` - SSH password (optional, will prompt)
- `--user` - SSH user (default: root)
- `--workdir` - Working directory (default: /root/autodl-tmp/)
- `--gpu` - GPU info (e.g., "<GPU_DESCRIPTION>")
- `--cpu` - CPU info
- `--ram` - RAM size
- `--disk` - Disk size

**Example:**
```bash
autodl add example-project \
  --host gpu.example.invalid \
  --port "$SSH_PORT" \
  --gpu "<GPU_DESCRIPTION>" \
  --cpu "<CPU_DESCRIPTION>" \
  --ram "<RAM_DESCRIPTION>"
```

#### `autodl list`
List all configured instances.

**Options:**
- `-v, --verbose` - Show detailed info

**Example:**
```bash
autodl list
# Output:
# 📋 AutoDL Instances (2):
#
#   example-project
#     Host: gpu.example.invalid:<SSH_PORT>
#
#   qwen2-audio
#     Host: gpu.example.invalid:<SSH_PORT>
```

#### `autodl remove <name>`
Remove an instance from configuration.

### Connection

#### `autodl connect <name>`
SSH to instance with auto-login.

**What it does:**
1. Auto-fills password (using sshpass)
2. Changes to workdir
3. Opens interactive shell

**Example:**
```bash
autodl connect example-project
# 🔌 Connecting to example-project...
# [Opens SSH session in /root/autodl-tmp/]
```

### Status Checking

#### `autodl status <name>`
Comprehensive status check.

**Checks:**
1. **GPU Status**
   - GPU-enabled: Shows GPU models, utilization, memory
   - CPU-only: Alerts "No GPU detected"
2. **Disk Usage**
   - Used percentage with color-coded alerts
   - Available space
3. **Conda Status**
   - Initialized or not
   - Conda base path
4. **Network Turbo**
   - Available or not
   - Active or inactive

**Example output:**
```bash
autodl status example-project

🔍 Checking status: example-project

GPU Status:
  ✅ GPU 0: NVIDIA GeForce RTX 4090
     Usage: 85%, Memory: 18234/24564 MB
  ✅ GPU 1: NVIDIA GeForce RTX 4090
     Usage: 12%, Memory: 2048/24564 MB

Disk Status:
  ⚠️  82% used (41G/50G, 9.1G available)

Conda Status:
  ✅ Conda initialized: /root/miniconda3

Network Turbo:
  ⚠️  Network turbo available but not active
     Run: autodl turbo example-project
```

**CPU-only mode example:**
```bash
autodl status qwen2-audio

🔍 Checking status: qwen2-audio

GPU Status:
  ⚠️  No GPU detected (CPU-only mode)

Disk Status:
  ✅ 48% used (24G/50G, 26G available)

Conda Status:
  ⚠️  Conda not initialized
     Run: autodl setup qwen2-audio

Network Turbo:
  ✅ Network turbo active
```

#### `autodl disk <name>`
Detailed disk usage analysis.

**Shows:**
- Overall disk usage
- Top 10 largest directories

**Example:**
```bash
autodl disk example-project

💾 Disk Usage: example-project

Filesystem      Size  Used Avail Use% Mounted on
/dev/vda1        50G   41G  9.1G  82% /root/autodl-tmp

📂 Largest directories:

7.6G    /root/autodl-tmp/example-dataset/
2.4G    /root/autodl-tmp/example-model/
1.2G    /root/autodl-tmp/example-project/
856M    /root/autodl-tmp/example-run/
```

### Setup & Utilities

#### `autodl setup <name>`
Initialize a new instance.

**What it does:**
1. Check and initialize conda (for bash or zsh)
2. Verify network turbo availability
3. Create workdir if needed

**Example:**
```bash
autodl setup example-project

⚙️  Setting up instance: example-project

1. Checking conda...
   Initializing conda...
   ✅ Conda initialized for bash

2. Checking network turbo...
   ✅ Network turbo available at /etc/network_turbo
   💡 Run 'autodl turbo example-project' to activate

3. Ensuring workdir exists...
   ✅ Workdir ready: /root/autodl-tmp/

✅ Setup complete!

Connect with: autodl connect example-project
```

#### `autodl turbo <name>`
Enable network acceleration.

**What it shows:**
- Instructions to source /etc/network_turbo
- Benefits of turbo mode

**Example:**
```bash
autodl turbo example-project

🚀 Enabling network turbo on example-project...

💡 To use turbo in your session:
   autodl connect example-project
   source /etc/network_turbo

   This significantly speeds up downloads, git clone, pip install, etc.
```

## Typical Workflows

### First-Time Setup

**Scenario:** Just got a new AutoDL instance.

```bash
# 1. Add instance
autodl add my-instance \
  --host gpu.example.invalid \
  --port 12345 \
  --gpu "2x A6000"

# 2. Setup (conda + turbo check)
autodl setup my-instance

# 3. Connect
autodl connect my-instance

# 4. Inside instance: enable turbo
source /etc/network_turbo
```

### Daily Usage

**Scenario:** Connect and check status.

```bash
# Check before connecting
autodl status example-project

# Connect if all good
autodl connect example-project
```

### Monitoring Disk

**Scenario:** Running out of space.

```bash
# Quick check
autodl status example-project
# ⚠️  82% used

# Detailed analysis
autodl disk example-project
# Shows largest dirs

# Connect and clean up
autodl connect example-project
# rm -rf /root/autodl-tmp/old-experiment/
```

### GPU vs CPU Mode

**Scenario:** Switched from GPU to CPU-only to save cost.

```bash
# Check current mode
autodl status example-project

# If CPU-only mode:
# GPU Status:
#   ⚠️  No GPU detected (CPU-only mode)

# This is normal when:
# - Doing data download/preparation
# - Instance is stopped/paused
# - Switched to CPU-only config to save money
```

## Configuration

**Storage location:** `@@KIKI_AGENT_HOME@@/autodl_instances.json`

**Format:**
```json
{
  "instances": {
    "example-project": {
      "host": "gpu.example.invalid",
      "port": "<SSH_PORT>",
      "user": "root",
      "password": "yourpassword",
      "workdir": "/root/autodl-tmp/",
      "gpu": "<GPU_DESCRIPTION>",
      "cpu": "<CPU_DESCRIPTION>",
      "ram": "<RAM_DESCRIPTION>",
      "disk": "<DISK_DESCRIPTION>",
      "added_at": "2026-03-18"
    }
  }
}
```

**Security:** Passwords are stored in plain text. Consider using:
- SSH keys (upload public key to AutoDL)
- System keychain (future enhancement)

## Requirements

### System Dependencies

**sshpass** (for auto-login):
```bash
# macOS
brew install hudochenkov/sshpass/sshpass

# Linux (Debian/Ubuntu)
apt-get install sshpass

# Linux (RHEL/CentOS)
yum install sshpass
```

### Python Dependencies

None - uses only standard library.

## Critical: Post-SSH First Steps

**Every time you SSH into an AutoDL instance, run these immediately:**

```bash
source /etc/network_turbo    # ALWAYS first — enables fast networking
```

This is not optional. Without it, git clone, pip install, and model downloads are 5-10x slower.

## Port Change Detection

AutoDL frequently reassigns SSH ports when instances restart or resume. **Always verify the port before connecting.**

### Detection Workflow
1. If `ssh -p <port>` fails with "Connection refused", the port likely changed
2. Check the AutoDL web console (https://www.autodl.com) for the current port
3. Update `TOOLS.md` and `@@KIKI_AGENT_HOME@@/autodl_instances.json` with the new port
4. Log the change to `.learnings/ERRORS.md` if it caused issues

### Proactive Check (add to HEARTBEAT.md)
```bash
# Quick port connectivity check
ssh -o ConnectTimeout=5 -p <port> root@<host> "echo ok" 2>/dev/null || echo "PORT_CHANGED"
```

## GPU Status + Disk Space Periodic Check

Add this to your heartbeat routine (every 4-8 hours during active research):

```bash
# One-liner status check via SSH
ssh -p <port> root@<host> "source /etc/network_turbo; nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader; echo '---'; df -h /root/autodl-tmp/"
```

**Alert thresholds:**
- Disk > 80%: Warning — clean up old checkpoints
- Disk > 90%: Critical — training may fail due to no space
- GPU utilization 0% during expected training: Check if process crashed

## Training Result Auto-Pull

After remote training completes, pull **lightweight result files only** to local machine for analysis:

**拉什么（< 10MB）：**
- CSV/JSON 指标文件（几 KB ~ 几百 KB）
- Training log 摘要（tail 最后几百行）
- 图片（loss curve、对比图）

**不拉什么（留在服务器）：**
- ❌ 模型权重（.pt/.bin，几百 MB ~ 几 GB）
- ❌ 完整数据集
- ❌ 完整 training log（只拉 tail）

```bash
# 1. Pull metrics/logs (small files only)
scp -P <port> root@<host>:/root/autodl-tmp/<project>/results/*.csv ./data/
scp -P <port> root@<host>:/root/autodl-tmp/<project>/results/*.json ./data/
scp -P <port> root@<host>:/root/autodl-tmp/<project>/results/*.png ./data/

# 2. Pull training log summary (NOT full log)
ssh -p <port> root@<host> "tail -200 /root/autodl-tmp/<project>/train.log" > ./data/train_summary.log

# 3. rsync with size limit for incremental sync
rsync -avz --max-size=10m -e "ssh -p <port>" root@<host>:/root/autodl-tmp/<project>/results/ ./data/results/
```

**⚠️ 模型权重保留在服务器上**，需要时再用 SSH 直接加载或单独手动下载。

**Integrate with autoresearch**: After pulling results, update `research-state.yaml` — move the experiment from `active_experiments` to `experiments.trajectory` with the metrics.

## Autoresearch Watchdog Integration

When autoresearch tracks a remote experiment on AutoDL, the watchdog checks:

```yaml
# In research-state.yaml
active_experiments:
  - id: "exp_001"
    type: remote
    ssh_host: "root@gpu.example.invalid"
    ssh_port: "<SSH_PORT>"
    progress_file: "/root/autodl-tmp/project/logs/train.log"
    result_file: "/root/autodl-tmp/project/results/metrics.json"
    stall_threshold_min: 60
```

**Watchdog check sequence** (on each continuity tick):
1. SSH connectivity test (catches port changes)
2. `stat` on progress_file — is mtime recent?
3. `tail -5` on log file — any errors?
4. `nvidia-smi` — is GPU actually being used?
5. `df -h` — enough disk space?

If any check fails, the watchdog logs the issue and attempts diagnosis before alerting.

## Troubleshooting

### "sshpass not found"

**Problem:** Auto-login requires sshpass.

**Solution:**
```bash
brew install hudochenkov/sshpass/sshpass
```

### "Connection refused"

**Problem:** Instance may be stopped or port changed.

**Solution:**
1. Check AutoDL web console for new port
2. Update with: `autodl add <name> --port <new-port>`

### "Conda not initialized"

**Problem:** New instance, conda not set up.

**Solution:**
```bash
autodl setup <name>
```

### "Disk >90% full"

**Problem:** Running out of space.

**Solution:**
1. Check largest dirs: `autodl disk <name>`
2. Connect and clean up
3. Common culprits:
   - Downloaded tar.gz files
   - Old experiment outputs
   - Cached pip packages

## Best Practices

### 1. GPU vs CPU Modes

**When to use CPU-only mode:**
- Data download/preprocessing
- Code development
- Environment setup
- Cost savings between training runs

**When to use GPU mode:**
- Model training
- Inference at scale
- GPU-accelerated preprocessing

**Always check mode:**
```bash
autodl status <name>
```

### 2. Disk Management

**Before large downloads:**
```bash
autodl disk <name>  # Check available space
```

**After downloads:**
```bash
# Extract and delete tar
tar -xzf data.tar.gz && rm data.tar.gz
```

**Regular cleanup:**
- Remove old checkpoints
- Clean conda cache: `conda clean --all`
- Remove unused environments

### 3. Network Acceleration

**Always enable before:**
- Large downloads
- `git clone`
- `pip install` with many packages
- Dataset downloads

```bash
source /etc/network_turbo
```

### 4. Conda Management

**Always initialize on new instances:**
```bash
autodl setup <name>
```

**Verify before use:**
```bash
autodl status <name>
# Check "Conda Status"
```

### 5. Multiple Instances

**Use descriptive names:**
- `training-gpu` vs `prep-cpu`
- `scbench-a6000` vs `qwen-rtx4090`

**Tag by purpose:**
- Store info in `--gpu`, `--cpu` fields
- Use `autodl list -v` to see all

## Integration Ideas

### 1. Heartbeat Monitoring

Add to HEARTBEAT.md:
```bash
# Check AutoDL disk space
autodl status example-project | grep "Disk Status"
```

### 2. Training Notifications

When training completes, log to memory:
```bash
autodl status example-project >> memory/daily/$(date +%Y-%m-%d).md
```

### 3. WhatsApp/Telegram Alerts

Alert on disk >90%:
```bash
DISK=$(autodl status example-project | grep "used")
if [[ $DISK =~ "9[0-9]%" ]]; then
  message send --to user "⚠️ AutoDL disk >90%"
fi
```

## Tips

1. **Check status before connecting** - Know if GPU is available
2. **Setup new instances immediately** - conda init takes 30 seconds
3. **Monitor disk proactively** - Don't wait for 100%
4. **Use turbo for large operations** - 5-10x faster downloads
5. **Store passwords securely** - Consider SSH keys

## See Also

- [references/common-issues.md](references/common-issues.md) - Troubleshooting guide
- [references/best-practices.md](references/best-practices.md) - Advanced tips
- [assets/instances.json.template](assets/instances.json.template) - Config template
