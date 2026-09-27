# 给 Codex 的安装说明

这是 Kiki 个人自用技能库。收到“安装这个仓库”的请求后，先阅读本文件与 README，再完成文件安装。不要把下载仓库等同于完成安装。

1. 使用当前机器已有的 GitHub 访问方式，克隆 `kikixiong/kiki-custom-skill` 到普通源码目录，例如 `~/repos/kiki-custom-skill`。不重复做登录预检，不复制其他机器的凭据。
2. 在**当前目标机器**确认 home 和 `CODEX_HOME` 是否已设置。默认技能路径为 `~/.codex/skills/<目录名>/SKILL.md`；有 `CODEX_HOME` 时为 `$CODEX_HOME/skills/<目录名>/SKILL.md`。
3. 在仓库执行 `python3 install.py --target codex --profile generic`；Mac、A6000-4、A6000-8 分别选择 `mac`、`a6000-4`、`a6000-8`。
4. 默认安装全部 200 个个人技能。只选一部分时使用 `--skills` 及 CATALOG 中的目录名。安装器会替换路径模板并备份已有同名条目，保留无关技能和 `.system`。
5. 完成后报告实际安装根目录、数量、备份位置和操作错误。开启新会话以加载技能。不要执行模型、数据实验、技能功能测试或授权探测来“验证安装”，除非用户另有要求。

```bash
cd ~/repos/kiki-custom-skill
python3 install.py --target codex --profile a6000-4
```

上例仅用于当前所在机器为 A6000-4 的情况。A6000-8 使用 `--profile a6000-8`。安装器不会 SSH 到其他机器。

**你的论文技能：** `~/.codex/skills/kiki-paper-writing/SKILL.md`，在 Codex 中可用 `$kiki-paper-writing`。另一套完整论文流程为 `$kiki-paper-workflow`。

不要把 `reference/` 的系统/插件快照作为普通技能安装。需要插件时使用当前 Codex 的插件管理能力；现成的 Mac 插件缓存不代表 Linux 服务端有相同运行时。

后续更新：在仓库 `git pull --ff-only` 后重复同一安装命令。不要删除整个 `~/.codex/skills`，不要改全局模型、SSH、VPN、账号或 shell 配置。
