---
name: creating-research-meeting-reports
description: Use when preparing a pre- or post-meeting research brief from notes, drafts, slides, tables, logs, or meeting decisions for supervisor, lab, project, or research-review discussions.
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Creating Research Meeting Reports

Write a concise, decision-ready Markdown report by default. Organize it around the research decision, not source chronology. Adapt the problem-driven logic from Enyan Dai's [Individual Meeting Guideline](https://enyandai.github.io/guidelines/individual-meeting/).

Use this for substantive research reasoning before or after a supervisor, lab, project, or research-review meeting. Do not use it for calendar scheduling, administrative minutes, generic standups, or routine status summaries with no research question or decision.

## Build the report

1. Extract only supplied evidence. Label statements as **Evidence**, **Inference**, **Proposal**, or **Unknown**. Surface conflicts, failed hypotheses, negative results, and protocol caveats; never turn correlation or a routine loss curve into a mechanistic conclusion.
2. Open with one to three concrete feedback requests, decisions, or questions. State one-sentence motivation and name both the in-scope problem and a meaningful out-of-scope claim or unknown.
3. Name the supported major challenge and, only if supported, a minor challenge. A challenge is an evidenced named obstacle or uncertainty, not a purpose phrase reverse-engineered from a component name. Map each claimed component or contribution to that named challenge only when the notes support why it exists. Otherwise write **Challenge mapping: Unknown** and include this explicit item under Decision requests: **Meeting question: What evidenced obstacle or uncertainty motivates [component name(s)]?**
4. Add an explicit method/mechanism section. For each component, state **Component**, **Supplied operation**, **Challenge mapping**, **Mechanism evidence**, and **Missing definition or test**. Use an equation only when supplied evidence supports its terms, or label it a proposed discussion form and expose undefined terms.
5. For every included research question, use the literal labels **Claim**, **Setting**, **Motivation**, **Observation**, **Interpretation**, **Limitation or confound**, and **Decision enabled**. Keep unavailable fields explicit rather than filling them with plausible detail.
6. Include draft or slide changes only when they would clarify the research logic. Include a next-week table only when future work is proposed, requested, or agreed; every row has **Task**, **Reason**, and a concrete **Deliverable**.

Use this compact shape, omitting genuinely inapplicable sections rather than inventing content:

“Short” or “concise” changes sentence length, not the contract: keep the explicit method/mapping fields and all seven labels for every included RQ.

```markdown
# Meeting report
## Decision requests
## Motivation and boundary
## Challenges and contribution mapping
## Method and mechanism
## Evidence by research question
## Draft or slide changes
## Meeting record
## Next-week plan
| Task | Reason | Deliverable |
```

For a pre-meeting report, lead with requested feedback and label proposed decisions and actions **Pending**. For a post-meeting report, separate **Recorded decisions** (meeting evidence) from **Analysis and recommendations** (agent-derived); preserve open questions and convert agreed work to the next-week table.

Evidence calibration: if metric A exceeds B but A used a larger batch size and a different pooling rule, report the measured comparison and the protocol confound; mark the superiority claim **Unknown** pending a matched comparison.

## Quick reference

| Evidence state | Write |
| --- | --- |
| Directly supplied or measured | **Evidence** |
| Reasoned consequence | **Inference** |
| Suggested action or framing | **Proposal** |
| Missing support or definition | **Unknown** |

## Common mistakes

- Mapping a component to “create views” or “provide negatives”: those are purpose phrases, not evidenced obstacles. Name the supported obstacle or write **Unknown** and ask why the component is needed.
- Omitting one RQ field because it is unavailable: retain the explicit label and write **Unknown**.
- Treating a normal loss curve as mechanism evidence: report the curve as an observation and the mechanism as **Unknown**.
- Inventing next-week work to complete the template: omit the table when no future action is applicable.
- Mixing PI decisions with recommendations: separate recorded meeting evidence from agent-derived analysis.
- Collapsing a short report into free-form evidence/interpretation/recommendation prose: compress each required field to one line instead; do not remove the mapping question, method fields, or RQ labels.

## Formal artifacts

First synthesize the finished research content. When the requested deliverable is `.tex`, an Overleaf-ready project, or a compiled PDF, **REQUIRED SUB-SKILL:** Use creating-elegantpaper-reports. Pass it the completed content; let that skill package and verify the artifact.
