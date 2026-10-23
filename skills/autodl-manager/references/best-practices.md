# Best Practices

Advanced tips for AutoDL workflow optimization.

## Instance Management

### Naming Convention

**Good names:**
```
training-rtx4090    # Purpose + GPU type
prep-cpu            # Purpose + mode
scbench-a6000       # Project + GPU
qwen-inference      # Model + task
```

**Bad names:**
```
instance1           # Not descriptive
test                # Too vague
my-server           # Doesn't tell purpose
```

### Multi-Instance Strategy

**Typical setup:**

| Instance | Purpose | Mode | When to Use |
|----------|---------|------|-------------|
| prep-cpu | Data prep | CPU-only | Download, preprocess |
| train-gpu1 | Main training | 2x RTX4090 | Model training |
| train-gpu2 | Experiments | 1x A6000 | Hyperparameter search |
| infer-gpu | Inference | 1x RTX4090 | Model serving |

**Why multiple instances:**
- Save cost: Use CPU for prep, GPU only for training
- Parallel work: Train on one, prep data on another
- Redundancy: Backup if one instance fails

### Cost Optimization

**1. Use CPU-only for non-GPU tasks**

```bash
# Check if you really need GPU
autodl status <name>

# If "No GPU detected" but you're just downloading:
# This is good! Saving money.
```

**Tasks that don't need GPU:**
- Data download
- File extraction
- Code development
- Environment setup
- Data preprocessing (unless GPU-accelerated)

**2. Stop instances when not in use**

Don't leave instances running overnight if not training.

**3. Use appropriate GPU models**

| Task | GPU Needed | Cost |
|------|-----------|------|
| BERT fine-tuning | RTX4090 x1 | $$ |
| GPT training | A100 x2 | $$$$ |
| Inference | T4 x1 | $ |
| Data prep | None | $ |

**4. Monitor disk usage**

Storage costs money too:
```bash
# Regular cleanup
autodl disk <name>
```

---

## Disk Management

### Before Large Downloads

**Always check space first:**
```bash
autodl disk <name>
# Need >20% free for safety
```

**Estimate download size:**
- Check source (GitHub releases, HuggingFace repo info)
- Allow 2x size for extraction
- Example: 10GB tar.gz → need 20GB free

### Download Strategy

**1. Use network turbo**

```bash
autodl connect <name>
source /etc/network_turbo

# Then download
git clone https://...
pip install -r requirements.txt
```

**Speed improvements:**
- git clone: 5-10x faster
- pip install: 3-5x faster
- wget: 3-5x faster

**2. Incremental downloads**

For large datasets:
```bash
# Instead of downloading 100GB at once:
# Download in parts
wget https://.../part1.tar.gz
tar -xzf part1.tar.gz && rm part1.tar.gz
wget https://.../part2.tar.gz
tar -xzf part2.tar.gz && rm part2.tar.gz
```

**3. Verify checksums**

```bash
# Avoid corrupted downloads
md5sum file.tar.gz
# Compare with source MD5
```

### Cleanup Routine

**Daily:**
```bash
# Remove temporary files
rm -rf /tmp/*
rm -rf ~/.cache/pip/*
```

**Weekly:**
```bash
# Clean conda
conda clean --all

# Remove old checkpoints
find /root/autodl-tmp -name "checkpoint_*.pt" -mtime +7 -delete

# Remove logs
find /root/autodl-tmp -name "*.log" -mtime +14 -delete
```

**After each experiment:**
```bash
# Archive results
tar -czf experiment_results.tar.gz results/
# Upload to external storage
# Then delete original
rm -rf results/
```

### Disk Space Monitoring

**Set up alerts:**
```bash
# In HEARTBEAT.md or cron:
autodl disk <name> | grep -E "9[0-9]%|100%"
# If match, send alert
```

---

## Conda Best Practices

### Environment Strategy

**1. Separate environments per project**

```bash
# Don't use base for everything
conda create -n scbench python=3.9
conda create -n qwen python=3.10
```

**2. Export environment specs**

```bash
# Save environment
conda env export > environment.yml

# Recreate on new instance
conda env create -f environment.yml
```

**3. Use conda-pack for migration**

```bash
# Pack environment
conda install conda-pack
conda pack -n myenv -o myenv.tar.gz

# On new instance
mkdir -p /root/miniconda3/envs/myenv
tar -xzf myenv.tar.gz -C /root/miniconda3/envs/myenv
conda activate myenv
```

### Initialization Best Practices

**Always check on new instances:**
```bash
autodl setup <name>
```

**Verify before heavy work:**
```bash
autodl status <name>
# Check "Conda Status"
```

**Use correct shell:**
- AutoDL default: bash
- If you use zsh: `conda init zsh`

---

## Training Workflow

### Setup Checklist

Before starting training on new instance:

```bash
# 1. Check status
autodl status example-project
# ✅ GPU available
# ✅ Disk <80%
# ✅ Conda initialized

# 2. Connect
autodl connect example-project

# 3. Enable turbo (for pip install)
source /etc/network_turbo

# 4. Setup environment
conda activate myenv
pip install -r requirements.txt

# 5. Verify GPU
nvidia-smi

# 6. Start training
python train.py
```

### Long-Running Training

**1. Use screen or tmux**

```bash
# So training continues if disconnected
screen -S training
python train.py
# Ctrl+A, D to detach

# Reattach later
screen -r training
```

**2. Save checkpoints frequently**

```python
# Every N epochs
if epoch % 5 == 0:
    torch.save({
        'epoch': epoch,
        'model': model.state_dict(),
        'optimizer': optimizer.state_dict(),
        'loss': loss,
    }, f'checkpoint_epoch_{epoch}.pt')
```

**3. Log everything**

```python
import logging

logging.basicConfig(
    filename='training.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# In training loop
logging.info(f'Epoch {epoch}, Loss: {loss:.4f}')
```

**4. Monitor remotely**

```bash
# From local machine
watch -n 60 'autodl disk example-project'

# Or set up notifications
# (see Integration section)
```

### Result Management

**After training:**

```bash
# 1. Save final model
torch.save(model.state_dict(), 'final_model.pt')

# 2. Generate report
python evaluate.py > results.txt

# 3. Archive everything
tar -czf experiment_$(date +%Y%m%d).tar.gz \
    final_model.pt results.txt logs/ checkpoints/

# 4. Download to local
# (from local machine)
scp -P <port> root@<host>:experiment_*.tar.gz .

# 5. Clean up instance
rm -rf checkpoints/
rm -rf logs/
```

---

## Data Management

### Dataset Organization

**Recommended structure:**
```
/root/autodl-tmp/
├── datasets/           # Raw datasets
│   ├── scbench/
│   └── imagenet/
├── processed/          # Processed data
│   ├── scbench_train.pt
│   └── scbench_val.pt
├── models/             # Model checkpoints
│   └── scbench/
├── results/            # Experiment outputs
│   └── exp_20260318/
└── scripts/            # Code
    └── train.py
```

**Benefits:**
- Clear separation
- Easy to clean up
- Easy to backup

### Data Download Best Practices

**1. Use persistent storage**

Verify `/root/autodl-tmp` is on data disk (persistent).

**2. Resume capability**

```bash
# For large downloads, use wget -c or curl -C -
wget -c https://.../large_dataset.tar.gz

# If interrupted, restart with -c to continue
```

**3. Verify before extraction**

```bash
# Check archive integrity
tar -tzf dataset.tar.gz > /dev/null
# If no errors, safe to extract and delete
```

**4. Stream processing**

For huge files:
```bash
# Extract without saving archive
wget -O - https://.../data.tar.gz | tar -xz
```

---

## GPU Management

### GPU Selection

**For multi-GPU instances:**

```bash
# Check GPU status
autodl status <name>

# Use specific GPU
CUDA_VISIBLE_DEVICES=0 python train.py

# Use all GPUs
CUDA_VISIBLE_DEVICES=0,1 python train.py
```

### GPU Monitoring

**During training:**

```bash
# Watch GPU usage
watch -n 5 nvidia-smi

# Or in Python
import GPUtil
GPUtil.showUtilization()
```

**Optimal utilization:**
- GPU usage: 90-100%
- Memory usage: 80-95% (leave some buffer)

### GPU Troubleshooting

**If GPU underutilized (<50%):**
1. Check DataLoader bottleneck
2. Increase batch size
3. Use mixed precision (fp16)
4. Profile code

**If GPU OOM:**
1. Reduce batch size
2. Use gradient accumulation
3. Use gradient checkpointing
4. Use mixed precision

---

## Network Optimization

### When to Use Turbo

**Always enable for:**
- Large downloads (>100MB)
- `git clone` of big repos
- `pip install` with many packages
- Dataset downloads

**How to enable:**
```bash
source /etc/network_turbo
```

**Verify it's active:**
```bash
autodl status <name>
# Should show: Network turbo active
```

### Download Strategies

**1. Parallel downloads**

For multiple files:
```bash
# Use xargs with parallel
cat file_list.txt | xargs -n 1 -P 4 wget
# Downloads 4 files at once
```

**2. Use mirrors**

- PyPI: Use Aliyun mirror
- GitHub: Use mirror.ghproxy.com
- HuggingFace: Use hf-mirror.com

**3. Optimize git clone**

```bash
# Shallow clone (faster)
git clone --depth 1 https://...

# Single branch
git clone --single-branch --branch main https://...
```

---

## Security & Access

### Password Management

**Current:** Stored in plaintext in `@@KIKI_AGENT_HOME@@/autodl_instances.json`

**Better options:**

**1. SSH keys (recommended)**

```bash
# Generate key
ssh-keygen -t ed25519 -C "autodl@codex"

# Upload ~/.ssh/id_ed25519.pub to AutoDL console
# Then connect without password
ssh -p <port> root@<host>
```

**2. System keychain (future)**

Store passwords in macOS Keychain or Linux keyring.

### Access Control

**If sharing instance with others:**

1. Create separate user accounts
2. Use sudo for privileged operations
3. Don't share root password

---

## Integration & Automation

### With Memory System

**Log instance usage:**

```bash
# In daily entry
autodl status example-project >> memory/daily/$(date +%Y-%m-%d).md
```

### With Notifications

**Disk space alerts:**

```bash
# In cron or HEARTBEAT.md
DISK=$(autodl status example-project | grep "used" | grep -oE "[0-9]+%")
if [[ ${DISK%\%} -gt 85 ]]; then
    message send --to telegram "⚠️ AutoDL disk ${DISK}"
fi
```

**Training completion:**

```python
# In training script
import subprocess

def send_notification(message):
    subprocess.run([
        'message', 'send',
        '--to', 'telegram',
        '--message', message
    ])

# After training
send_notification(f'Training complete! Final loss: {loss:.4f}')
```

### With Cron

**Periodic status checks:**

```bash
# Every 2 hours, check disk
0 */2 * * * autodl disk example-project | grep -E "9[0-9]%|100%" && notify_user
```

---

## Quick Reference

### Essential Commands

```bash
# First time setup
autodl add <name> --host <host> --port <port>
autodl setup <name>

# Daily usage
autodl status <name>
autodl connect <name>

# Monitoring
autodl disk <name>

# Inside instance
source /etc/network_turbo
nvidia-smi
df -h
```

### Workflow Template

```bash
# 1. Check status
autodl status training-gpu

# 2. Connect if ready
autodl connect training-gpu

# 3. Enable turbo
source /etc/network_turbo

# 4. Activate environment
conda activate myenv

# 5. Check GPU
nvidia-smi

# 6. Start work
screen -S exp1
python train.py

# 7. Detach
# Ctrl+A, D

# 8. Monitor from local
watch -n 300 'autodl disk training-gpu'
```

---

## Lessons Learned (from real usage)

### 1. Disk Space Management

**Problem:** Downloaded 10GB archive, disk jumped from 76% to 91%.

**Lesson:**
- Always check space before download
- Delete archives after extraction
- Monitor disk proactively

### 2. Port Changes

**Problem:** SSH port changed from `<OLD_SSH_PORT>` to `<NEW_SSH_PORT>` without notice.

**Lesson:**
- Verify port in AutoDL console when connection fails
- Update config immediately
- Check status before connecting

### 3. Conda Initialization

**Problem:** New instance, conda commands not found.

**Lesson:**
- Always run `autodl setup <name>` on new instances
- Verify with `autodl status <name>`
- Don't assume conda is ready

### 4. Network Acceleration

**Problem:** Slow downloads, forgot to enable turbo.

**Lesson:**
- Enable turbo before any large operation
- Verify with `autodl status <name>`
- Make it a habit

### 5. GPU Mode Detection

**Problem:** Connected, no GPU, forgot it was in CPU mode.

**Lesson:**
- Check status first: `autodl status <name>`
- Know your instance mode
- Use correct instance for the task

---

## Advanced Tips

### 1. Custom aliases

```bash
# Add to ~/.bashrc on AutoDL instance
alias turbo='source /etc/network_turbo && echo "Turbo enabled"'
alias gpu='watch -n 5 nvidia-smi'
alias disk='df -h /root/autodl-tmp'
```

### 2. Auto-enable turbo

```bash
# Add to ~/.bashrc
if [ -f /etc/network_turbo ]; then
    source /etc/network_turbo
fi
```

### 3. Git config for speed

```bash
# On AutoDL instance
git config --global core.compression 0
git config --global http.postBuffer 524288000
```

### 4. Persistent screen sessions

```bash
# Create named sessions for different tasks
screen -S download
screen -S training
screen -S monitoring

# List sessions
screen -ls

# Reattach to specific session
screen -r training
```

---

## Summary Checklist

**Before starting work:**
- [ ] Check instance status
- [ ] Verify GPU availability
- [ ] Check disk space (>20% free)
- [ ] Verify conda initialized
- [ ] Enable network turbo

**During work:**
- [ ] Use screen/tmux for long tasks
- [ ] Save checkpoints frequently
- [ ] Monitor disk usage
- [ ] Log everything

**After completion:**
- [ ] Archive results
- [ ] Download important files
- [ ] Clean up temporary files
- [ ] Stop instance if not needed

**Regular maintenance:**
- [ ] Weekly conda clean
- [ ] Remove old checkpoints
- [ ] Update instance configs
- [ ] Check for port changes
