---
name: research-router
description: 调研与选题的总入口：论文检索（arXiv/Semantic Scholar/DOI）、单篇速读、每日论文追踪、相关工作、系统综述、深度研究、头脑风暴选题、idea 评估、证据批判、研究 wiki、自主科研编排。先用它再按表读取具体 skill
---

# 调研与选题 Router

本分类的叶子 skill 已设为仅显式调用（Claude Code：frontmatter `disable-model-invocation: true`；Codex：`agents/openai.yaml` 中 `policy.allow_implicit_invocation: false`），不在自动列表里。本 skill 是它们的二级目录。

## 用法

1. 按下表选 1 个主 skill（必要时加 1～2 个辅助）；拿不准时看“默认选择”和“不用于”列。
2. 用文件读取工具读取 `@@KIKI_SKILLS_DIR@@/<目录名>/SKILL.md`，按其正文执行。**不要**通过技能调用机制加载叶子（Claude Code 的 Skill 工具会因仅显式调用而失败）。
3. 叶子正文里的相对路径（`references/`、`scripts/`）按该 SKILL.md 所在目录解析；叶子要求“调用某 skill”时同样改为 Read 其 SKILL.md。
4. 正文含 Codex 专有能力（Codex MCP、原生 imagegen、`~/.codex`、automation API）时：在 Codex 中照常使用；在 Claude Code 中换成等价物（Agent 子代理、本地脚本），没有等价物就告诉用户。
5. 用户点名某 skill（Claude Code 输入 `/名字`，Codex 输入 `$名字`）时直接用它。选定后告诉用户“用的是 X”。
6. 请求属于其他分类时改读对应 router：`paper-router`、`experiment-router`、`ml-train-router`、`ml-infer-router`、`llm-app-router`、`ml-domain-router`、`quant-router`、`coding-router`、`meta-router`。

标记：⚠C = 含 Codex 专有用法；重 = 多阶段重型流程，仅在用户明确要求时用。

## 默认选择（没有特殊信号时）

| 请求 | 默认 |
|---|---|
| 帮我找某主题的相关工作/调研一下这个方向 | `research-lit` |
| 读懂这篇 arXiv 论文 | `alphaxiv` |
| 搜/下载 arXiv 论文 | `arxiv` |
| 帮我想研究 idea / 选题 | `brainstorming-research-ideas` |
| 这个 idea 值不值得做 | `idea-evaluator` |
| 写一份系统性综述 | `af-literature-review` |

## 论文检索

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `arxiv` | 按主题或 arXiv ID 搜索最新预印本、拉取元数据、批量下载 PDF 到 papers/ | 已发表会议期刊/引用数改用 semantic-scholar；单篇快速读懂改用 alphaxiv |
| `semantic-scholar` | 检索已发表会议/期刊论文（IEEE/ACM 等），查引用数、venue、TLDR、引用关系 | 最新预印本或下载 PDF 改用 arxiv；跨库查 DOI/开放全文改用 af-paper-lookup |
| `af-paper-lookup` | 按 DOI/PMID/作者/主题跨 10 个学术库（PubMed、OpenAlex、Crossref、Unpaywall 等）查论文与开放全文 | 纯 arXiv 场景改用 arxiv；查 CS 引用数改用 semantic-scholar |
| `alphaxiv` | 给一个 arXiv ID/链接，快速读懂单篇论文，AlphaXiv 摘要→全文 markdown→LaTeX 源码逐级回退 | 主题检索或多篇调研改用 research-lit 或 arxiv |

## 论文追踪

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `arxiv-daily-digest` | 按用户配置的研究兴趣抓取、过滤、排序 arXiv 新论文，生成本地 Markdown digest；用户要求时才设定时任务或外发 | 一次性检索改用 arxiv；量化方向论文挖掘改用 quant-ai-paper-scout |
| `quant-ai-paper-scout` | 检索 NeurIPS/ICML/KDD 等 AI/时序论文，提炼可用于股票期货预测、多因子、alpha 的思路 | 非量化领域的相关工作调研改用 research-lit |

## 文献调研

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `research-lit` ⚠C | 围绕课题找相关工作并梳理研究脉络，可联动 Zotero/Obsidian/本地 papers/ 与 arXiv、DeepXiv | 正式系统性综述（PRISMA）改用 af-literature-review；单篇论文改用 alphaxiv |
| `af-literature-review` ⚠C 重 | 系统性文献综述：规划检索、筛选纳入、数据提取、主题综合、引用核验，输出 markdown/PDF | 快速相关工作梳理改用 research-lit；多代理深度研究报告改用 deep-research |
| `deep-research` 重 | 13 代理深度研究：问题定义、检索、证据综合、事实核查、meta-analysis、APA 报告，含苏格拉底引导模式 | 只需相关工作列表改用 research-lit；只做 idea 打分改用 idea-evaluator |
| `top-survey-workflow` | 用户要写综述、review article、tutorial review 或 state-of-the-art 综合，并要求达到顶刊水准，需要设计 taxonomy 并论证与已有综述的差异，而非逐篇罗列的阅读笔记。 | （论文类，也在 paper-router） |

## 选题构思

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `brainstorming-research-ideas` | 结构化头脑风暴找研究方向：问题优先、抽象阶梯、矛盾挖掘、跨领域迁移等十种框架，发散→收敛 | 追求认知科学式原创突破改用 creative-thinking-for-research；评估已有 idea 改用 idea-evaluator |
| `creative-thinking-for-research` | 用双联想、类比映射、约束操纵、反转、相邻可能等认知科学框架产生非增量的原创 idea | 项目级结构化选题流程改用 brainstorming-research-ideas |

## 选题评估

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `idea-evaluator` | 评估已有 idea 是否值得做：致命缺陷、创新性、可行性、五维打分、多个候选对比 | 还没有 idea 改用 brainstorming-research-ideas；审查已有研究证据质量改用 af-scientific-critical-thinking |
| `af-scientific-critical-thinking` ⚠C | 批判性审查研究设计、统计有效性、偏倚、混杂、证据质量（GRADE、Cochrane ROB）、逻辑谬误 | 评估自己的新 idea 改用 idea-evaluator |
| `novelty-check` ⚠C | 用户问“有没有人做过 X”“这个方法新不新”“最接近的 prior work 是哪篇、差在哪”“审稿人会拿哪篇来说我不新”；动手实验或写作前需要核查方法和实验设定的新颖性风险；需要知道怎样定位贡献。 | （论文类，也在 paper-router） |

## 知识库

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `research-wiki` | 维护项目级持久研究知识库：init/ingest/sync/query/lint，关联论文、idea、实验、结论图谱 | 从零搭建 wiki 目录结构与提示词模板改用 research-wiki-organization-prompts |
| `research-wiki-organization-prompts` | 搭建 raw/wiki 结构的研究 wiki 脚手架，论文摄入、领域地图、研究空白（gaps）整理的提示词流程 | 已有 ARIS 项目 wiki 的增量摄入与查询改用 research-wiki |

## 研究编排

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `0-autoresearch-skill` 重 | 全自主端到端 AI 研究项目：双循环（实验迭代+综合转向），从文献到论文并路由到领域 skill | 只需规划 AI 协作边界改用 vibe-research-workflow；只做调研改用 research-lit |
| `vibe-research-workflow` ⚠C | 规划 AI 辅助科研的编程、绘图、写作各阶段分工与学术诚信规则（元 skill） | 要全自主跑实验到论文改用 0-autoresearch-skill |
