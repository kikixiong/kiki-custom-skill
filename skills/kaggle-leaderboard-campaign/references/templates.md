# 模板

占位符用 `<...>`。所有模板中的数字字段都要能追溯到 `data/runs/<label>/` 的 JSON。

## 1. GOAL.md

```markdown
# GOAL — <竞赛名>

> 自主迭代的总纲。每轮先读本文件、research-state.yaml、findings.md。目标或约束变化只改本文件，并在 research-log.md 记一笔。

## 1. 目标
- 最终截止：<UTC 时间>。最终分 = <metric 定义，原文引用 metric 源码行号>。
- 代理指标：<eval 壳路径> 原样调用官方 verifier（<路径@hash>），<随机任务>取 <N> 个预声明 salt 均值，<确定任务>取开发 salt + 1 个交叉 salt。
- 基线：<分数>，<日期> 在本机和集群逐位复现；对应公开榜 <分数/名次>。
| 任务 | 资源 | 成本 | 倍率 |
|---|---|---:|---:|

## 2. 里程碑（每周重新拉榜校准）
| 里程碑 | 本地分 | 约等名次 | 成本乘积需下降 | 日期 |
- 汇率：任一任务成本降 1% ≈ +<Δ> 分。

## 3. 新 best 验收条件
1. 原样运行官方 verifier 并通过；随机任务全部预声明 salt；零容忍任务另加交叉 salt。
2. 通过 metric 的文件/格式检查（eval 壳已复刻）。
3. 证据可追溯：data/runs/<label>/ 完整 JSON；同步 findings.md、research-state.yaml。
4. 有可运行的生成源码（获奖交付要求）；不透明产物只能做对照或非最终提交。

## 4. 约束
- 规则：<账号数、组队、外部数据、署名>。
- 须用户确认：榜单提交、公开发布、组队/合并、超出算力上限、规则含义不清处。
- 算力：<提交器路径>；上限 <如：不超过集群总量一半>；GPU 更快就用 GPU；本机只做轻量检查（≤ <n> 进程）。
- 外部代码：审查（sandbox/<name>/REVIEW.md，Verdict: APPROVED）→ 断网沙箱作业；产物视为不可信数据。
- 诚信：不挑 salt、不刷 seed、不改 verifier、负结果同样记录、不利用 verifier 盲区。

## 5. 工作方式：内循环 / 外循环 / 自检节拍 / 并行流
## 6. 当前计划（引用 SYNTHESIS.md 排名）
## 7. 汇报与停止（推送门槛 <Δ>；上一次推送 <分支@commit, 分数>；新分支命名；停止条件）
```

## 2. research-state.yaml

```yaml
project: {title: "<>", question: "<>", status: active, started: "<date>", deadline: "<UTC>"}
baseline:
  label: <label>
  source: <repo@commit (artifact sha256)>
  local_score: <float>
  reproduced: "<date>, local (<py/libs>) and cluster (<py>); identical costs"
  tasks: {<task>: {cost: <>, ratio: <>, <resource fields>}}
milestones:
  - {id: M1, local_score: <>, due: "<date>", status: open}
official_scores:          # 每次榜单提交：本地分 vs LB 分，用于校准
  - {archive: <sha8>, submission: <id>, public_score: <>, note: "local <> calibrates to LB <+Δ>"}
leaderboard_snapshots:
  - {date: "<>", first: <>, tenth: <>, best_public_notebook: <>, teams: <>}
team_upstream: []         # 队友分支/提交，及其分任务构成
hypotheses:               # 排序 backlog 的镜像
  - {id: <ID>, statement: "<可证伪的陈述，含数值门槛>", status: pending|testing|supported|refuted|inconclusive, priority: high|medium|low, price: "<预测 Δ%，ΔGM>", result: "<一句话 + label>"}
experiments:
  proxy_metric: "<定义>"
  best_value: <float>
  best_labels: {<task>: <label>}
  best_branch: <branch@commit>
  last_pushed: {branch: <>, score: <>, next_push_threshold: <>}
  trajectory:
    - {run_id: <label>, hypothesis: <ID>, metric_value: <>, delta: <>, change_summary: "<>"}
active_experiments:       # 关闭时把 id 改成 <id>-DONE
  - {id: <slug>, type: subagent|workflow|manual, hypothesis: <ID>, started: "<UTC>", jobs: [<job ids>], stall_threshold_min: 300, watch_path: experiments/<slug>/}
outer_loop: {cycle: <n>, last_direction: DEEPEN|BROADEN|PIVOT, last_reflection: "<>", next_due: "<date>"}
pivot_assessments: []
compute: {cluster: "<提交器与上限>", local: "<限制>"}
```

## 3. experiments/<slug>/protocol.md（预注册）

```markdown
# <slug> protocol — pre-registration (<UTC 时间，早于任何作业>)

绑定规则：GOAL.md §3 §4 §7。标签：VERIFIED / CLAIMED / INFERRED。后续 Addendum 可细化预测，不得放宽 kill 规则。

## 参照（VERIFIED）
<当前 best 的 label、sha256、分任务成本、来源 JSON 路径>

## 假设
<一句可证伪的陈述>

## 机制
<为什么会省；改哪个文件哪一行；与已关闭方向的区别>

## 定价（INFERRED，附算式）
- 汇率：<1 单位资源 = x% 成本>；预测 Δ成本 <区间>，ΔGM <区间>，成功概率 <p>。
- 盈亏预算：<若资源 A 降 n，可多花 m 单位资源 B>。

## 运行
<脚本/作业命令、资源、seed 来源（复用已有 seed 或预声明），预计时长>
- 前置检查：脚本自身的 assert/正则/flag 前置条件已读：<列出与本次参数相关的>。
- 跑到完成：<最终官方数字的定义>；中途数字只作信息。

## Kill 条件
<最便宜的否证检查 + 阈值>；命中即关闭并记 NEGATIVE。

## 决策表
| 结果区间 | 动作 |
|---|---|
| <≤ a> | BUILD / 进入 S6 |
| <a..b> | 需额外满足 <条件> 才继续 |
| <> b> | 关闭 |

## 结果（运行后追加，不改上文）
## Addendum <n>（<UTC>）
```

## 4. research-log.md 行

```markdown
| <#> | <date> | <type> | **<一句结论，含数字和 VERIFIED/INFERRED>**
  - 证据：<label / job id / JSON 路径 / sha8>
  - 对比：<vs 当前 best / vs 预测>
  - 决策：keep | pivot | escalate；下一步 <>。 |
```
类型：bootstrap / decision（写明用户原话）/ intel / pre-registration / inner-loop / CANDIDATE / NEGATIVE /
correction（“更正 log <#>：……”）/ review / incident / PUSHED / event。负结果和“未被检验”（作业崩溃）分开写。

## 5. sandbox/<name>/REVIEW.md（第三方代码）

```markdown
# Review: sandbox/<name>, revision <n>

Reviewer: <agent/人>, <UTC>. 相关协议：<路径与章节>。上一修订：<sha8，批准过的作业 id>。

## 1. 来源
<URL / notebook / 分支@commit，作者，许可证（记录即可，是否阻挡按 GOAL.md），获取日期>

## 2. 文件与改动
<复制文件数、是否原样；我们新增的文件逐个列 sha256 和功能>

## 3. 逐类检查（每个 .py 都 grep 过 + 入口手读）
| 类别 | 结果 |
|---|---|
| 网络（socket/requests/urllib/http） | |
| 子进程（subprocess/os.system/popen） | |
| 动态执行（eval/exec/compile/__import__ 非常量） | |
| 反序列化（pickle/np.load allow_pickle/torch.load） | |
| 环境变量/凭据读取 | |
| 写自身目录外的文件 | |
| 混淆/编码载荷 | |

## 4. 风险评估与运行方式
<只经 `<提交器> sandbox --name <name>`；断网命名空间 + fail-closed 出网检查；产物在单独作业中用我们的 eval 验证>

## 5. Orchestrator 复核
<独立 grep 命令与结果摘要>

## 6. 文件清单（MANIFEST.sha256 的 sha256：<>）

Verdict: APPROVED | REJECTED
```

## 6. 发布：提交信息与给用户的汇报

提交信息（英文，提交前确认 `git config user.name/user.email` 是用户身份）：
```
<task(s)>: <one-line change>, local <metric> <old> -> <new>

- <taskA>: <label> cost <old> -> <new> (<Δ%>), <N>/<N> salts PASS
- <taskB>: unchanged (<label>)
- Evidence: evidence/<label>/*.json; submission.zip sha256 <>
- Generator: <path>; third-party parts credited in NOTICE.md
<attribution lines required by the environment>
```

给用户的汇报（中文，先汇报再推送）：
```
新结果：本地 <metric> <new>（上次推送 <old>，+<Δ>；推送门槛 <thr>：达到/未达到）。
| 任务 | 旧成本 | 新成本 | Δ% | 证据 |
来源：<哪些是我们的 / 队友的 / 公开的，署名>
验证：<N> 个预声明 salt 全部 PASS；结构性收益 vs 运气拆分：<>；独立评审：<结论>。
风险：<源码闭环、不透明产物、规则疑点>。
待你决定：<是否推送分支 / 是否提交榜单 / 是否公开>。
```

## 7. Agent brief

```markdown
## 目标
<一句话 + 可度量的通过标准（如：在 <参照> 上 mean T ≤ <x>，九盐全 PASS）>

## 背景（你看不到我的对话）
- 当前 best：<label、成本、文件绝对路径>
- 已排除：<方向 + 证据路径>，不要重做。
- 规则：<GOAL.md 相关章节；不运行下载代码；重活经 <提交器>；只写 <experiments/slug/>>

## 要读的文件
<绝对路径 + 行号范围>

## 交付
- 形状：<表格 / 3–5 个候选带价格 / 代码补丁 / yes-no + 一段理由>，长度上限 <>。
- 每个数字标 VERIFIED / CLAIMED / INFERRED；汇率写出算式。
- 先写 protocol.md 再提交任何作业；方法跑到最终官方数字再下结论。
- 作业 id 写入 <路径>，以便你中断后作业仍可被接管。
```
