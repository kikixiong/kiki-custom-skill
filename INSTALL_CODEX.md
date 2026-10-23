# 给 Codex 的安装说明

安装前阅读 README 与本文件。使用当前机器的路径和项目约定，不沿用维护者的环境。

1. 使用已有的 GitHub 访问方式克隆 https://github.com/kikixiong/kiki-custom-skill 到普通源码目录，不复制其他机器的凭据。
2. 确认当前用户目录及 `CODEX_HOME`。默认技能目录为 `~/.codex/skills`；设置 `CODEX_HOME` 时使用其 `skills` 子目录，也可传入 `--codex-home`。
3. 在仓库执行 `python3 install.py --target codex`。安装器自动填充当前机器路径；不需要机器 profile，也不会连接其他机器。
4. 默认安装 manifest 中的全部技能；只选部分时使用 `--skills` 和 CATALOG 中的目录名。同名条目先备份，无关技能与 `.system` 保留。
5. 需要机器专属配置时，复用用户和项目约定；缺少必要字段才集中询问。将补充内容保存到当前 Codex home 下的 `skill-config/kiki-custom-skill/environment.md`，不回写本仓库、不记录凭据。没有远程任务时不要求远程主机配置。
6. 报告实际安装位置、数量、备份位置和操作错误，提示新建会话加载技能。安装不授权模型实验、技能评测、登录变更或远程部署。

```bash
python3 install.py --target codex
# 仅显示路径和同名冲突
python3 install.py --target codex --dry-run
```

论文写作入口为 `$kiki-paper-writing`；多阶段工作流为 `$kiki-paper-workflow`。

不将 `reference/` 的系统和插件快照当作普通技能安装。更新时先 `git pull --ff-only` 再运行同一安装命令。不要删除整个技能目录或重写用户全局模型、网络、账号及 shell 配置。
