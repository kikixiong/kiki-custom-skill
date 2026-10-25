---
name: coding-router
description: 软件开发与 GitHub 请求的总入口：仓库/PR/issue、CI 失败修复、review 意见、提交推送开 PR、代码结构与重构、测试验证强度、学术主页/GitHub Pages、接手项目、科研代码复现。先用它再按表读取具体 skill
---

# 软件开发与 GitHub 请求 Router

本分类的叶子 skill 已设为仅显式调用（Claude Code：frontmatter `disable-model-invocation: true`；Codex：`agents/openai.yaml` 中 `policy.allow_implicit_invocation: false`），不在自动列表里。本 skill 是它们的二级目录。

## 用法

1. 按下表选 1 个主 skill（必要时加 1～2 个辅助）；拿不准时看“默认选择”和“不用于”列。
2. 用文件读取工具读取 `@@KIKI_SKILLS_DIR@@/<目录名>/SKILL.md`，按其正文执行。**不要**通过技能调用机制加载叶子（Claude Code 的 Skill 工具会因仅显式调用而失败）。
3. 叶子正文里的相对路径（`references/`、`scripts/`）按该 SKILL.md 所在目录解析；叶子要求“调用某 skill”时同样改为 Read 其 SKILL.md。
4. 正文含 Codex 专有能力（Codex MCP、原生 imagegen、`~/.codex`、automation API）时：在 Codex 中照常使用；在 Claude Code 中换成等价物（Agent 子代理、本地脚本），没有等价物就告诉用户。
5. 用户点名某 skill（Claude Code 输入 `/名字`，Codex 输入 `$名字`）时直接用它。选定后告诉用户“用的是 X”。
6. 请求属于其他分类时改读对应 router：`paper-router`、`research-router`、`experiment-router`、`ml-train-router`、`ml-infer-router`、`llm-app-router`、`ml-domain-router`、`quant-router`、`meta-router`。

标记：⚠C = 含 Codex 专有用法；重 = 多阶段重型流程，仅在用户明确要求时用。

## 默认选择（没有特殊信号时）

| 请求 | 默认 |
|---|---|
| 看一下这个 PR/issue/仓库 | `github` |
| CI 挂了帮我修 | `gh-fix-ci` |
| 处理 PR 的 review 意见 | `gh-address-comments` |
| 提交并推送开个 PR | `yeet` |
| 写/重构一段代码 | `lean-modular-coding` |
| 这个项目现在什么情况 | `project-intake-autopilot` |

## GitHub 协作

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `github` | GitHub 总入口：浏览仓库、PR/issue 分诊与摘要、查看 PR patch、评论/标签、已推送分支建 PR | CI 失败改用 gh-fix-ci；处理审查意见改用 gh-address-comments；提交推送发 PR 改用 yeet |
| `gh-fix-ci` | GitHub Actions/PR checks 失败：拉取 job 日志、定位原因并修复代码 | PR 审查评论改用 gh-address-comments；本地测试策略改用 lightweight-development-verification |
| `gh-address-comments` | 处理 PR review 意见：拉取 reviewThreads、按文件归类可执行意见、确认范围后逐条修改 | CI 红了改用 gh-fix-ci；仅摘要 PR/issue 改用 github |
| `yeet` ⚠C | 明确要求一键发布：建分支、暂存、commit、push 并开草稿 PR | 分支已推送只需建 PR 或看 PR 改用 github |

## 编码规范

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `lean-modular-coding` | 写/改/重构/评审任意语言代码时控制结构：入口精简、按职责拆模块、避免过度抽象与防御代码 | 测试/构建/lint/审查强度怎么定改用 lightweight-development-verification |
| `lightweight-development-verification` | 规划改动批次与验证强度：按风险选测试、build、lint、E2E、审查，避免重复门禁，协调 subagent | 代码结构与模块拆分改用 lean-modular-coding；CI 日志修复改用 gh-fix-ci |

## 网站维护

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `academic-homepage-maintainer` | 维护学术个人主页/项目页/论文列表：Jekyll、静态 HTML、React/Vite/Next、GitHub Pages | 论文正文写作改用 paper-router；通用 PR 操作改用 github |

## 项目接手

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `project-intake-autopilot` | 接手陌生本地项目“看看”：读 README/计划/依赖/入口，分类项目类型，给出现状与下一步 | 已明确是科研训练评估代码要推进改用 research-code-autopilot |

## 科研代码

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `research-code-autopilot` | 科研代码改造：训练/评估脚本、复现、seed/配置、结果日志、在已授权的执行环境中运行实验与故障处理 | 首次摸清项目改用 project-intake-autopilot；纯代码风格改用 lean-modular-coding |
