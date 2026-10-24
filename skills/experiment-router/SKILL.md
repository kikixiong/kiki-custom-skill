---
name: experiment-router
description: 实验与科研代码的总入口：实验规划、结果分析、可信度审计、实验监控、训练检查、科研代码实现/复现、算法核验、项目进度、AutoDL、GPU/CUDA 排障、wandb/MLflow/SwanLab/TensorBoard。先用它再按表读取具体 skill
---

# 实验与科研代码 Router

本分类的叶子 skill 已设为仅手动调用（`disable-model-invocation: true`），不在自动列表里。本 skill 是它们的二级目录。

## 用法

1. 按下表选 1 个主 skill（必要时加 1～2 个辅助）；拿不准时看“默认选择”和“不用于”列。
2. 用 Read 读取 `@@KIKI_SKILLS_DIR@@/<目录名>/SKILL.md`，按其正文执行。**不要**用 Skill 工具调叶子（已禁止模型调用，会失败）。
3. 叶子正文里的相对路径（`references/`、`scripts/`）按该 SKILL.md 所在目录解析；叶子要求“调用某 skill”时同样改为 Read 其 SKILL.md。
4. 正文含 Codex 专有能力（Codex MCP、原生 imagegen、`~/.codex`、automation API）时换成 Claude Code 等价物（Agent 子代理、本地脚本）；没有等价物就告诉用户。
5. 用户点名某 skill 或 `/名字` 时直接用它。选定后告诉用户“用的是 X”。
6. 请求属于其他分类时改读对应 router：`paper-router`、`research-router`、`ml-train-router`、`ml-infer-router`、`llm-app-router`、`ml-domain-router`、`quant-router`、`coding-router`、`meta-router`。

标记：⚠C = 含 Codex 专有用法；重 = 多阶段重型流程，仅在用户明确要求时用。

## 默认选择（没有特殊信号时）

| 请求 | 默认 |
|---|---|
| 帮我看下实验跑得怎么样 | `monitor-experiment` |
| 训练是不是有问题/loss 不对 | `training-check` |
| 分析一下这些实验结果 | `analyze-results` |
| 继续推进这个科研项目 | `research-start-routing` |
| 这个结果靠谱吗 | `experiment-integrity-audit` |
| 加个实验追踪/记录指标 | `weights-and-biases` |

## 规划

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `experiment-plan` 重 | 方法已定，要设计实验矩阵、消融、评估协议、运行顺序和 GPU 预算来支撑论文主张 | 还在找 idea 改用 brainstorming-research-ideas/idea-evaluator；直接写代码用 research-task-executor |
| `ablation-planner` ⚠C | 主结果已经通过 result-to-claim（claim_supported 为 yes 或 partial），要规划消融；research-review 或审稿意见指出缺少消融；用户说“帮我设计消融”“审稿人会要哪些 | （论文类，也在 paper-router） |

## 结果分析

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `analyze-results` | 已有实验结果，要做对比表、mean±std、相对 baseline 的 delta、趋势与显著性结论 | 怀疑结果可信度用 experiment-integrity-audit；运行中进度用 monitor-experiment |
| `result-to-claim` ⚠C | 一批主实验刚完成，用户问“这些结果能不能支撑我的 claim”“这个结论要不要收窄”“还缺什么实验才能写进论文”，或者在写论文或 rebuttal 前要先确定可以主张的结论范围；结果有歧义、需要客观的第二意见时使用。 | （论文类，也在 paper-router） |

## 审计

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `experiment-audit` ⚠C 重 | 查 agent 生成结果是否造假：伪 ground truth、自归一化分数、无来源数字、范围夸大，需独立 reviewer | 常规数据泄漏/划分/基线公平检查用 experiment-integrity-audit |
| `experiment-integrity-audit` | 判断结果能否信：train/test 泄漏、划分、基线公平性、指标方向/平均方式、种子方差、可复现性 | 怀疑 agent 编造结果/伪标签用 experiment-audit；回测泄漏用 backtest-integrity-audit |
| `paper-claim-audit` ⚠C | 论文 LaTeX 已写好，本地也有结果文件，用户想确认“论文里的数字和表格是否和实验输出一致”“85.3% 是不是真的”“说 15% 提升算得对不对”“consistently outperforms 是否言过其实”；在 | （论文类，也在 paper-router） |

## 监控

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `monitor-experiment` ⚠C | 看正在跑的实验：远程 cnic-ps 日志 tail、进程/session 状态、已存 JSON/CSV 结果，单次快照 | 判断训练健康度（NaN/发散/停滞）用 training-check；AutoDL 实例用 autodl-experiment |
| `training-check` ⚠C | 基于 loss/eval/lr/grad norm 或 W&B run 判断训练是否 NaN、发散、停滞，给 CONTINUE/STOP 结论 | 只看日志进度用 monitor-experiment；CUDA/显存报错用 server-gpu-diagnosis |

## 科研编码

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `research-code-autopilot` 重 | 整体推进科研代码：读 README/入口脚本、训练评估脚本、复现论文结果、日志与故障处理 | 单个明确实现任务用 research-task-executor；算法正确性审查用 research-algorithm-checker |
| `research-algorithm-checker` | 对照论文/伪代码审查实现：张量 shape、dtype、索引、梯度/概率数值、边界、性能，维护 ISSUES.md | 通用代码 review 用 code-review；要直接实现功能用 research-task-executor |
| `research-task-executor` | 执行一个明确的科研代码/实验实现任务（加模块、改脚本、跑 smoke check）并更新任务记录 | 项目级统筹复现用 research-code-autopilot；先理清现状用 research-progress-tracker |

## 项目状态

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `research-progress-tracker` | 恢复/整理科研项目进度：维护 PROGRESS.md、PIPELINE.md、EXPERIMENTS.csv、ISSUES.md，给下一步 | 第一次接手陌生项目用 project-intake-autopilot |
| `research-start-routing` | 泛泛的“开始/继续推进科研项目”请求，先分派到进度、算法审查、任务执行或 GPU 诊断 skill | 需求已明确时直接用对应具体 skill |
| `project-intake-autopilot` | 接手陌生本地项目：读 README/依赖/入口脚本，判断是科研代码还是论文项目，归纳现状与下一步 | 已有进度文档的科研项目续做用 research-progress-tracker |

## 远程GPU

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `autodl-experiment` 重 | 在 AutoDL/SeetaCloud SSH 实例上启动、监控、排障、邮件通知、拉回结果，tmux/screen、conda/HF 配置 | 实例连接/磁盘/学术加速管理用 autodl-manager；cnic-ps 实验看 monitor-experiment |
| `autodl-manager` | 管理 AutoDL 实例：SSH 连接、有无 GPU 检测、磁盘告警、conda 初始化、网络加速、多实例 | 在实例上跑/监控训练任务用 autodl-experiment |
| `server-gpu-diagnosis` | 排查 CUDA 不可用、GPU 不可见、驱动/框架版本不兼容、显存 OOM、服务器环境问题（默认 cnic-ps） | 训练指标异常用 training-check；AutoDL 实例状态用 autodl-manager |

## 实验追踪

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `mlflow` | 用 MLflow 记录参数/指标/artifact、Model Registry 版本管理、模型部署、自建追踪服务 | 实时协作看板和 sweep 用 weights-and-biases；本地轻量用 tensorboard/swanlab |
| `weights-and-biases` | 用 W&B/wandb 自动记录、实时看板、超参 sweep、artifact 血缘、团队协作 | 需开源/自托管用 swanlab 或 mlflow；只要本地曲线用 tensorboard |
| `swanlab` | 用 SwanLab 做开源/本地/自托管实验追踪，记录标量和图片音频等媒体，国内友好 | 需 sweep 和团队看板用 weights-and-biases；需模型注册用 mlflow |
| `tensorboard` | 用 TensorBoard SummaryWriter 看 loss 曲线、直方图、模型图、embedding 投影、profiler | 需云端协作/sweep 用 weights-and-biases；需模型版本管理用 mlflow |
