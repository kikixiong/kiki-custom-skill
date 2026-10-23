# 给 Claude Code 的安装说明

本仓库采用 `SKILL.md` 加配套资源目录的结构。安装前阅读 README 与本文件，使用当前机器的路径和项目约定。

1. 用已有权限克隆 https://github.com/kikixiong/kiki-custom-skill 到普通源码目录。
2. 默认技能目录为 `~/.claude/skills`，共享资源在 `~/.claude/skill-support/kiki-custom-skill`。设置 `CLAUDE_CONFIG_DIR` 或传入 `--claude-home` 时，使用对应 home 下的目录。
3. 执行 `python3 install.py --target claude`。安装器渲染本机路径，并把已知技能的 `$skill-name` 调用示例适配为 `/skill-name`。不需要机器 profile，也不会连接其他机器。
4. 原同名技能先备份，无关技能保留。需要补充机器约定时，复用用户和项目配置；必要信息缺失才集中询问，并保存到当前 Claude Code home 下的 `skill-config/kiki-custom-skill/environment.md`。不回写仓库、不记录凭据、不改全局 `CLAUDE.md`。
5. 报告实际位置、安装数量、备份位置和操作错误，提示新建会话。安装不授权模型实验、技能评测、登录变更或远程部署。

```bash
python3 install.py --target claude
# 同一机器确实需要两个客户端时
python3 install.py --target both
```

论文写作入口为 `/kiki-paper-writing`；多阶段工作流为 `/kiki-paper-workflow`。

调用技能时遵循安装后的运行说明，使用当前 Claude Code 的实际能力。`agents/openai.yaml` 是 Codex 元数据，不是 Claude Code 插件配置。文件安装不会提供缺失的插件、连接器、授权或模型依赖。

默认不安装 `reference/` 的系统或插件快照。日后先 `git pull --ff-only`，再执行同一安装命令。
