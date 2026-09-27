#!/usr/bin/env python3
"""Watch experiment progress and send de-duplicated email alerts."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path


FAILURE_PATTERNS = [
    re.compile(r"Traceback \(most recent call last\)"),
    re.compile(r"CUDA out of memory", re.IGNORECASE),
    re.compile(r"\bKilled\b"),
    re.compile(r"\bRuntimeError\b"),
    re.compile(r"\bException\b"),
    re.compile(r"\bERROR\b"),
]


def read_text(path: str | None) -> str:
    if not path:
        return ""
    file_path = Path(path)
    if not file_path.exists():
        return ""
    return file_path.read_text(encoding="utf-8", errors="replace")


def tail(text: str, lines: int) -> str:
    return "\n".join(text.splitlines()[-lines:])


def parse_thresholds(value: str) -> list[float]:
    thresholds: list[float] = []
    for part in value.split(","):
        part = part.strip().rstrip("%")
        if not part:
            continue
        number = float(part)
        if 0 <= number <= 100:
            thresholds.append(number)
    return sorted(set(thresholds))


def parse_progress_from_text(text: str) -> float | None:
    candidates: list[float] = []

    for match in re.finditer(r"(?<![\d.])(\d{1,3}(?:\.\d+)?)\s*%", text):
        value = float(match.group(1))
        if 0 <= value <= 100:
            candidates.append(value)

    ratio_patterns = [
        r"(?i)\bepoch\s*[:=]?\s*(\d+)\s*/\s*(\d+)",
        r"(?i)\bstep\s*[:=]?\s*(\d+)\s*/\s*(\d+)",
        r"(?i)\biter(?:ation)?\s*[:=]?\s*(\d+)\s*/\s*(\d+)",
    ]
    for pattern in ratio_patterns:
        for match in re.finditer(pattern, text):
            current = int(match.group(1))
            total = int(match.group(2))
            if total > 0:
                candidates.append(min(100.0, max(0.0, current / total * 100.0)))

    if not candidates:
        return None
    return max(candidates)


def parse_progress(progress_file: str | None, log_text: str) -> float | None:
    progress_text = read_text(progress_file)
    if progress_text:
        progress = parse_progress_from_text(progress_text)
        if progress is not None:
            return progress
    return parse_progress_from_text(log_text)


def detect_failure(log_text: str, exit_code_file: str | None) -> tuple[bool, str]:
    if exit_code_file:
        path = Path(exit_code_file)
        if path.exists():
            raw = path.read_text(encoding="utf-8", errors="replace").strip()
            if raw:
                try:
                    code = int(raw)
                except ValueError:
                    code = 1
                if code != 0:
                    return True, f"exit_code={code}"
                return False, "exit_code=0"

    latest = tail(log_text, 120)
    for pattern in FAILURE_PATTERNS:
        if pattern.search(latest):
            return True, f"log pattern: {pattern.pattern}"
    return False, ""


def load_state(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"sent": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"sent": []}


def save_state(path: Path, state: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def state_path(args: argparse.Namespace) -> Path:
    if args.state_file:
        return Path(args.state_file)
    if args.run_root:
        return Path(args.run_root) / "notify_state.json"
    if args.log_file:
        return Path(args.log_file).parent / "notify_state.json"
    return Path("notify_state.json")


def send_alert(args: argparse.Namespace, event: str, progress: float | None, summary: str) -> None:
    script = Path(__file__).with_name("send_email_notify.py")
    command = [
        sys.executable,
        str(script),
        "--event",
        event,
        "--project",
        args.project,
        "--run-id",
        args.run_id,
        "--summary",
        summary,
    ]
    if progress is not None:
        command += ["--progress", f"{progress:g}"]
    if args.run_root:
        command += ["--run-root", args.run_root]
    if args.log_file:
        command += ["--log-file", args.log_file]
    if args.env_file:
        command += ["--env-file", args.env_file]
    if args.dry_run:
        command.append("--dry-run")

    subprocess.run(command, check=False)


def check_once(args: argparse.Namespace) -> None:
    path = state_path(args)
    state = load_state(path)
    sent = set(state.get("sent", []))

    log_text = read_text(args.log_file)
    progress = parse_progress(args.progress_file, log_text)
    failed, reason = detect_failure(log_text, args.exit_code_file)

    if failed and "failed" not in sent:
        send_alert(args, "failed", progress, f"Experiment failure detected: {reason}")
        sent.add("failed")
        state["sent"] = sorted(sent)
        state["last_progress"] = progress
        state["updated_at"] = int(time.time())
        save_state(path, state)
        print(f"state={path} progress={progress} sent={','.join(sorted(sent))}")
        return

    thresholds = parse_thresholds(args.thresholds)
    if progress is not None:
        for threshold in thresholds:
            key = f"progress_{threshold:g}"
            if progress >= threshold and key not in sent:
                event = f"progress_{int(threshold)}" if threshold.is_integer() else "progress"
                send_alert(args, event, progress, f"Progress reached {progress:.1f}%")
                sent.add(key)

    if args.exit_code_file:
        exit_path = Path(args.exit_code_file)
        if exit_path.exists():
            raw = exit_path.read_text(encoding="utf-8", errors="replace").strip()
            if raw == "0" and "success" not in sent:
                send_alert(args, "success", progress if progress is not None else 100.0, "Experiment completed successfully")
                sent.add("success")

    state["sent"] = sorted(sent)
    state["last_progress"] = progress
    state["updated_at"] = int(time.time())
    save_state(path, state)
    print(f"state={path} progress={progress} sent={','.join(sorted(sent))}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--run-root", default="")
    parser.add_argument("--log-file", default="")
    parser.add_argument("--progress-file", default="")
    parser.add_argument("--exit-code-file", default="")
    parser.add_argument("--state-file", default="")
    parser.add_argument("--thresholds", default="50,75,100")
    parser.add_argument("--interval", type=int, default=60)
    parser.add_argument("--env-file", default="")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    while True:
        check_once(args)
        if args.once:
            break
        time.sleep(max(5, args.interval))


if __name__ == "__main__":
    main()
