---
name: project-intake-autopilot
description: 接手现有项目，检查文件、识别当前状态并归纳下一步。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
disable-model-invocation: true
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Project Intake Autopilot

Use this skill to orient quickly in an unfamiliar local project and turn that orientation into an actionable next move.

## Workflow

1. Identify the project root:
   - Prefer the current directory if it contains `.git`, `README*`, `pyproject.toml`, `requirements.txt`, `package.json`, `paper/`, `submission/`, `scripts/`, or `configs/`.
   - If the user points to a top-level folder under `the user-specified project directory`, work inside that folder first.

2. Read only high-signal context:
   - `README*`, `MASTER_PLAN*`, `PROJECT_STATUS*`, `TODO*`, `CHANGELOG*`, `notes/*status*`, and recent summary files.
   - Dependency files: `requirements.txt`, `environment.yml`, `pyproject.toml`, `package.json`.
   - Entry scripts under `scripts/`, `src/`, `train*`, `eval*`, `run*`, `main*`.

3. Classify the project:
   - Research code: models, data, experiments, metrics, runs.
   - Paper project: LaTeX, notes, figures, tables, reviews.
   - Benchmark/challenge: official rules, baseline, data splits, submission scripts.
   - Website/release: GitHub Pages, project page, assets, deployment.
   - Quant research: data pipeline, factor, backtest, portfolio, risk.

4. Produce or execute the next useful action:
   - If the user asked to "看看", return a concise map: goal, current status, key files, likely next tasks, risks.
   - If the user asked to continue, implement one coherent improvement and validate it.
   - If blocked by external data/GPU/network, document the exact blocker and switch to an unblocked prep task.

## Commands

Prefer narrow commands:

```bash
pwd
git status --short
find . -maxdepth 3 \( -name README.md -o -name 'MASTER_PLAN*' -o -name 'PROJECT_STATUS*' -o -name requirements.txt -o -name pyproject.toml -o -name package.json \)
find . -maxdepth 3 \( -type d -name scripts -o -type d -name configs -o -type d -name notes -o -type d -name outputs -o -type d -name runs -o -type d -name results \)
rg -n "TODO|FIXME|next step|blocker|pending|claim|metric|submission|deadline" .
```

## Output Standard

Keep intake reports short and decision-oriented:

- Current purpose
- What is already done
- What is risky or missing
- Best next 3 tasks
- Exact command or file to start with

Do not rewrite project structure unless needed to complete the user's request.
