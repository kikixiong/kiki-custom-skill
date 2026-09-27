# AutoDL Experiment Runner

![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?style=flat-square)
![AutoDL Workflow](https://img.shields.io/badge/AutoDL-Workflow-2563EB?style=flat-square)
![Email Alerts](https://img.shields.io/badge/Email-Alerts-16A34A?style=flat-square)
![Bilingual](https://img.shields.io/badge/Docs-ZH%20%2F%20EN-F59E0B?style=flat-square)
![Security Aware](https://img.shields.io/badge/Security-Secret%20Aware-DC2626?style=flat-square)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)

一个面向 AutoDL / SeetaCloud SSH GPU 实例的 Codex Skill，用来把远程实验从“临时手搓命令”升级成可启动、可监控、可通知、可拉回、可复盘的工作流。

它适合这些场景：

- 在 AutoDL 上后台启动训练、评估、特征提取或批量推理任务；
- 自动整理数据盘、缓存、日志、结果和 checkpoint 路径；
- 用 `tmux` / `screen` 避免 SSH 断开导致任务丢失；
- 在 50%、75%、100% 或失败时发邮件提醒；
- 给已经跑起来的任务增加旁路日志监听，不重启实验；
- 把结果、日志、启动脚本和复盘经验拉回并记录。

[English README](README.en.md)

## 安装

推荐直接克隆到 Codex skills 目录：

```powershell
git clone https://github.com/handsomeZR-netizen/autodl-experiment-skill "$env:USERPROFILE\.codex\skills\autodl-experiment"
```

或者放到项目级目录：

```powershell
git clone https://github.com/handsomeZR-netizen/autodl-experiment-skill .codex\skills\autodl-experiment
```

## 使用示例

```text
Use $autodl-experiment to launch my training job on AutoDL.
Ask me for any missing SSH, conda, run.sh, and email alert settings.
Notify me at 50%, 75%, 100%, and when the job fails.
```

中文也可以：

```text
用 $autodl-experiment 帮我在 AutoDL 上跑这个实验。
远程 SSH、运行脚本、conda 环境、邮件通知缺什么你先问我。
进度到 50%、75%、100% 和失败时发邮件提醒我。
```

## 交互式配置

这个 skill 不假设你的实验格式固定。它会先尽量从项目和上下文推断，再询问关键缺失项：

- 远程连接：host、port、user、SSH key 或交互式密码；
- 实验入口：已有远程 `.sh`，或需要生成新的 `run.sh`；
- 进度来源：百分比日志、epoch/step、progress file、artifact marker；
- 通知策略：QQ 邮箱、Gmail、Outlook、其他 SMTP；
- 通知节点：默认 `50,75,100,failed`，也可自定义。

## 邮件通知

复制配置模板到远程 run 目录，并只在远程填真实授权码：

```bash
cp assets/notify.env.example /root/autodl-tmp/<project>/runs/<run_id>/notify.env
chmod 600 /root/autodl-tmp/<project>/runs/<run_id>/notify.env
```

支持 QQ 邮箱、Gmail 和通用 SMTP。真实 SMTP 授权码不要提交到 GitHub，不要写入 runbook，不要发到聊天里。

## 安全设计

- 不保存 SSH 密码、邮箱授权码、HF token、API key 或私钥；
- 不默认覆盖用户已有 `.sh`；
- 正在跑的任务默认只做旁路监控，不杀进程、不重启；
- 结果出现后尽早拉回，降低服务器释放前丢结果的风险；
- 内置 secret scan 建议和日志脱敏规则。

## 目录结构

```text
autodl-experiment-skill/
  SKILL.md
  agents/openai.yaml
  assets/
  references/
  scripts/
  evals/
```

## License

MIT
