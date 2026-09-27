---
name: analyze-results
description: 分析实验数据、统计差异并生成对比表和结论。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Analyze Experiment Results

Analyze: $ARGUMENTS

## Workflow

### Step 1: Locate Results
Resolve the actual run and evaluation configuration from its manifest. Default experiment host: `cnic-ps` (hostname `ps`). For scbenchmark/scGRAIN use `/data1/jiaqi/scREBOUND/runs/<run_id>`; other projects use their recorded result directories.
- Analyze raw experiment data and run statistical/data checks on the remote host.
- The Mac may read small exported aggregate tables and prepare reports/figures; it must not run model/data experiments, probes or replacement evaluations.
- Reuse already saved metrics. Preserve seed, split, metric definition and data/weight provenance; do not infer them from filenames alone.

### Step 2: Build Comparison Table
Organize results by:
- **Independent variables**: model type, hyperparameters, data config
- **Dependent variables**: primary metric (e.g., perplexity, accuracy, loss), secondary metrics
- **Delta vs baseline**: report absolute delta with metric direction; include relative improvement only for a meaningful nonzero baseline

### Step 3: Statistical Analysis
- If multiple seeds: report mean +/- std, check reproducibility
- If sweeping a parameter: identify trends (monotonic, U-shaped, plateau)
- Flag outliers or suspicious results

### Step 4: Generate Insights
For each finding, structure as:
1. **Observation**: what the data shows (with numbers)
2. **Interpretation**: why this might be happening
3. **Implication**: what this means for the research question
4. **Next step**: what experiment would test the interpretation

### Step 5: Update Documentation
If findings are significant:
- Propose updates to project notes or experiment reports
- Draft a concise finding statement (1-2 sentences)

## Output Format
Always include:
1. Raw data table
2. Key findings (numbered, concise)
3. Suggested next experiments (if any)

