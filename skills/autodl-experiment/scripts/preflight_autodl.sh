#!/usr/bin/env bash
set -euo pipefail

CONDA_ENV="${CONDA_ENV:-base}"

echo "== GPU =="
nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv,noheader || true

echo "== Disk =="
(df -h / /root/autodl-tmp 2>/dev/null || df -h) || true

echo "== Python =="
if [ -f /root/miniconda3/etc/profile.d/conda.sh ]; then
  # shellcheck disable=SC1091
  source /root/miniconda3/etc/profile.d/conda.sh
  conda activate "${CONDA_ENV}" || true
fi
which python || true
python -V || true

echo "== Packages =="
python - <<'PY' || true
import importlib.util
for name in ["torch", "transformers", "cv2", "sklearn", "pandas", "tqdm"]:
    print(name, "OK" if importlib.util.find_spec(name) else "MISSING")
PY

echo "== Background runner =="
(tmux -V || screen -v || true)

echo "== Proxy =="
env | grep -i proxy || true
