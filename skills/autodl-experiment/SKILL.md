---
name: autodl-experiment
description: Launch, monitor, troubleshoot, notify, and archive AutoDL or SeetaCloud SSH GPU experiments. Use for remote training/evaluation jobs, tmux/screen launches, conda/CUDA/HuggingFace setup, SMTP email progress alerts, failure alerts, result pullback, and append-only runbook notes. Do not use for local-only debugging unless a remote SSH GPU instance is involved.
disable-model-invocation: true
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# AutoDL Experiment

这是一个面向 AutoDL/SeetaCloud 风格 SSH GPU 实例的远程实验工作流 skill。它的目标不是给出一套死脚本，而是让 Codex 像实验助理一样：先判断任务类型，补齐关键配置，再安全地启动、监控、通知、拉回结果和沉淀 runbook。

## Core Rule

优先从用户上下文、项目文件、已有 `run.sh`、日志和 `docs/AUTODL_EXPERIMENT_RUNBOOK.md` 推断配置。只询问无法可靠推断、且会影响执行或安全的字段。

每次最多先问 3 个最高优先级问题。不要一次性把所有配置项丢给用户。

永远不要把 SSH 密码、SMTP 授权码、API token、HF token、私钥、私有数据链接写入：

- `SKILL.md`
- `LAUNCH_INFO.md`
- `AUTODL_EXPERIMENT_RUNBOOK.md`
- 日志摘要
- GitHub README / issue / PR

## Task Router

先判断用户真正要做哪类事：

- 启动新实验：生成或更新 `run.sh`，预检环境，放进 `tmux`/`screen`。
- 监控已有实验：只读取 session、日志、GPU、磁盘和 artifacts。
- 给正在跑的任务加通知：旁路监听日志，不杀进程、不改原进程。
- 给已有 `.sh` 加通知：生成 wrapper，默认不覆盖原脚本。
- 拉回结果：优先拉回 CSV/JSON/MD/log/config/script，小心大 checkpoint。
- 排查失败：先保全日志和结果，再定位环境、网络、缓存、显存、磁盘问题。
- 整理复盘：追加事实型 runbook，不写敏感信息。

## Information Collection

如果缺信息，按这个优先级询问。

远程连接：

- `REMOTE_HOST`
- `REMOTE_PORT`
- `REMOTE_USER`，通常是 `root`
- 认证方式：SSH key、已有 SSH config、交互式密码

实验入口：

- 启动命令或已有远程 `.sh` 路径
- `PROJECT_NAME`
- `RUN_ID`
- `CONDA_ENV`
- `REMOTE_ROOT`，默认 `/root/autodl-tmp/<project>`
- `OUTPUT_DIR`

进度来源：

- 日志中的百分比，如 `50%`
- `epoch x/y` 或 `step x/y`
- 训练脚本写出的 progress file
- artifacts 数量或阶段 marker
- 如果都没有，退化为 started / heartbeat / success / failed 通知

邮件通知：

- 是否启用邮件通知
- 邮箱服务商：QQ、Gmail、Outlook、其他 SMTP
- 收件人
- 通知节点：默认 `50,75,100,failed`
- 授权码注入方式：远程环境变量或未提交的 `.env`

## Remote Layout

除非项目已有约定，使用：

```text
/root/autodl-tmp/<project>/
  data/
  cache/
  runs/<run_id>/
    run.sh
    LAUNCH_INFO.md
    notify_state.json
    logs/
      main.log
      notify.log
    results/
    checkpoints/
    configs/
```

HuggingFace 缓存默认放到数据盘：

```bash
export HF_HOME=/root/autodl-tmp/cache/huggingface
export HUGGINGFACE_HUB_CACHE=/root/autodl-tmp/cache/huggingface/hub
export TRANSFORMERS_CACHE=/root/autodl-tmp/cache/huggingface/hub
```

## Preflight

启动或排错前先做远程预检：

```bash
bash scripts/preflight_autodl.sh
```

至少检查 GPU、磁盘、Python、conda、关键包、`tmux`/`screen`。如果脚本还没上传到远程，读取 `references/autodl-reference.md` 里的预检命令块。

## Launch Rules

长任务不要直接绑在 SSH 前台。优先使用 `tmux`，没有 `tmux` 时使用 `screen`。

如果用户已有 `.sh`：

- 不要直接覆盖原脚本。
- 生成 wrapper 或新的 `run_with_notify.sh`。
- wrapper 负责日志、退出码、通知和 artifacts 路径。

如果用户要新建实验：

- 用 `assets/run.sh.template` 渲染标准启动脚本。
- 生成 `<RUN_ROOT>/LAUNCH_INFO.md`。
- 将 stdout/stderr 写入 `<RUN_ROOT>/logs/main.log`。

## Email Notification

通知能力必须是可配置的，不要假设固定进度格式。

默认通知策略：

- 50%
- 75%
- 100% 或成功完成
- 失败

可按用户要求改成：

- `25,50,75,100`
- `10,30,60,90,100`
- 只通知失败和完成
- 启动、心跳、失败、完成

使用脚本：

```bash
python scripts/watch_progress_notify.py \
  --project "<project>" \
  --run-id "<run_id>" \
  --run-root "<RUN_ROOT>" \
  --log-file "<RUN_ROOT>/logs/main.log" \
  --thresholds "50,75,100" \
  --env-file "<RUN_ROOT>/notify.env"
```

邮件发送脚本：

```bash
python scripts/send_email_notify.py \
  --event progress_75 \
  --project "<project>" \
  --run-id "<run_id>" \
  --progress 75 \
  --summary "Validation reached 75%" \
  --env-file "<RUN_ROOT>/notify.env"
```

配置模板见 `assets/notify.env.example`。真实 SMTP 授权码只放远程环境变量或未提交的 `.env` 文件。

## Monitoring Response

报告进度时保持简洁，不要整段粘贴 tqdm：

```text
Run:
Session:
Remote path:
GPU:
Disk:
Progress:
Latest signal:
Artifacts:
Notification:
Risk:
Next command:
```

## Pullback

结果出现就尽早拉回，不要等服务器释放前最后一分钟。

优先拉回：

- `run.sh`
- `LAUNCH_INFO.md`
- `logs/`
- `results/*.csv`
- `results/*.json`
- `results/*.md`
- configs
- figures
- 小型 checkpoints

`scp` 端口参数使用大写 `-P`，并在本地机器执行。

## Runbook

遇到可复用问题后追加：

```bash
python scripts/append_autodl_note.py \
  --event "HF download failed in tmux" \
  --problem "tmux did not inherit acceleration/cache variables" \
  --cause "launch script lacked network_turbo and HF cache exports" \
  --fix "moved exports into run.sh" \
  --evidence "weights loaded from /root/autodl-tmp/cache"
```

## Safety Guardrails

执行以下操作前必须明确确认：

- `rm -rf`
- 重置系统盘或数据盘
- 覆盖已有 run 目录
- kill 所有 Python 进程
- 删除 checkpoints 或 results
- 上传日志到公开仓库
- 在命令行明文传密码或授权码

如果必须使用 SSH 密码，让用户在安全交互提示里输入；不要把密码写进命令、脚本或文件。

## Definition of Done

一次远程实验任务完成时，应该至少具备：

- 远程预检结果已记录或摘要说明。
- 长任务运行在 `tmux`/`screen` 或安全 wrapper 中。
- `run.sh`、`LAUNCH_INFO.md`、日志路径和结果路径明确。
- 邮件通知配置已按用户选择启用、跳过或 dry-run 验证。
- 结果 artifacts 可发现，重要结果已拉回或给出精确拉回命令。
- 可复用问题已追加到 runbook。
- 最终回复包含 run id、远程路径、session、状态、通知策略、结果文件和下一条检查命令。

## References

- AutoDL 命令细节和排错表：`references/autodl-reference.md`
- 英文镜像说明：`references/SKILL.en.md`
- 通知配置模板：`assets/notify.env.example`
- 标准启动模板：`assets/run.sh.template`
