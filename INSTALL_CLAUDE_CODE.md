# 给 Claude Code 的安装说明

这是 Kiki 个人自用技能库，内容采用 `SKILL.md` 加配套目录结构。请按当前机器路径安装，不沿用 Mac 的绝对路径。

1. 用当前机器已有权限克隆 `kikixiong/kiki-custom-skill` 到 `~/repos/kiki-custom-skill` 或其他普通源码目录。
2. 默认安装位置是 `~/.claude/skills/<技能目录>/SKILL.md`；共享资源在 `~/.claude/skill-support/kiki-custom-skill/`。设置了 `CLAUDE_CONFIG_DIR` 或 `--claude-home` 时，安装器使用该目录的对应子目录。
3. 在目标机器执行 `python3 install.py --target claude --profile generic`。Mac、A6000-4、A6000-8 分别使用相应 profile。
4. 安装器渲染本机绝对路径，并把已知技能的 `$skill-name` 调用例子适配为 `/skill-name`。`agents/openai.yaml` 是附带的 Codex 元数据，不是 Claude Code 插件配置。
5. 原同名技能先备份；无关技能保留。报告实际目录、安装数量和备份位置，不运行模型/数据实验、技能功能测试或账号授权预检。

```bash
cd ~/repos/kiki-custom-skill
python3 install.py --target claude --profile a6000-8
```

上例在 A6000-8 上运行。若同一机器同时用 Codex 与 Claude Code，可执行 `python3 install.py --target both --profile a6000-8`，分别安装到两个客户端的目录。

**你的论文技能：** `~/.claude/skills/kiki-paper-writing/SKILL.md`，使用 `/kiki-paper-writing`。完整多阶段工作流为 `/kiki-paper-workflow`。安装后新建会话使用。

调用技能前读取安装后的 `support/compatibility.md` 所对应实际路径。正文中历史的 Codex API/工具名字需映射到当前 Claude Code 的实际能力；工具不可用时明确说明，不要虚构调用或结果。插件、外部服务授权及模型依赖需由本机现有环境提供，文件安装不等于这些能力已配置。

默认不把 `reference/` 下的系统或插件快照注册为 Claude Code 技能。不要改用户的全局 `CLAUDE.md`、授权、模型或 shell 配置。日后在仓库 `git pull --ff-only`，再运行同一安装命令。

目录与 `/skill-name` 调用规则依据 [Claude Code 官方技能文档](https://code.claude.com/docs/en/skills)。
