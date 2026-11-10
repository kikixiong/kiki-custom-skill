# 与 Qgentic-AI 的对照

来源：Qgentic-AI，https://github.com/bogoconic1/Qgentic-AI（作者 bogoconic1，MIT License）。2026-11-10 以只读方式
浅克隆阅读了 README、`prompts/main_agent.py`、`prompts/research.py`、`prompts/guardrails.py`、`prompts/bash_judge.py`、
`prompts/tools_developer.py`、`utils/idea_pool.py`、`utils/compact.py`、`utils/skills.py`、`config.yaml`，未执行任何代码，
本 skill 也未复制其代码，以下只是对其设计思想的概括。

## 1. Qgentic-AI 的结构（概括）

- **角色**：MainAgent（编排者，GPT-5.5 循环，所有步骤都是工具调用）+ Researcher 子 agent（web 搜索/抓取 + bash 探针，
  产出带 URL 引用的 `RESEARCH.md`）。辅助 LLM：bash 安全裁判（每条 shell 命令执行前 allow/block）、训练监控
  （定时读 stdout/stderr，NaN、死锁、OOM 时 kill）、泄漏审查、代码安全审查、stack trace 联网诊断。
- **输入**：`GOAL.md`（会话目标，注入每个agent的 system prompt）、`RESEARCHER_INSTRUCTIONS.md`（任务专属研究指引）、
  竞赛数据与 Meta Kaggle 元数据。
- **工件**（`task/<slug>/<run_id>/`）：`MAIN.md`（活的计划）、`ideas/INDEX.md` + `ideas/<id>_<slug>.md`（idea 池，
  每次增删改后重建索引，索引常驻 system prompt）、`developer_vN/`（每次尝试一个目录：`SOLUTION.py/.txt/.json/.md`、
  `submission.csv`）、`research_N/RESEARCH.md`、只追加的 `*_chat.jsonl` 审计日志、可导出的 HTML trace。
- **循环**：选 idea → `start_dev_session` → 写 SOLUTION.py（固定日志头、必须写 `SOLUTION.json{score}`）→
  `run_solution`（静态 guardrail + 实时监控）→ **自查**（重读代码、score 与内部统计对账、grep 泄漏模式）→
  更新 idea 池 → 下一个。每次运行后强制一句 `metric=, delta=, decision=keep|pivot|escalate` 并在 MAIN.md 追加一行。
- **上下文控制**：上一轮 prompt 超过阈值（20 万 token）时把早期对话压缩成结构化摘要，保留最近 4 轮原文。
- **终止**：软件里没有终止条件，用户满意时手动停止。
- **写作纪律**：idea 正文必须是 spec（具体工件、可度量的通过标准、绝对路径、验证步骤，没有“也许 X 或 Y”）；
  给 Researcher 的指令必须自包含、写明答案形状和已排除项；“不要外包理解”。

## 2. 我们采纳的

| Qgentic-AI 的做法 | 在本 skill 中的落点 |
|---|---|
| GOAL.md 作为贯穿所有agent的总纲 | S1 产出 `GOAL.md`，每轮自检先读 |
| idea 池 = 索引 + 每 idea 一文件，idea 是 spec 不是想法 | S3 backlog（`SYNTHESIS.md` + state `hypotheses`），S4 protocol 要求可度量门槛和决策表 |
| 每次尝试独立目录 | `experiments/<slug>/` + `data/runs/<label>/` |
| 运行后强制 `metric/delta/decision` 记账 | `research-log.md` 行模板的“决策：keep/pivot/escalate” |
| 成功的运行也要自审（score 与 stats 对账、查泄漏、太好要怀疑） | S6 运气拆分、S7 对抗评审、“agent汇报，Orchestrator 核实” |
| 研究子 agent的结论“URL 存在但结论未独立验证”，要抽查 | 角色表中的复核规则；lessons 中 log 187→188 |
| 自包含 brief、写明答案形状和已排除项、不外包理解 | `templates.md` §7 |
| 独立文件的并行工具调用 | 每任务一条工作流、只写自己目录 |
| 训练监控：NaN/死锁/OOM 才 kill，模糊就继续 | “跑完才判”：探针只排序不判死 |
| 写操作限定在工作目录 + 命令安全裁判 | 沙箱只挂载 `sandbox/<name>/`，审查清单 |
| 上下文压缩 | 我们用文件化状态（state/log/findings）实现跨会话续接，压缩时以文件为准 |

## 3. 我们不同的地方及原因

| 方面 | Qgentic-AI | 我们 | 原因 |
|---|---|---|---|
| 分数来源 | `SOLUTION.json` 里脚本自报的 score（本地 CV） | 只认官方 verifier 原样运行的 JSON，基线先逐位复现 | verifier 赛题的分数可以完全复现；自报分数会混入盲区和运气 |
| 随机性 | 单次运行 | 预声明多 salt 均值、配对 seed 拆运气、禁止挑 salt | 我们见过 -0.121% 里只有 -0.019% 是结构性的 |
| 事前定价 | idea 有通过标准，但不要求数值预测 | 汇率表、预测区间、盈亏预算、kill 条件、决策表先于运行 | 防止事后合理化；汇率错一个量级会让整条线白做 |
| 终止 / 判死 | 永远循环；监控可按健康度 kill | kill 只按预注册条件且在完整运行后；外循环强制跳出框架 | 用户明确要求“跑完再判”；长期微调陷入局部最优 |
| 多 agent | 一个编排者 + 一个研究者，同一模型 | 研究/设计（强模型）、编码、独立对抗评审、安全评审分开，Orchestrator 复核 | 审查需要不被你的结论锚定；agent的“通过/解锁”多次出错 |
| 外部代码 | LLM 安全裁判 + guardrail，在主机上执行 | 书面 REVIEW.md（逐类 grep + 哈希清单）+ 集群断网沙箱；产物当不可信数据 | 下载的 notebook 不可信；集群容器默认可出网 |
| 情报 | Researcher 做 web 研究 | 定期拉榜、缓存公开 notebook、队友分支，分任务 diff 并拼装 | 我们最大的几步来自收割和拼装，不是自研 |
| 发布 | 无（生成 submission.csv） | 推送门槛、新分支、用户身份、先汇报、外部动作需批准 | 团队仓库与竞赛规则要求；用户掌控对外动作 |
| 算力 | 本地 GPU，单进程执行 | 集群作业提交器硬性上限（≤ 集群一半）、GPU 优先、共享存储陈旧文件对策 | 共享集群与 共享对象存储挂载的实际约束 |
| 记录 | jsonl 对话审计 + MAIN.md | 只追加的 research-log（含 correction / NEGATIVE / incident）+ VERIFIED/CLAIMED/INFERRED 标签 | 负结果和更正是后续定价的输入 |

## 4. 可进一步借鉴（尚未采用）

- Qgentic-AI 的 HTML trace 导出：便于把一次战役的完整过程给用户或队友复盘。
- “每个工具结果后先写 1–3 句：结果说明了什么、下一步为什么”——可用于子 agent的进度汇报格式。
