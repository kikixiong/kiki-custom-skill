# Kiki Custom Skill

**Kiki 个人自用的技能集合。** 用于在自己的 Mac、A6000-4、A6000-8 等机器之间保存、安装和更新，不是面向公众的通用产品，也不代表所有内容由 Kiki 原创。

包含 **200 个个人技能**及其脚本、模板和共享资源。你自己的论文写作技能是 **`kiki-paper-writing`（Kiki Paper Writing）**；完整的多阶段论文工作流另存为 `kiki-paper-workflow`。

[查看全部技能](CATALOG.md) · [给 Codex 的安装说明](INSTALL_CODEX.md) · [给 Claude Code 的安装说明](INSTALL_CLAUDE_CODE.md)

## 安装到哪里

| 客户端 | 默认技能安装位置 | 辅助资源位置 |
|---|---|---|
| Codex | `~/.codex/skills/<技能目录>/SKILL.md` | `~/.codex/skill-support/kiki-custom-skill/` |
| Claude Code | `~/.claude/skills/<技能目录>/SKILL.md` | `~/.claude/skill-support/kiki-custom-skill/` |

在每台目标机器上执行安装。这里的 `~` 是**当前登录用户在那台机器上的 home**，不是 Mac 的 `/Users/...`，也不是其他服务器的 `/home/...`。

Codex 设置了 `CODEX_HOME` 时，安装器使用 `$CODEX_HOME/skills`；Claude Code 设置了 `CLAUDE_CONFIG_DIR` 时使用其 `skills` 子目录。也可通过 `--codex-home` / `--claude-home` 明确指定。

## 下载与安装

需要 Python 3.10+、Git，以及这台机器已经具备的私有仓库访问权限。安装器只复制文件和填充本机路径，不安装依赖、不登录服务、不启动实验。

```bash
mkdir -p ~/repos
git clone git@github.com:kikixiong/kiki-custom-skill.git ~/repos/kiki-custom-skill
cd ~/repos/kiki-custom-skill

# 只配置 Codex
python3 install.py --target codex

# 或者只配置 Claude Code
python3 install.py --target claude

# 或者同时配置两个客户端
python3 install.py --target both
```

HTTPS 已有凭据的机器也可使用 `https://github.com/kikixiong/kiki-custom-skill.git`。复用已有访问方式；不要把 token 放进仓库、URL 或聊天。

机器配置示例，选择当前所在机器对应的一条执行：

```bash
# Mac
python3 install.py --target both --profile mac

# A6000-4
python3 install.py --target both --profile a6000-4

# A6000-8
python3 install.py --target both --profile a6000-8
```

这些命令需要在各自机器上运行；在 Mac 上指定 `--profile a6000-4` 不会远程连接或部署到服务器。

只安装部分技能时使用目录名：

```bash
python3 install.py --target codex --skills kiki-paper-writing kiki-paper-workflow
```

安装器默认备份已有的同名技能，再放入本次副本；不删除其他技能。原目录是软链接时备份链接本身，不修改链接指向的外部库。备份位于对应客户端目录下的 `skill-backups/kiki-custom-skill/<时间戳>/`。处理中的错误会尝试回滚当前客户端已替换的条目；异常断电等情况可根据备份手动恢复。

## 更新

```bash
cd ~/repos/kiki-custom-skill
git pull --ff-only
python3 install.py --target both --profile a6000-4
```

按当前机器调整 `--target` 和 `--profile`。新建客户端会话加载新技能。日常维护优先修改仓库并提交，再在其他机器拉取；只改安装目录不会自动同步回 GitHub。

`--dry-run` 仅显示目标路径和同名冲突，不写入文件。仓库内容包含安装时填充的 `@@KIKI_*@@` 路径标记，请使用安装器，不要直接把模板目录软链接到客户端技能目录。

## 内容范围

- `skills/`：默认可安装的 200 个个人技能。
- `support/`：共享科研工具、精选写作语料库和跨客户端运行说明。
- `profiles/`：机器标签与个人执行偏好；不包含 IP、SSH 密钥或账号凭据。
- `reference/system-skills/`：6 个系统入口的参考快照。
- `reference/plugin-packages/`：58 个插件技能入口及其原包资源，仅供参考。
- `provenance/`、`THIRD_PARTY_NOTICES.md`：来源和版权说明。

系统技能和插件由对应客户端自行管理，安装器不会把缓存冒充已安装插件，也不会覆盖 `.system`。需要专用工具、连接器、文档运行时或外部 API 的技能，只能使用当前机器实际提供的能力；GitHub、Overleaf 等授权不会随技能文件迁移。

`skill-creator` 参考副本于 2026-10-09 按个人选择更新为 [Anthropic 版本](https://github.com/anthropics/skills/tree/683bc88e56f3e09ba94f7055977f3d3aa499f202/skills/skill-creator)，完整保留脚本、查看器和 Apache-2.0 许可证，并附 Codex/Claude 执行说明。维护者本机的同名入口已单独备份后更新；它仍位于 `reference/system-skills/skill-creator/`，**默认安装器不会把这次系统入口替换传播到其他机器**。来源与改动见 `provenance/anthropic-skill-creator.json`。Claude 专用评测脚本不代表 Codex 原生评测能力，本次未运行评测。

SCFM 私有论文库未打包。需要它时配置 `KIKI_SCFM_LIBRARY` 或向 `scfm-paper-writing/scripts/library.py` 传入 `--library /真实路径`。Kiki Paper Writing 本身的写作资料已完整包含。

保留个人实验偏好：Mac 不运行模型/数据实验；默认实验主机为 CNIC，用户明确指定其他主机时按任务执行。安装本仓库不授权启动实验、抢占 GPU、停止已有任务或改 SSH/VPN。

## 维护状态

本次按用户要求只做文件与静态检查，**没有运行安装器测试、技能功能测试或模型实验，也未部署到两台 A6000**。旧技能中的验证报告是历史资料，不是本次跨客户端验证结果。

第三方许可证和必要来源信息保留，详见 [来源说明](THIRD_PARTY_NOTICES.md)。不要在未经检查的情况下把这个个人仓库改为公开。

Claude Code 的个人技能目录与调用方式依据[官方技能文档](https://code.claude.com/docs/en/skills)；Codex 的默认路径与本机系统 `skill-installer` 说明保持一致。
