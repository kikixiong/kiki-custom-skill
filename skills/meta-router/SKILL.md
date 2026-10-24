---
name: meta-router
description: 元技能与通用请求的总入口：施压纠偏(pua/再试试/又错了)、模糊输入澄清、记忆/知识图谱/经验沉淀、新建 skill 前查重、Mermaid 图、Markdown 文档、组会简报与 ElegantPaper 报告。先用它再按表读取具体 skill
---

# 元技能与通用请求 Router

本分类的叶子 skill 已设为仅显式调用（Claude Code：frontmatter `disable-model-invocation: true`；Codex：`agents/openai.yaml` 中 `policy.allow_implicit_invocation: false`），不在自动列表里。本 skill 是它们的二级目录。

## 用法

1. 按下表选 1 个主 skill（必要时加 1～2 个辅助）；拿不准时看“默认选择”和“不用于”列。
2. 用文件读取工具读取 `@@KIKI_SKILLS_DIR@@/<目录名>/SKILL.md`，按其正文执行。**不要**通过技能调用机制加载叶子（Claude Code 的 Skill 工具会因仅显式调用而失败）。
3. 叶子正文里的相对路径（`references/`、`scripts/`）按该 SKILL.md 所在目录解析；叶子要求“调用某 skill”时同样改为 Read 其 SKILL.md。
4. 正文含 Codex 专有能力（Codex MCP、原生 imagegen、`~/.codex`、automation API）时：在 Codex 中照常使用；在 Claude Code 中换成等价物（Agent 子代理、本地脚本），没有等价物就告诉用户。
5. 用户点名某 skill（Claude Code 输入 `/名字`，Codex 输入 `$名字`）时直接用它。选定后告诉用户“用的是 X”。
6. 请求属于其他分类时改读对应 router：`paper-router`、`research-router`、`experiment-router`、`ml-train-router`、`ml-infer-router`、`llm-app-router`、`ml-domain-router`、`quant-router`、`coding-router`。

标记：⚠C = 含 Codex 专有用法；重 = 多阶段重型流程，仅在用户明确要求时用。

## 默认选择（没有特殊信号时）

| 请求 | 默认 |
|---|---|
| 用户抱怨反复失败、要求再试 | `pua` |
| 画一张流程图/时序图 | `mermaid-diagram` |
| 写给导师的正式进展报告/PDF | `creating-elegantpaper-reports` |
| 记住某件事/整理记忆 | `memory-manager` |
| 组会前准备讨论材料 | `creating-research-meeting-reports` |

## 施压与纠偏

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `pua-en` | 英文场景施压：“try harder/stop giving up/you keep failing”，PIP 式西方大厂绩效话术+方法论 | 中文触发用 pua；日文用 pua-ja |
| `pua-ja` | 日语场景施压（詰め文化），用户以日语表达不满或要求穷尽方案 | 中文用 pua；英文用 pua-en |

## 记忆与学习

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `self-improvement` ⚠C | 命令意外失败、用户纠错“你搞错了”、发现可复用模式时，记录到 .learnings/ 或提升为 AGENTS.md 规则 | 按日/周/月整理记忆日志用 memory-manager；结构化实体关系用 ontology |
| `memory-manager` | 维护 MEMORY.md 与 memory/daily、weekly、monthly 分层日志：写日记、周/月压缩、检索历史记忆 | 失败教训/纠错沉淀用 self-improvement；实体与依赖图谱用 ontology |
| `ontology` | 类型化知识图谱：创建/查询 Person/Project/Task 等实体、“link X to Y”、依赖查询、跨 skill 共享状态 | 时间线式日志记忆用 memory-manager；经验教训记录用 self-improvement |

## skill 发现与管理

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `skill-advisor` ⚠C | 新建 skill 前查本地已装 skill 是否重复，建索引并检索相似功能，判断复用还是新建 | 从远端平台找/装新 skill |

## 图形与文档

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `mermaid-diagram` ⚠C | 单独生成 Mermaid 流程图/时序图/类图等，输出到 figures/ 并用 mmdc 渲染校验与视觉评审 | 整篇 Markdown 科学文档内嵌图用 af-markdown-mermaid-writing |
| `af-markdown-mermaid-writing` | 以 Markdown+内嵌 Mermaid 为规范格式撰写科学文档、技术说明、报告 | 只要一张图用 mermaid-diagram；正式 PDF/LaTeX 报告用 creating-elegantpaper-reports |

## 报告产出

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `creating-elegantpaper-reports` | 面向导师/实验室的正式报告：中期/进展/实验报告，ElegantPaper v0.12 LaTeX、Overleaf 源码、可打印 PDF | 组会前后讨论简报用 creating-research-meeting-reports；论文本身走 paper-router |
| `creating-research-meeting-reports` | 组会/导师会议前后的研究简报：从笔记、日志、slides 提炼决策点与待反馈问题，默认 Markdown | 正式 PDF/LaTeX 报告用 creating-elegantpaper-reports；日程或行政纪要不适用 |

`pua`、`prompt-clarifier` 保持自动调用，不在此表。
