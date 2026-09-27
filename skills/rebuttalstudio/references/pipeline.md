# RebuttalStudio Pipeline

Adapted from `runtsang/RebuttalStudio`.

## Five Stages

1. `Breakdown`: convert reviewer feedback into atomic weaknesses, questions, and requests.
2. `Reply`: outline point-by-point responses before writing polished paragraphs.
3. `First Round`: compile the first-round rebuttal in the target venue format.
4. `Multi Rounds`: handle follow-up reviewer discussion, clarifications, and new issues.
5. `Final Remarks`: summarize the rebuttal outcome and close remaining points.

## Codex Use

This local skill is a text and workflow adapter, not the Electron editor itself. Use it to organize review comments, draft evidence-grounded responses, and produce copy-pastable OpenReview/CMT text. If the user explicitly asks to run the RebuttalStudio app, inspect or install the upstream Node project separately.
