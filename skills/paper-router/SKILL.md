---
name: paper-router
description: 论文与学术文本请求的总入口：选题定位、大纲、起草/改写章节、中英文润色、去 AI 味、翻译、引用、审稿自查、数字/证明核验、论文图表、slides/海报、LaTeX 编译、Overleaf 同步、rebuttal、基金、综述。任何论文写作、改稿、投稿、返修请求即使看起来是简单改写也先用它，再按表读取具体 skill。
---

# Paper Router

论文类 skill 已设为仅手动调用（`disable-model-invocation: true`），不在自动列表里。本 skill 是它们的二级目录。

## 用法

1. 按下表判断请求阶段，选 1 个主 skill（必要时再加 1～2 个辅助）。拿不准时先看“易混淆对照”。
2. 用 Read 工具读取所选 skill 的 SKILL.md 绝对路径，按其正文执行。**不要**用 Skill 工具调它（已禁止模型调用，会失败）。
3. 叶子 skill 正文里的相对路径（`references/`、`scripts/` 等）按该 SKILL.md 所在目录解析。
4. 叶子 skill 要求“调用/使用某 skill”时，同样改为 Read `@@KIKI_SKILLS_DIR@@/<name>/SKILL.md`。
5. 正文提到 Codex 专有能力（Codex MCP、原生 imagegen、`~/.codex`、fork_turns）时，换成 Claude Code 等价物（Agent 子代理、本地绘图脚本）；没有等价物就告诉用户。
6. 用户点名某个 skill 或 `/名字` 时，直接用那个，不再路由。
7. 一次选定后告诉用户“用的是 X”，方便纠正。

路径前缀统一为 `@@KIKI_SKILLS_DIR@@/`，下文只写目录名，实际读取 `@@KIKI_SKILLS_DIR@@/<目录名>/SKILL.md`。

标记：⚠C = 正文含 Codex 专有用法，按第 5 条转译；重 = 多阶段重型流程，仅在用户明确要全流程时用。

## 默认选择（没有特殊信号时）

| 请求 | 默认 |
|---|---|
| 改/写 AI/ML 论文某一节、比较候选版本、按反馈迭代 | `kiki-paper-writing` |
| 只改英文表达，一次给结果 | `nature-polishing` |
| 投稿前挑毛病，要问题清单 | `pre-submission-reviewer` |
| 已有审稿意见写 rebuttal | `rebuttal` |
| 论文数据图（matplotlib） | `nature-figure` |
| 编译 LaTeX / 修编译错误 | `paper-compile` |

## 1. 选题定位与规划

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `novelty-check` ⚠C | “有没有人做过 X”、最近邻工作、贡献定位 | 全面评估 idea 可行性（`idea-evaluator`）；系统综述（`af-literature-review`） |
| `tech-paper-template` | 方法论文“背景-局限-想法-挑战-模块-贡献”逻辑链 | benchmark 论文（`benchmark-paper-template`）；要页数/图表/引用规划（`paper-plan`） |
| `benchmark-paper-template` | 贡献是 benchmark/数据集/评测框架的论文结构 | 方法论文（`tech-paper-template`） |
| `intro-drafter` | 只理 Introduction 六段提纲、动机-贡献一致性、running example；输出提纲不是成稿 | 写成段落（`kiki-paper-writing`） |
| `paper-plan` ⚠C | 实验结论已有，要 PAPER_PLAN.md：逐节大纲、页数、Figure 1、引用脚手架 | idea 不稳（`idea-evaluator`）；只要逻辑链（`tech-paper-template`） |
| `af-systems-paper-writing` | OSDI/SOSP/NSDI 等系统论文骨架、页数分配、Motivation 观察、系统类 Evaluation | ML 会议（`20-ml-paper-writing`） |
| `ablation-planner` ⚠C | 设计消融、算力有限时排优先级、rebuttal 补实验 | 整体实验矩阵（`experiment-plan`）；分析已有结果（`analyze-results`） |
| `grant-proposal` | 写基金申请书正文（国自然、NSF、科研費） | 只要格式模板（`af-venue-templates`） |
| `top-survey-workflow` | 写综述/review article，设计 taxonomy | 只整理文献不写综述（`af-literature-review`） |

## 2. 起草与实质改写

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `kiki-paper-writing` | **默认**。AI/ML 论文任一节的诊断式修订、多版本比较、多轮反馈迭代、claim 强度校准、术语/符号统一、caption、近终稿一致性审计、从 idea/大纲证据驱动起草 | 会议模板/转投换格式/API 取 BibTeX（`20-ml-paper-writing`）；纯语言润色（`nature-polishing`） |
| `20-ml-paper-writing` | 从研究 repo 写 NeurIPS/ICLR 整篇初稿、新建会议 LaTeX 工程、转投换模板压页数、Semantic Scholar 取真实 BibTeX、查会议 checklist | 段落级修订（`kiki-paper-writing`）。注：frontmatter name 是 `ml-paper-writing` |
| `paper-write` ⚠C | 已有 PAPER_PLAN.md，批量产出 `sections/*.tex` 和 references.bib | 无大纲（先 `paper-plan`）；改已有段落（`kiki-paper-writing`） |
| `research-paper-writing` | 已有段落的结构与衔接：flow、反向大纲、一段一信息、段落角色标注 | 只改措辞（`nature-polishing`） |
| `academic-paper` | 社科/教育/期刊论文，APA/Chicago，访谈式配置；引用格式互转、双语摘要、AI 使用声明、审稿意见整理成修改路线图 | ML 会议稿（`kiki-paper-writing` / `20-ml-paper-writing`）。默认 zh-TW，偏重 |
| `af-scientific-writing` ⚠C | 医学/生命科学 IMRAD、CONSORT/STROBE/PRISMA、提纲扩写成段、技术报告/白皮书排版 | ML/系统会议稿 |
| `scfm-paper-writing` | 单细胞基础模型（scGPT、Geneformer 等）论文章节，对照同领域范文 | 非单细胞领域（`kiki-paper-writing`） |

## 3. 语言润色与翻译

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `nature-polishing` | **默认**。英文段落一次性润色成 Nature 风格：精炼、拆长句、hedging；标题/摘要字数规范 | 要逐句挑方案多轮确认（`af-paper-polish-workflow`）；ML 顶会不要英式拼写（`kiki-paper-writing`） |
| `af-paper-polish-workflow` | 逐段/逐节交互式精修，先核结构再改句；跨章节数字术语一致、highlights | 一次性快速改（`nature-polishing`） |
| `af-humanizer-zh` | 中文文本去 AI 味、删套话 | 英文润色；翻译 |
| `awesome-ai-research-writing` | 短小文字变换：中译英 LaTeX、英译中、缩写到 N 词、扩写、写 caption | 精修（`nature-polishing`） |

## 4. 引用

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `af-citation-management` | DOI/arXiv 转 BibTeX、找高被引论文导出、清理去重 .bib、PubMed 检索 | 核查引用是否支持论断（`citation-audit`） |
| `citation-audit` ⚠C | 投稿前查引用是否编造、作者年份是否对、是否支持所在句、预印本是否已正式发表 | 草稿未完成时；只整理 bib（`af-citation-management`） |

## 5. 审稿、自查与核验

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `pre-submission-reviewer` | **默认**。投稿前挑毛病：按严重程度列逻辑/语言/LaTeX/图表/AI 味问题清单，不改写 | 要直接改写（润色类） |
| `academic-paper-reviewer` | 多审稿人模拟 + 编辑决定（Accept/Major…）、修改后 re-review；偏期刊 | 单份审稿报告（`af-peer-review`） |
| `af-peer-review` ⚠C | 替期刊写一份规范 referee report；临床/生物医学方法统计检查；评审基金或演讲 | 多审稿人模拟（`academic-paper-reviewer`） |
| `af-scholar-evaluation` ⚠C | 量化评分卡、最弱维度、多版本分数追踪 | 叙述式审稿（`af-peer-review`） |
| `research-review` ⚠C | ML 研究的严厉外部审稿人：挑战 story、该补哪些实验、mock NeurIPS review，多轮对话 | 一次性稿件审稿（`academic-paper-reviewer`） |
| `result-to-claim` ⚠C | 刚跑完实验：结果能支撑哪些 claim、要不要收窄、还缺什么 | 论文写完核数字（`paper-claim-audit`） |
| `paper-claim-audit` ⚠C | 论文里的数字/表格/“consistently outperforms”是否与结果文件一致 | 实验代码作弊/泄漏（`experiment-audit`） |
| `proof-checker` ⚠C | 检查并修复定理证明漏洞、补推导 | 公式排版（`paper-compile`） |
| `auto-paper-improvement-loop` ⚠C 重 | 已能编译的完整稿，无人值守多轮审-改-编译 | 一次性审稿意见（`pre-submission-reviewer`） |

## 6. 论文图表

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `nature-figure` | **默认**数据图。matplotlib 期刊/顶会风格、多面板、统一配色、矢量导出、美化已有图 | 架构图（`figure-spec`）；按计划批量出全部图（`paper-figure`） |
| `paper-figure` ⚠C | 按结果文件或 PAPER_PLAN.md 一次产出整篇的数据图和对比表、`\includegraphics` 片段 | 架构/流程图；定性样本图 |
| `af-academic-plotting` ⚠C | 没指定图型，先判断画数据图还是框图；选色板/视觉风格 | 已知图型时用具体 skill |
| `scientific-figure-making` | 明确要 figures4papers 风格的 matplotlib 图 | 未提 figures4papers（`nature-figure`） |
| `figures4papers` | 明确说参考 figures4papers 仓库 demo，找最接近示例脚本改写 | 同上 |
| `figure-spec` | 可编辑、精确的 SVG/PDF 架构图、pipeline 图、决策图（含中文标签） | 数据图；简单流程图（`mermaid-diagram`） |
| `figure-designer` | 出图前规划 Figure 1/总览图布局，或审查已有图；只出文字方案 | 要图文件或代码 |
| `paper-illustration` ⚠C | AI 生成/编辑概念插图、teaser，位图可接受 | 含实测数值的图（严禁）；可编辑框图 |
| `craft-scientific-figure-prompts` ⚠C | 产出是生图 prompt：学参考图风格、审长 prompt、局部修正、多图风格统一 | 直接要图 |

## 7. 演示与海报

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `paper-slides` ⚠C 重 | 已有 LaTeX 论文工程，生成会议 talk 的 Beamer+PPTX+讲稿 | 组会/答辩（`af-scientific-slides`） |
| `af-presenting-conference-talks` | 快速搭会议 talk 页面大纲、speaker notes、讲稿 | 要成品流水线（`paper-slides`） |
| `af-scientific-slides` ⚠C | 非会议场景：seminar、答辩、组会、journal club、基金 pitch | 论文转会议 talk（`paper-slides`） |
| `paper-poster` ⚠C | 会议海报 A0/A1，PDF/PPTX/SVG，tcbposter 排错 | slides |

## 8. 投稿、返修、编译与同步

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `rebuttal` ⚠C | **默认**。OpenReview/CMT 审稿意见写有字数限制的正式 rebuttal、追问的增量回复、QUICK_MODE 只看策略 | 投稿前自查（`pre-submission-reviewer`） |
| `rebuttalstudio` | 点名 RebuttalStudio，或要五阶段式整理、OpenReview 评论串逐条回复、Final Remarks | 有严格字符预算的终稿（`rebuttal`） |
| `af-venue-templates` | 拿会议/期刊/基金/海报的模板和格式规范、调写作风格到目标期刊 | 编译（`paper-compile`） |
| `paper-compile` | **默认**。编译 PDF、修报错、`??` 引用、页数/字体嵌入/匿名检查 | 改内容 |
| `overleaf-sync` | 单纯 pull/push/status 与 Overleaf 同步 | 逐段审批（`overleaf-paper-sync`） |
| `overleaf-paper-sync` | 逐段推到 Overleaf 网页审阅、批准后再改下一段 | 普通同步（`overleaf-sync`） |

## 9. 全流程与其他路由（重，仅用户明确要求时）

| skill | 用于 |
|---|---|
| `kiki-paper-workflow` ⚠C 重 | NARRATIVE_REPORT.md → 大纲 → 图 → 正文 → 编译 → 两轮改进，产出英文 LaTeX+PDF，约 45-90 分钟 |
| `academic-pipeline` 重 | 调研→写作→核验→审稿→修改→终检 10 阶段，每阶段要用户确认 |
| `top-ai-paper-submission` | 口语化跨阶段：“能中吗”“离投稿还差什么”、投稿打包、OpenReview 表单字段 |
| `supervisor-skills-routing` | 很早期、诉求笼统：idea 值不值得做、故事线理不顺；不确定时先问一个问题 |
| `academicforge-routing` | 用户明确要 AcademicForge / af-* 系列工具时 |
| `academicforge-tool` ⚠C | 在 AcademicForge 上游语料中按主题搜指南、管理 preset；不自动 resync |

## 其他分类

请求不属于论文写作时改读对应 router：文献检索/idea 评估 → `research-router`；实验规划/结果分析/实验审计 → `experiment-router`；Mermaid 图、中文正式报告、组会简报 → `meta-router`；训练/推理框架 → `ml-train-router` / `ml-infer-router`。
