# AutoDL Experiment Reference

## Official Docs

- Academic resource acceleration: https://www.autodl.com/docs/network_turbo/
- Background execution: https://www.autodl.com/docs/daemon/
- Upload data: https://www.autodl.com/docs/scp/
- Download data: https://www.autodl.com/docs/down/
- System disk space FAQ: https://www.autodl.com/docs/qa1/

## Preflight Command Block

```bash
set -e
echo "== GPU ==" && nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv,noheader
echo "== Disk ==" && (df -h / /root/autodl-tmp 2>/dev/null || df -h)
echo "== Python =="
source /root/miniconda3/etc/profile.d/conda.sh
conda activate "${CONDA_ENV:-base}"
which python
python -V
python - <<'PY'
import importlib.util
for name in ["torch", "transformers", "cv2", "sklearn", "pandas", "tqdm"]:
    print(name, "OK" if importlib.util.find_spec(name) else "MISSING")
PY
echo "== tmux/screen ==" && (tmux -V || screen -v || true)
```

## Transfer Rules

Use uppercase `-P` for `scp` ports and run `scp` from the local machine.

```bash
scp -rP <PORT> root@<HOST>:<RUN_ROOT>/results <LOCAL_PULL_DIR>
scp -rP <PORT> root@<HOST>:<RUN_ROOT>/logs <LOCAL_PULL_DIR>
```

For many small files, prefer tar streaming.

## Troubleshooting Table

| Symptom | Likely Cause | Fix |
|---|---|---|
| `python: command not found` | Non-login shell without conda | `source /root/miniconda3/etc/profile.d/conda.sh && conda activate <env>` |
| HuggingFace unreachable | Proxy not active in tmux | Put `source /etc/network_turbo` inside the launch script |
| Model weights redownload | Cache env missing | Export `HF_HOME`, `HUGGINGFACE_HUB_CACHE`, `TRANSFORMERS_CACHE` |
| GPU memory low, speed low | CPU/video/data bottleneck | Inspect data loader, cache, decoding and preprocessing |
| Full tqdm floods chat | Raw carriage-return logs | Parse progress or tail filtered lines |
| Mail not sent | SMTP app password missing or blocked | Test `send_email_notify.py --dry-run`, then verify SMTP host/port/TLS |
| Duplicate alerts | State file lost | Keep `<RUN_ROOT>/notify_state.json` with run artifacts |
