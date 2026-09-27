#!/usr/bin/env bash
set -euo pipefail

RUN_ROOT="${1:-}"
if [ -z "${RUN_ROOT}" ]; then
  echo "Usage: monitor_run.sh <RUN_ROOT>" >&2
  exit 2
fi

LOG_FILE="${RUN_ROOT}/logs/main.log"

echo "== Sessions =="
tmux ls 2>/dev/null || screen -ls 2>/dev/null || true

echo "== GPU =="
nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv,noheader || true

echo "== Disk =="
(df -h / /root/autodl-tmp 2>/dev/null || df -h) || true

echo "== Latest log =="
tail -80 "${LOG_FILE}" 2>/dev/null || true

echo "== Artifacts =="
"$(dirname "$0")/find_artifacts.sh" "${RUN_ROOT}" || true

echo "== Notify state =="
cat "${RUN_ROOT}/notify_state.json" 2>/dev/null || true
