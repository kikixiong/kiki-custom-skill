#!/usr/bin/env bash
set -Eeuo pipefail

if [ "$#" -lt 5 ]; then
  cat >&2 <<'USAGE'
Usage:
  wrap_existing_run.sh <existing_sh> <run_root> <project> <run_id> <notify_env> [thresholds]

This wrapper does not edit the original shell script. It runs it, captures logs,
writes an exit code file, and starts the progress notification watcher.
USAGE
  exit 2
fi

EXISTING_SH="$1"
RUN_ROOT="$2"
PROJECT="$3"
RUN_ID="$4"
NOTIFY_ENV="$5"
THRESHOLDS="${6:-50,75,100}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${RUN_ROOT}/logs/main.log"
EXIT_CODE_FILE="${RUN_ROOT}/exit_code.txt"

mkdir -p "${RUN_ROOT}/logs" "${RUN_ROOT}/results" "${RUN_ROOT}/checkpoints" "${RUN_ROOT}/configs"

python "${SCRIPT_DIR}/send_email_notify.py" \
  --event started \
  --project "${PROJECT}" \
  --run-id "${RUN_ID}" \
  --run-root "${RUN_ROOT}" \
  --summary "Wrapped experiment started" \
  --env-file "${NOTIFY_ENV}" || true

bash "${EXISTING_SH}" 2>&1 | tee "${LOG_FILE}" &
RUN_PID=$!

python "${SCRIPT_DIR}/watch_progress_notify.py" \
  --project "${PROJECT}" \
  --run-id "${RUN_ID}" \
  --run-root "${RUN_ROOT}" \
  --log-file "${LOG_FILE}" \
  --thresholds "${THRESHOLDS}" \
  --env-file "${NOTIFY_ENV}" \
  >> "${RUN_ROOT}/logs/notify.log" 2>&1 &
WATCH_PID=$!

set +e
wait "${RUN_PID}"
EXIT_CODE=$?
set -e

echo "${EXIT_CODE}" > "${EXIT_CODE_FILE}"

python "${SCRIPT_DIR}/watch_progress_notify.py" \
  --project "${PROJECT}" \
  --run-id "${RUN_ID}" \
  --run-root "${RUN_ROOT}" \
  --log-file "${LOG_FILE}" \
  --thresholds "${THRESHOLDS}" \
  --env-file "${NOTIFY_ENV}" \
  --exit-code-file "${EXIT_CODE_FILE}" \
  --once \
  >> "${RUN_ROOT}/logs/notify.log" 2>&1 || true

kill "${WATCH_PID}" 2>/dev/null || true
exit "${EXIT_CODE}"
