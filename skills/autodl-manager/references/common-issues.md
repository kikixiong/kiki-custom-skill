# Common Issues & Solutions

Troubleshooting guide for AutoDL Manager.

## Connection Issues

### Port Changed Without Notice

**Symptoms:**
```bash
autodl connect scbenchmark
# ssh: connect to host ... port 15049: Connection refused
```

**Cause:** AutoDL reassigns ports when instances restart.

**Solution:**
1. Check AutoDL web console for new port
2. Update config:
   ```bash
   autodl add scbenchmark --host <host> --port <new-port>
   ```

**Prevention:** Always check status first:
```bash
autodl status scbenchmark
```

### Password Authentication Failed

**Symptoms:**
```bash
Permission denied (publickey,password)
```

**Causes:**
1. Password changed in AutoDL console
2. Typo when adding instance
3. Instance requires key-based auth

**Solution:**
```bash
# Update password
autodl add scbenchmark --password <new-password>

# Or use SSH keys (better)
ssh-keygen -t ed25519
# Upload ~/.ssh/id_ed25519.pub to AutoDL console
```

### sshpass Not Installed

**Symptoms:**
```bash
Error: sshpass not installed
```

**Solution:**
```bash
# macOS
brew install hudochenkov/sshpass/sshpass

# Linux (Debian/Ubuntu)
sudo apt-get install sshpass

# Linux (RHEL/CentOS)
sudo yum install sshpass
```

---

## GPU Detection Issues

### "No GPU detected" When GPU Should Exist

**Possible causes:**

#### 1. Instance in CPU-only mode
**Check:** AutoDL console - is GPU enabled?

**Solution:** Switch to GPU mode in console, restart instance.

#### 2. nvidia-smi not in PATH
**Check:**
```bash
autodl connect <name>
which nvidia-smi
# If not found:
export PATH=/usr/local/cuda/bin:$PATH
```

#### 3. Driver not loaded
**Check:**
```bash
lsmod | grep nvidia
```

**Solution:** Usually auto-fixed on reboot. Contact AutoDL support if persists.

### GPU Shows 100% Usage When Idle

**Cause:** Previous process still running.

**Check:**
```bash
nvidia-smi  # Shows process IDs
ps aux | grep python  # Find hung processes
```

**Solution:**
```bash
kill -9 <PID>
# Or force kill all Python:
pkill -9 python
```

---

## Disk Space Issues

### Sudden Disk Full (>95%)

**Common culprits:**

#### 1. Large downloaded archives
```bash
# Check for tar.gz, zip files
find /root/autodl-tmp -name "*.tar.gz" -size +1G

# Clean up after extraction
rm *.tar.gz *.zip
```

#### 2. Conda cache
```bash
# Can take several GB
conda clean --all
```

#### 3. Pip cache
```bash
pip cache purge
```

#### 4. Docker images (if using Docker)
```bash
docker system prune -a
```

#### 5. Jupyter checkpoints
```bash
find /root/autodl-tmp -name ".ipynb_checkpoints" -exec rm -rf {} +
```

### Can't Delete Files (Permission Denied)

**Cause:** Files owned by different user (rare on AutoDL).

**Solution:**
```bash
sudo rm -rf <directory>
# Or
sudo chown -R root:root <directory>
rm -rf <directory>
```

---

## Conda Issues

### "conda: command not found"

**Cause:** Conda not initialized.

**Solution:**
```bash
# Via autodl-manager
autodl setup <name>

# Or manually
conda init bash  # or zsh
source ~/.bashrc
```

### "base environment not activated"

**Cause:** Shell not configured to auto-activate base.

**Check:**
```bash
# Should see (base) in prompt
# If not:
conda activate base
```

**Fix permanently:**
```bash
conda config --set auto_activate_base true
```

### Conda environment not found

**Symptom:**
```bash
conda activate myenv
# EnvironmentNameNotFound: myenv
```

**Check:**
```bash
conda env list
```

**Solution:**
- If environment doesn't exist, create it
- If exists but not found, check conda init

---

## Network Issues

### Slow Downloads Even With Turbo

**Possible causes:**

#### 1. Turbo not actually active
**Check:**
```bash
env | grep -i turbo
# Should show turbo-related variables
```

**Fix:**
```bash
source /etc/network_turbo
```

#### 2. Source server is slow
**Example:** Downloading from HuggingFace during peak hours.

**Solution:** Try different mirrors or later time.

#### 3. Bandwidth throttling
**AutoDL may throttle after heavy usage.**

**Check:** Test speed to different servers.

### Git Clone Fails

**Symptoms:**
```bash
git clone https://...
# fatal: unable to access '...': Could not resolve host
```

**Causes:**
1. Network turbo not enabled
2. DNS issues
3. GitHub throttling

**Solutions:**
```bash
# 1. Enable turbo
source /etc/network_turbo

# 2. Try different DNS
# Edit /etc/resolv.conf (temporary)

# 3. Use git:// instead of https://
git clone git://github.com/...
```

---

## Performance Issues

### Training Much Slower Than Expected

**Diagnostics:**

#### 1. Check GPU utilization
```bash
nvidia-smi
# Should be 90-100% during training
```

If low:
- **DataLoader bottleneck:** Increase num_workers
- **CPU bottleneck:** Profile code
- **I/O bottleneck:** Use SSD, not HDD

#### 2. Check CPU usage
```bash
htop
```

If CPU at 100% but GPU low:
- Data preprocessing too slow
- Use GPU for preprocessing (torchvision transforms)

#### 3. Check disk I/O
```bash
iostat -x 1
# High %util means disk bottleneck
```

Solution:
- Load data to RAM: `--pin_memory`
- Use faster disk
- Preload dataset

### Out of Memory (OOM)

**GPU OOM:**
```bash
# Check available memory
nvidia-smi

# Reduce batch size
# Or use gradient accumulation
# Or mixed precision (fp16)
```

**CPU OOM:**
```bash
# Check RAM usage
free -h

# Reduce DataLoader workers
# Or use swap (slow)
```

---

## Conda vs System Python

### Wrong Python Version

**Symptom:**
```bash
python --version
# Python 3.8.10 (expected 3.9+)
```

**Cause:** Using system Python instead of conda.

**Check:**
```bash
which python
# Should be: /root/miniconda3/bin/python
# Not: /usr/bin/python
```

**Fix:**
```bash
conda activate base
# Or specific environment:
conda activate myenv
```

### Packages Installed in Wrong Location

**Symptom:**
```bash
pip install numpy
# Works

python
import numpy
# ModuleNotFoundError
```

**Cause:** pip installed to system Python, but using conda Python.

**Check:**
```bash
which pip
which python
# Should both be in /root/miniconda3/
```

**Fix:**
```bash
# Always use conda's pip
conda activate base
pip install numpy
```

---

## AutoDL-Specific Issues

### Instance Paused/Stopped Unexpectedly

**Cause:** Balance insufficient or manual stop.

**Check:** AutoDL console - instance status.

**Prevention:**
- Monitor balance
- Set auto-stop time carefully

### Can't Resume Training After Restart

**Cause:** State not saved properly.

**Prevention:**
```python
# Save checkpoint every N epochs
torch.save({
    'epoch': epoch,
    'model_state': model.state_dict(),
    'optimizer_state': optimizer.state_dict(),
}, 'checkpoint.pt')

# Resume:
checkpoint = torch.load('checkpoint.pt')
model.load_state_dict(checkpoint['model_state'])
optimizer.load_state_dict(checkpoint['optimizer_state'])
start_epoch = checkpoint['epoch'] + 1
```

### Data Lost After Instance Deletion

**Cause:** Data stored in temporary disk, not persistent.

**AutoDL disk types:**
- **System disk:** Ephemeral, lost on deletion
- **Data disk:** Persistent, survives deletion
- **/root/autodl-tmp/:** Usually on data disk (check console)

**Prevention:**
- Confirm disk type in AutoDL console
- Backup important results to external storage
- Use git for code

---

## Quick Fixes

### Reset Environment

**If everything is broken:**
```bash
# 1. Remove config
rm @@KIKI_AGENT_HOME@@/autodl_instances.json

# 2. Re-add instance
autodl add <name> --host <host> --port <port>

# 3. Re-setup
autodl setup <name>
```

### Force Reconnect

**If connection hangs:**
```bash
# Kill existing SSH
pkill -f "ssh.*autodl"

# Reconnect
autodl connect <name>
```

### Emergency Disk Cleanup

**If 99% full and can't delete normally:**
```bash
# 1. Find largest files
du -ah /root/autodl-tmp | sort -rh | head -20

# 2. Delete .cache dirs
rm -rf ~/.cache/*
rm -rf /root/.cache/*

# 3. Clean conda
conda clean --all --yes

# 4. Clean pip
pip cache purge

# 5. Remove old logs
find /root/autodl-tmp -name "*.log" -mtime +7 -delete
```

---

## Getting Help

If issue persists:

1. **Check status:**
   ```bash
   autodl status <name>
   ```

2. **Test basic SSH:**
   ```bash
   ssh -p <port> root@<host>
   ```

3. **Check AutoDL console:**
   - Instance status
   - Balance
   - Network status

4. **Contact AutoDL support:**
   - Web console support
   - WeChat support group

5. **Check local skill files:**
   - `@@KIKI_SKILLS_DIR@@/autodl-manager/SKILL.md`
   - `@@KIKI_SKILLS_DIR@@/autodl-manager/scripts/autodl_cli.py`
