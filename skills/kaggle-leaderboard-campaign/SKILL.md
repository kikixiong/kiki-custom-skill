---
name: kaggle-leaderboard-campaign
description: 长周期“有官方 verifier/打分器”的优化竞赛与冲榜战役编排（Kaggle 竞赛、优化比赛、verifier-scored / metric-scored challenge、leaderboard 冲榜、成本最小化、电路/编译/求解器类赛题），把逐位复现的代理指标、预注册+kill 条件、汇率定价、多 agent研究循环（multi-agent research loop：研究/设计 vs 编码 vs 对抗评审）、情报收割与按任务拼装、第三方代码审查+断网沙箱、集群作业与发布纪律、跳出局部最优的外循环串成一条流水线；适合已有或将有 GOAL.md / research-state.yaml 的多周竞赛项目，而非写论文的通用 autoresearch 或单纯的代码复现。
metadata:
  source: kiki-custom-skill original; adapted ideas from bogoconic1/Qgentic-AI (MIT) and HKUSTDial/Supervisor-Skills (CC-BY-4.0)
  local-profile: kiki-custom-skill
disable-model-invocation: true
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Kaggle 冲榜战役（kaggle-leaderboard-campaign）

一套从长期 Kaggle 优化战役（Google Quantum AI 电路编译赛，三题几何平均，23.906 → 26.16）提炼的工作流，
融合了开源框架 Qgentic-AI（bogoconic1/Qgentic-AI，MIT）的若干设计。核心信念：**分数只有经官方 verifier
原样复验才算数；大收益来自结构性改变和组件收割，而不是无止境的微调。**

## 何时用 / 何时不用

| 用这个 skill | 改用 |
|---|---|
| 有官方 verifier 或 metric 源码、分数可本地复现的竞赛/优化任务，周期以周计 | 一次性跑个 baseline：`research-code-autopilot` |
| 多个子任务（per-task 成本）、要拼装组合包、要冲榜/守榜 | 写论文的端到端科研：`0-autoresearch-skill`（本 skill 借用其双循环和 state 文件，但目标是**榜单分**而非 paper） |
| 需要多 agent并行、集群作业、第三方 notebook 审查 | 只评估一个 idea：`idea-evaluator`；只审结果可信度：`experiment-integrity-audit` |

与 `0-autoresearch-skill` 的分工：沿用它的 `research-state.yaml` / `research-log.md` / `findings.md` /
`experiments/<slug>/protocol.md` 骨架；本 skill 追加 verifier 复现门槛、汇率定价、收割拼装、沙箱、发布门槛和
“跳出框架”外循环。两者不要同时作为主 skill。

## 角色与模型分工

| 角色 | 模型 | 职责 | 产出 |
|---|---|---|---|
| Orchestrator（主线程） | 最强模型 | 读 state、选题、写 brief、**复核子 agent结论**、决定 keep/pivot、对用户汇报 | `research-log.md` 行、state 更新 |
| Researcher / Designer | 强模型（Opus 级） | 文献、下界推导、新架构设计、定价 | `literature/distill/*.md`、设计稿 |
| Coder / Runner | 可用较快模型 | 按 spec 实现、提交集群作业、记录 JSON | `experiments/<slug>/`、`data/runs/<label>/` |
| Adversarial Reviewer | 独立agent，不给它你的结论 | 找错：规则违背、运气、算错汇率、泄漏/盲区利用 | review 结论（sound / rules_respected / passes） |
| Security Reviewer | 独立agent + Orchestrator 自己 grep 复核 | 第三方代码审查 | `sandbox/<name>/REVIEW.md` |

规则：**agent汇报，Orchestrator 核实**。子 agent的数字在进入 findings 或发布前，至少复核一处关键环节
（重算汇率、读它的 JSON、grep 它审查过的代码）。Brief 自包含：目标、已排除项、文件绝对路径、答案形状、长度上限
（模板见 `references/templates.md` §7）。不把“理解”外包：先自己综合，再写 spec。

## 流水线（9 个阶段）

每阶段：输入 → 输出（文件）→ 完成判据。文件模板见 `references/templates.md`。

### S1 Bootstrap 与基线逐位复现
- 输入：赛题页面、metric 源码、官方 verifier、最佳公开基线。
- 做：缓存规则/metric/榜单到 `research/`；写评测壳 `src/<x>_eval.py`，**原样**调用官方 verifier（不改一行）；
  固定一组预声明 salt/seed（如 9 个）；在本机和集群各复现一次基线。
- 输出：`GOAL.md`（目标、里程碑、验收条件、约束、须用户确认的动作）、`research-state.yaml`、
  `research-log.md`、`findings.md`、`data/runs/baseline-*/`（完整 verifier JSON）。
- 完成判据：代理指标与官方/公开分**逐位一致**（或差值已解释，如 local 23.90600 vs LB 23.91005）；
  在此之前不做任何优化。

### S2 情报收割（Intel harvest）
- 输入：公开榜、最新高分 notebook、论坛、队友分支、论文。
- 做：拉榜快照；缓存 notebook 为文本（只读不执行）；对每个公开/队友组件抽出**分任务成本**，与我们逐题 diff；
  用榜单算术反推领先者的分任务上限（“领先者三题乘积 ≈ X，我们 ≈ Y，需再 ×1.41”）。
- 输出：`research-log.md` 中 `intel` 行、`research-state.yaml: leaderboard_snapshots`、`literature/distill/*.md`。
- 完成判据：每个子任务都知道“公开最好 / 队友最好 / 我们”三个数，以及差距来自哪种机制。
- 节奏：至少每周一次；已知的公开窗口（奖项截止、notebook 必须公开日）前后每天一次。

### S3 Idea backlog 与定价
- 输入：S2 的差距表、成本模型、下界。
- 做：按 `references/idea-research.md` 跑三段式：**发散**（每个子任务 10–20 个候选，至少 4 个透镜，
  一半以上是结构性的）→ **收敛**（先查致命缺陷，再做两句话测试、定价、范式转变探针）→ **精炼**（产出 S4 草稿）。
  写成本模型与**汇率表**（例：1 qubit = 814.8 T；10 Toffoli = 0.77% 而不是 0.12%）；每个 idea 给出预测
  收益、成功概率、所需算力、盈亏预算（“Q 降到 880 可多花 29,329 T”）；按期望 ΔGM/天 排序。
  明确区分合法的计分杠杆和 verifier 盲区（后者永不做）。
- 输出：`literature/distill/SYNTHESIS.md`（排序 backlog）、`cost_model.md`、state 中 `hypotheses`。
- 完成判据：Top-5 都有数值价格和最便宜的否证检查；全部近期 idea 加总的上限已算出（若够不到下一个里程碑，
  立即在 backlog 中加入结构性/收割类条目）。

### S4 预注册
- 输入：选中的 idea。
- 做：在任何作业之前写 `experiments/<slug>/protocol.md`：假设、机制、预测（数值区间）、kill 条件、
  “跑完才判”的声明、决策表（结果落在哪个区间 → 做什么）。后续 Addendum 可细化预测，**不能放宽 kill 规则**。
- 输出：`protocol.md` + `research-log.md` 一行 `pre-registration`。
- 完成判据：协议时间戳早于第一个作业；决策表覆盖所有结果区间。

### S5 构建与测量（集群）
- 做：所有重活走作业提交器（资源上限硬编码在提交器里，如“不超过集群总量一半”）；GPU 更快就用 GPU；
  每个新版本脚本/输入**换新文件名**或在 pod 内校验 sha256；作业从挂载的项目路径读输入，不从 `/tmp`；
  **启动扫参前读一遍脚本自身的 assert、正则和 flag 前置条件**；作业 ID 立即登记到 state 的 `active_experiments`。
- 输出：`experiments/<slug>/results/`、`data/runs/<label>/*.json`、`analysis.md`。
- 完成判据：方法跑到**最终官方数字**；探针只用来排序，不用来判死刑；失败、无增益、未被检验（作业崩溃）三者分开记。

### S6 固定 salt 验证
- 做：候选在全部预声明 salt 上跑官方 verifier，取均值；随机失败型指标照实计入每一次失败；
  用配对 seed 拆分“结构性收益”和“运气”（例：-0.121% 里只有 -0.019% 是结构性的）；零容忍任务至少加一个交叉 salt。
- 输出：`data/runs/<label>/`、组合分 `score --taskA X --taskB Y`。
- 完成判据：满足 `GOAL.md` 验收条件；从未挑 salt、从未针对 salt 反复试。

### S7 对抗评审
- 做：独立 reviewer（不看你的结论，只看代码、协议、JSON）检查：协议是否先于运行、规则是否遵守、数字是否可追溯、
  汇率是否算对、是否利用了 verifier 盲区。Orchestrator 再亲自抽查一处。
- 输出：review 记录（log 中 `review` 行）。
- 完成判据：`sound=true, rules_respected=true, passes_acceptance=true`；非阻断问题已记录。

### S8 发布 / 汇报
- 做：**先告诉用户**新分数和分任务证据；累计增益达到推送门槛才开分支（`improve/<date>-<metric><score>`，
  从 `main` 新开，永不提交 `main`）；以用户的 git 身份提交（提交前查 `git config user.email` 是否正确）；
  包含提交包、evidence、性能 JSON、方法说明、可运行的生成源码、SHA256SUMS、第三方署名。
  外部提交/公开发布/组队一律需用户明确批准。
- 输出：分支 + log 中 `PUSHED` 行 + state `best_*` 更新 + `findings.md` 表格新行。
- 完成判据：用户已收到汇报；分支可复现提交包的哈希。

### S9 外循环：跳出框架 + 再收割
- 触发：每约 5 个实验或 2 天；或连续两轮无增益；或 backlog 中最好的 idea 价格 < 0.5% 时。
- 做：(0) 用 `references/idea-research.md` 的“隐藏约束清单”和“否定与反转”透镜重写一遍 backlog；(1) 重新推导各任务下界和“领先者必然用了什么”；(2) 重跑 S2；(3) 至少立一条**不同架构**的线
  （从零生成器、换表示、换算法族），与微调线并行；(4) 按任务拼装当前所有最好的组件（自己的、队友的、公开的）
  并重新九盐验证；(5) 决定 DEEPEN / BROADEN / PIVOT，写入 `outer_loop` 和 `pivot_assessments`。
- 完成判据：backlog 重排；至少一条结构性条目进入 S4。

## 循环控制

- **自检节拍**：经用户批准后每 20–30 分钟唤醒一次：读 GOAL/state/findings → 查作业和子 agent → 登记结果 →
  推进下一项。会话级定时器会随会话结束，提醒用户重启。
- **并行**：每个子任务一条独立工作流，子 agent只写自己的 `experiments/<slug>/`；跨任务不互相阻塞；
  合并只在 Orchestrator 处进行。不要给运行中的工作流内的agent发消息（会复活第二个实例）。
- **停止/转向**：kill 条件命中 → 关闭并记负结果；连续两轮外循环无增益且 backlog 已空 → 回到文献/下界重新构思，
  不空转；用户说暂停 → 跑完当前轮次、不再提交新作业。
- **调研 vs 迭代**：调研只在某个执行步被具体问题卡住时开；已在跑的调研跑完后立刻转成 build-and-measure。
- **权限**：子 agent被权限系统拒绝的动作，Orchestrator 不代为执行，交给用户。

## 记录规范

- 标签：VERIFIED（官方函数/JSON 或确定性读取自己的字节）、CLAIMED（他人所说）、INFERRED（自己推算，附算式）。
- `research-log.md` 只追加；错了写 `correction` 行指向原行，不改历史。
- 行类型：bootstrap / decision / intel / pre-registration / inner-loop / CANDIDATE / NEGATIVE / correction /
  review / incident / PUSHED / event。
- 每个数字都能追溯到 `data/runs/` 中某个 JSON。

## 反模式（每条都付过学费，详见 `references/lessons.md`）

1. 复现基线之前就开始优化；或用非官方的“近似”打分器挑候选。
2. 选最幸运的 salt/seed；把失败运气算成结构收益。
3. 用早期探针或外推宣判方法死亡；或反过来，协议写在运行之后。
4. 不定价就动手；汇率算错一个数量级（brief 里的“10 Toffoli ≈ 0.12%”实为 0.77%）。
5. 只记正结果；把“作业崩溃未产出”记成“负结果”。
6. 相信子 agent的“解锁/通过”而不复核（log 187 → 188 更正：漏算了第 9 个输出，门槛未过）。
7. 连续数天在同一族内微调（每步 <0.3%），而结构性重写（队友从零写的测量式反算生成器，invsqrt 97,922 → 86,217，约 -12%）和组件拼装一直没做。
8. 在本机运行下载来的代码；或只隔离文件不隔离网络。
9. 原地覆盖共享存储上的脚本；作业读 `/tmp`；扫参前不读脚本自身的 assert/正则/flag 前置条件。
10. 未经批准提交榜单、公开 notebook、提交到 `main`、或以错误的 git 身份提交。

## 参考文件

- `references/idea-research.md`：竞赛版 idea 调研（发散 9 透镜、致命缺陷审查、两句话测试、定价表、范式转变探针、透镜选择对照、陷阱）。
- `references/templates.md`：GOAL.md、research-state.yaml、protocol.md、log 行、REVIEW.md、发布提交/汇报、agent brief 模板。
- `references/qgentic-comparison.md`：从 Qgentic-AI 借鉴了什么、哪里不同、为什么。
- `references/lessons.md`：具体战例及其产生的规则。
