# Kiki Custom Skill

面向 Codex 和 Claude Code 的可移植技能集合，包含 **200 个可安装技能**及其脚本、模板和共享资源。不同机器使用各自的用户目录、工具和项目配置；仓库不预设服务器、GPU、账号、实验路径或个人执行偏好。

[GitHub 仓库](https://github.com/kikixiong/kiki-custom-skill) · [技能目录](CATALOG.md) · [Codex 安装说明](INSTALL_CODEX.md) · [Claude Code 安装说明](INSTALL_CLAUDE_CODE.md)

## 一句话安装与配置

把下面这句话发给当前使用的 Codex 或 Claude Code：

> 请帮我安装并配置 https://github.com/kikixiong/kiki-custom-skill：先阅读仓库 README 和当前客户端的安装说明，识别本机用户目录及已有配置，用安装器完成安装并备份同名技能；从我的项目约定中读取需要的运行环境，缺少必要信息时集中询问我，主机、路径和执行偏好只保存到本机配置，不写回仓库，不复制凭据、不启动实验，最后告诉我安装位置和启用方法。

需要个性化时，可在同一句话后补充“远程主机用 `<SSH 别名>`，项目目录为 `<项目路径>`，运行环境为 `<环境名称>`，执行限制为 `<你的要求>`”。这些只是待填写字段；不使用远程实验时无需提供。安装器本身不连接远程主机。

机器专属约定保存到当前客户端 home 下的 `skill-config/kiki-custom-skill/environment.md`，或现有项目的本地配置。该文件不随仓库分发，也不会被安装器覆盖。只记录必要的别名、路径和偏好，凭据继续由原有凭据管理方式保管。已有用户和项目指令优先，不为安装本仓库重写全局规则。

## 安装位置

| 客户端 | 默认技能目录 | 共享资源目录 |
|---|---|---|
| Codex | `~/.codex/skills/` | `~/.codex/skill-support/kiki-custom-skill/` |
| Claude Code | `~/.claude/skills/` | `~/.claude/skill-support/kiki-custom-skill/` |

`~` 始终表示当前机器的当前用户。Codex 的 `CODEX_HOME`、Claude Code 的 `CLAUDE_CONFIG_DIR` 和安装器的 `--codex-home` / `--claude-home` 参数均受支持。无需选择机器型号或预设 profile。

## 手动安装

需要 Python 3.10+、Git 和已有的仓库访问权限。安装器只复制文件并填充本机路径，不安装依赖、不登录服务、不启动实验。

```bash
git clone https://github.com/kikixiong/kiki-custom-skill.git
cd kiki-custom-skill

# 选择当前使用的客户端
python3 install.py --target codex
# 或
python3 install.py --target claude
# 同一机器确实需要两个客户端时
python3 install.py --target both
```

也可使用已有的 SSH 仓库访问方式。不要把 token 放进命令、仓库或聊天。每台机器分别执行安装；在本机安装不等于向远端部署。

按需选择部分技能：

```bash
python3 install.py --target codex --skills kiki-paper-writing kiki-paper-workflow
```

`kiki-paper-writing` 提供论文写作指导；`kiki-paper-workflow` 是另一套多阶段论文流程，按任务选择。查看 [CATALOG.md](CATALOG.md) 获取全部目录名。

安装器先备份已有同名条目，再放入新副本；无关技能和 `.system` 保留。备份位于客户端 home 下的 `skill-backups/kiki-custom-skill/<时间戳>/`。替换软链接时只备份链接本身。处理中的错误会尝试回滚当前客户端已替换的条目；异常中断后可根据备份恢复。

`--dry-run` 仅显示目标路径和同名冲突，不写入文件。仓库含 `@@KIKI_*@@` 路径标记，请使用安装器，不要直接把未渲染的模板链接到客户端技能目录。

## 更新

```bash
git pull --ff-only
python3 install.py --target codex
```

按实际客户端选择 `codex`、`claude` 或 `both`。新建客户端会话加载更新。安装目录的修改不会自动回传到 GitHub；本机环境配置继续单独保留。

## 内容与能力边界

- `skills/`：默认可安装的 200 个技能。
- `support/`：共享工具、参考资源和跨客户端运行说明。
- `reference/`：系统和插件的参考快照，不由安装器注册或覆盖。
- `provenance/`、`THIRD_PARTY_NOTICES.md`：来源、版本和版权说明。

技能文件不提供插件运行时、外部服务授权或 GPU 资源。使用当前客户端实际提供的工具。系统技能和插件由对应客户端管理；参考快照不代表已经安装的能力。

`reference/system-skills/skill-creator/` 保存 Anthropic 版本及跨客户端执行说明，默认安装器不替换系统入口。其 Claude 专用评测脚本依赖 Claude CLI，不能据此宣称完成了 Codex 行为评测。

可选 SCFM 论文库由使用者自行提供，通过 `KIKI_SCFM_LIBRARY` 或 `--library` 指定；仓库不包含个人论文库。模型运行位置、设备选择和执行限制从当前任务及本机配置获得，安装行为本身不授权启动实验。

## 来源与维护

集合名称不表示全部内容由 Kiki 原创。保留第三方来源和许可证，详见 [来源说明](THIRD_PARTY_NOTICES.md)。这些来源信息及必要的技术示例不属于机器配置。

安装结果与技能功能验证分开报告；历史评测资料不代表当前机器已验证。维护时检查新文件中的个人路径、主机、账号状态和凭据，机器专属信息放到本机配置中。
