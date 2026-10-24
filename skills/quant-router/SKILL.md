---
name: quant-router
description: 量化金融研究的总入口：因子/alpha、IC、回测审查、未来函数、聚宽 JoinQuant、组合风险归因、数据管线时点、AI 量化论文与 idea。先用它再按表读取具体 skill
---

# 量化金融研究 Router

本分类的叶子 skill 已设为仅手动调用（`disable-model-invocation: true`），不在自动列表里。本 skill 是它们的二级目录。

## 用法

1. 按下表选 1 个主 skill（必要时加 1～2 个辅助）；拿不准时看“默认选择”和“不用于”列。
2. 用 Read 读取 `@@KIKI_SKILLS_DIR@@/<目录名>/SKILL.md`，按其正文执行。**不要**用 Skill 工具调叶子（已禁止模型调用，会失败）。
3. 叶子正文里的相对路径（`references/`、`scripts/`）按该 SKILL.md 所在目录解析；叶子要求“调用某 skill”时同样改为 Read 其 SKILL.md。
4. 正文含 Codex 专有能力（Codex MCP、原生 imagegen、`~/.codex`、automation API）时换成 Claude Code 等价物（Agent 子代理、本地脚本）；没有等价物就告诉用户。
5. 用户点名某 skill 或 `/名字` 时直接用它。选定后告诉用户“用的是 X”。
6. 请求属于其他分类时改读对应 router：`paper-router`、`research-router`、`experiment-router`、`ml-train-router`、`ml-infer-router`、`llm-app-router`、`ml-domain-router`、`coding-router`、`meta-router`。

标记：⚠C = 含 Codex 专有用法；重 = 多阶段重型流程，仅在用户明确要求时用。

## 默认选择（没有特殊信号时）

| 请求 | 默认 |
|---|---|
| 量化需求不明确、想先分派 | `quant-research-routing` |
| 验证一个因子/信号是否有效 | `factor-alpha-lab` |
| 回测收益太好，检查是否可信 | `backtest-integrity-audit` |
| 帮我找 AI 量化 idea / 最近有什么 paper 能做 | `quant-ai-research-autopilot` |
| 检查数据是否有未来函数、复权或时点问题 | `quant-data-pipeline-audit` |
| 分析持仓组合的风险暴露与收益归因 | `portfolio-risk-attribution` |

## 总入口

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `quant-research-routing` | 量化请求的首个入口：不确定该走因子、回测、数据、组合、聚宽还是 AI 论文流程时先用它分派 | 需求已明确时直接用对应专项 skill |

## 因子研究

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `factor-alpha-lab` | 单个因子/alpha 信号从构造到验证：IC/RankIC、分位收益、衰减、换手、行业市值中性化、正交化 | 策略回测结果可信度审查改用 backtest-integrity-audit；组合层面暴露改用 portfolio-risk-attribution |

## 回测审查

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `backtest-integrity-audit` | 审查策略回测与绩效声明：未来信息/泄漏、幸存者偏差、涨跌停/T+1、交易成本、样本外与过拟合，按 Blocker/Major 分级 | 数据源时点与复权问题改用 quant-data-pipeline-audit；聚宽平台专用代码用 joinquant-research-workflow |

## 平台工作流

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `joinquant-research-workflow` | 聚宽 JoinQuant 专用：jqdata 研究脚本、initialize/handle_data/run_daily 策略、本地模拟聚宽回测 | 非聚宽平台的通用回测审查用 backtest-integrity-audit |

## 组合风险

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `portfolio-risk-attribution` | 持仓/目标权重层面：行业风格暴露、集中度、Brinson/因子收益归因、回撤、VaR/CVaR、优化约束检查 | 单信号有效性检验改用 factor-alpha-lab |

## 数据审查

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `quant-data-pipeline-audit` | 行情/基本面数据管线正确性：公告日 vs 报告期、复权混用、代码复用、期货换月、时区日历、point-in-time 连接、重复键与缺失 | 策略层面泄漏与成本审查改用 backtest-integrity-audit |

## AI量化文献

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `quant-ai-paper-scout` | 窄范围检索 AI/ML 时序与金融论文（NeurIPS/ICML/KDD/arXiv q-fin/SSRN），单篇精读，论文转可证伪 alpha 思路 | 宽泛的“帮我找 AI 量化 idea”全流程改用 quant-ai-research-autopilot |
| `quant-ai-research-autopilot` 重 | 宽泛 AI+量化研究总流程：找方向、论文到 idea 排序、查新、可行性评估、转实验设计并分派下游 skill | 只查论文或精读单篇用 quant-ai-paper-scout；纯因子验证用 factor-alpha-lab |
