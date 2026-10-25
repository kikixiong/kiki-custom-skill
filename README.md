# Kiki Custom Skill

面向 Codex 和 Claude Code 的可移植技能集合，包含 **210 个可安装技能**（10 个分类 router + 200 个叶子技能）及其脚本、模板和共享资源。不同机器使用各自的用户目录、工具和项目配置；仓库不预设服务器、GPU、账号、实验路径或个人执行偏好。

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

## 分类路由（安装前必读）

技能全部进入自动列表会超出客户端的技能描述预算：Claude Code 实测 200 个技能时，排在字母后面的约 100 个只剩名字、没有描述，模型无法据此选择。因此本集合默认采用两级结构：

- **自动列表只放 12 个入口**：10 个分类 router 加 `pua`、`prompt-clarifier`（后两个按语气触发，跨所有领域）。
- **其余 198 个叶子技能设为仅显式调用**，不进自动列表，但用户仍可用 `/名字`（Claude Code）或 `$名字`（Codex）直接调用。
- **模型先调用 router，再用文件读取工具读取叶子的 `SKILL.md`**，按其正文执行。同一叶子可以出现在多个 router 中。

| router | 覆盖 |
|---|---|
| `paper-router` | 论文选题、起草、润色、去 AI 味、翻译、引用、审稿自查、核验、图表、slides/海报、编译、Overleaf、rebuttal、基金、综述 |
| `research-router` | 论文检索、单篇速读、每日追踪、相关工作、系统综述、深度研究、选题、idea 评估、研究 wiki |
| `experiment-router` | 实验规划、结果分析、可信度审计、监控、训练检查、科研代码、算法核验、项目进度、AutoDL、GPU 排障、实验追踪 |
| `ml-train-router` | 分布式训练、DeepSpeed/FSDP/Megatron、LoRA/QLoRA、SFT/DPO/GRPO/PPO、RLHF、蒸馏合并、MoE、长上下文、分词 |
| `ml-infer-router` | vLLM/SGLang/TensorRT-LLM/llama.cpp、投机解码、AWQ/GPTQ/HQQ/bitsandbytes/GGUF、剪枝、评测、云 GPU |
| `llm-app-router` | LangChain、LlamaIndex、DSPy、多 agent、结构化输出、向量库、embedding、tracing、guardrails |
| `ml-domain-router` | CLIP、BLIP-2、LLaVA、SAM、Stable Diffusion、Whisper、MusicGen、VLA 机器人、TransformerLens/SAE 可解释性 |
| `quant-router` | 因子/alpha、IC、回测审查、聚宽、组合风险归因、数据管线时点、AI 量化论文 |
| `coding-router` | GitHub 仓库/PR/issue、CI 修复、review 意见、提交推送、代码结构、验证强度、学术主页 |
| `meta-router` | 模糊输入澄清、记忆与知识图谱、经验沉淀、skill 查重、Mermaid、Markdown 文档、组会简报、ElegantPaper 报告 |

### 两个客户端的实现方式

| | Claude Code | Codex |
|---|---|---|
| 叶子仅显式调用 | 仓库里的 `SKILL.md` frontmatter 已带 `disable-model-invocation: true` | 安装器在每个叶子的 `agents/openai.yaml` 写入 `policy.allow_implicit_invocation: false` |
| router 读取叶子 | Read 工具读取 `~/.claude/skills/<名字>/SKILL.md` | shell 读取 `~/.codex/skills/<名字>/SKILL.md` |
| 读取权限 | **必须配置**，见下文 | 默认沙箱可读用户目录，通常无需配置；容器内见下文 |

### Claude Code 必需设置：叶子目录的读取权限

不配置时，router 每次读取叶子 `SKILL.md` 都会请求权限；在 `claude -p` 等非交互模式下会直接被拒，模型只能在没读到正文的情况下凭印象执行。安装时加 `--claude-allow-read`，安装器会先备份 `settings.json`，再追加两条只读规则：

```bash
python3 install.py --target claude --claude-allow-read
```

手动添加时，把 `<CLAUDE_HOME>` 换成实际 home 的绝对路径（例如 `/home/alice/.claude`），前面的 `//` 表示绝对路径：

```json
{ "permissions": { "allow": ["Read(/<CLAUDE_HOME>/skills/**)", "Read(/<CLAUDE_HOME>/skill-support/**)"] } }
```

### Codex 在容器里：沙箱起不来

Linux 上 Codex 用 bubblewrap 沙箱执行命令。容器通常不允许创建 user namespace，所有命令都会失败，报 `bwrap: No permissions to create a new namespace`，router 也就读不到叶子（模型可能编一个技能名）。此时在 `~/.codex/config.toml` 顶部加：

```toml
sandbox_mode = "danger-full-access"   # 依赖容器自身隔离
approval_policy = "on-request"        # 有风险的命令先询问
```

这会关闭 Codex 内置隔离，修改前先征得用户同意并备份配置。非容器机器不需要。

### 安装后检查

1. **新开一个会话**。技能列表在会话启动时加载，已打开的会话看不到变化。
2. 运行 `python3 support/routing/check_routers.py <客户端 home>/skills`。预期结果：`orphans: none`、`router refs to missing dirs: none`、自动列表描述约 2k 字符。
3. 在新会话里发一句“帮我把这段英文润色一下：……”。预期模型先调用 `paper-router`，再读取 `nature-polishing/SKILL.md`，并说明“用的是 nature-polishing”。

### 不想要两级结构时

`python3 install.py --target claude --no-routing` 会去掉叶子的仅显式标记，所有技能恢复自动调用（技能数量多时会出现描述截断）。用 `--skills` 只装部分技能时，安装器会自动带上 10 个 router。

### 维护：新增或删除技能

- 新增叶子技能：在对应 router 的表格里加一行（`| \`目录名\` | 用于 | 不用于（改用） |`），给它的 frontmatter 加 `disable-model-invocation: true`，同步更新 `manifest.json` 和 `CATALOG.md`。
- 新增的技能如果应该自动触发（跨领域、按语气触发），不加标记，也不放进 router。
- 改完运行 `check_routers.py`，确认没有孤儿和失效引用。

## 更新

```bash
git pull --ff-only
python3 install.py --target codex
```

按实际客户端选择 `codex`、`claude` 或 `both`。新建客户端会话加载更新。安装目录的修改不会自动回传到 GitHub；本机环境配置继续单独保留。

## 内容与能力边界

- `skills/`：默认可安装的 210 个技能，其中 10 个 `*-router` 为分类入口。
- `support/`：共享工具、参考资源和跨客户端运行说明。
- `reference/`：系统和插件的参考快照，不由安装器注册或覆盖。
- `provenance/`、`THIRD_PARTY_NOTICES.md`：来源、版本和版权说明。

技能文件不提供插件运行时、外部服务授权或 GPU 资源。使用当前客户端实际提供的工具。系统技能和插件由对应客户端管理；参考快照不代表已经安装的能力。

`reference/system-skills/skill-creator/` 保存 Anthropic 版本及跨客户端执行说明，默认安装器不替换系统入口。其 Claude 专用评测脚本依赖 Claude CLI，不能据此宣称完成了 Codex 行为评测。

可选 SCFM 论文库由使用者自行提供，通过 `KIKI_SCFM_LIBRARY` 或 `--library` 指定；仓库不包含个人论文库。模型运行位置、设备选择和执行限制从当前任务及本机配置获得，安装行为本身不授权启动实验。

## 来源与维护

集合名称不表示全部内容由 Kiki 原创。保留第三方来源和许可证，详见 [来源说明](THIRD_PARTY_NOTICES.md)。这些来源信息及必要的技术示例不属于机器配置。

安装结果与技能功能验证分开报告；历史评测资料不代表当前机器已验证。维护时检查新文件中的个人路径、主机、账号状态和凭据，机器专属信息放到本机配置中。
