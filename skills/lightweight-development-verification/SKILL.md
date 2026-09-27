---
name: lightweight-development-verification
description: Use when planning, implementing, reviewing, testing, building, linting, running E2E, checking generated-file hashes, or coordinating subagents for software changes where validation should match risk and duplicate gates should be avoided.
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Lightweight Development and Verification

## Overview

Deliver reliable changes with the smallest workflow that covers the actual risk. Batch related work, reuse valid evidence from unchanged code states, and concentrate independent review and full validation at risk boundaries, milestones, and final delivery.

This skill expresses a personal workflow preference. Apply it by default when it is compatible with higher-priority user, repository, safety, and compliance instructions.

## Plan Functional Batches

Create a small number of functional or module-level batches. Do not turn every edit into a separate task. For each batch state:

| Field | Required decision |
|---|---|
| Scope | Files, module, or behavior expected to change |
| Risk | Low, medium, or high, with one-line reason |
| Minimum validation | Smallest check covering the changed behavior |
| Independent review | Yes or no, with the triggering risk |

Use these defaults:

| Risk | Typical changes | Development validation | Review |
|---|---|---|---|
| Low | Copy, CSS, static content, tests, local function, one/few files | Self-review plus focused test or page check; explain when no test is useful | None |
| Medium | Related cross-module change, shared type/config/dependency/route/interface | Focused tests expanded to affected consumers | At most one combined batch review when a review trigger below applies |
| High | Architecture, public API, auth, security, payment, privacy, irreversible migration, persistence/data loss | Expanded unit/integration validation for the named risk | Specialized review and formal gate |

Temporarily increase rigor for flaky or nondeterministic failures, suspicious integration behavior, or an explicit strict-review request. Return to the default level when the risk is resolved.

## Implement and Validate Locally

Let one implementer complete several tightly related edits. During development:

- Run the affected component/module test for component changes.
- Run the corresponding unit test or test file for local logic.
- For copy, CSS, or static content, prefer a page inspection or no automated test when a test would not cover a real risk.
- Expand validation for shared types, configuration, dependencies, routes, build configuration, and cross-module contracts.
- Do not automatically pair every small fix with a full test suite and full build.

Before any command, answer:

1. What risk will this command detect?
2. Has relevant code, input, configuration, or dependency state changed since a successful run?
3. Has another agent already run this exact command successfully on the same code state?

If the state is unchanged and the evidence is trustworthy, reuse it. Evidence is fresh when it was produced after the last relevant change; it does not have to be rerun in the current message or by every agent.

## Review at Risk Boundaries

Use implementer self-review by default. Dispatch an independent reviewer only when at least one condition holds:

- core architecture, public interfaces, security, permissions, payments, privacy, migrations, persistence, or data-loss risk changed;
- the change crosses modules and its local impact is hard to bound;
- two consecutive fixes did not solve the same issue;
- a defined milestone is complete;
- final delivery needs one whole-change review;
- the user explicitly requests strict review.

Batch roughly three or four related small tasks before a review when a review is warranted. Perform one combined requirements-and-quality review for the batch. Do not run separate, overlapping specification and quality reviews.

Have the current implementer fix minor findings and run focused validation. Start a re-review only if the fix introduces a new substantive risk, a high-risk/load-bearing finding remains, or the first review cannot verify the correction from the evidence. Do not create a review loop merely because a template contains one.

## Place Formal Gates Sparingly

A normal subtask may continue when implementation is complete, its focused validation passed or the lack of a useful test is explained, no blocking error is known, and the scope matches the goal.

Use formal gates only after:

- a high-risk architecture/module batch;
- a runnable functional milestone;
- the final delivery.

Full tests, a complete build, full lint, and E2E belong at milestones or final delivery, selected according to the project and the risk. After roughly three or four related subtasks, run at most one justified stage-wide test/build. If final validation fails, fix the issue, run the affected checks, then run one final complete validation again.

## Limit Hash Checks

Use hashes only for deterministic generation, transfer integrity, or suspected accidental changes:

- once at first import/generation when relevant;
- once for the final generated output or delivery;
- additionally only when output nondeterminism, overwrite, or mismatch is suspected.

One repeat-generation comparison is enough for the same inputs and generator version. Do not hash ordinary source, style, or test edits.

## Coordinate Agents Efficiently

- Assign by module or functional batch, not tiny steps.
- Reuse one implementer for related work; do not default to separate spec and quality reviewers.
- Prefer event completion or waits of two to five minutes when no dependent work is ready. Do not poll every 30 seconds or repeatedly nudge an unchanged agent.
- Read project rules once and retain a summary unless the files change or a conflict appears.
- Use `rg` for focused discovery. Inspect `git status` and `git diff` once after a batch, not after each patch.
- Give reviewers the changed files, relevant context, and existing command evidence. Do not ask them to rescan the repository or repeat successful checks on the same state.

## Interaction With Heavy Workflow Skills

When this skill and a heavy workflow skill both apply:

- **Subagent-Driven Development:** group related work into functional batches. Per-task implementers, dual-verdict task gates, and automatic re-review loops are strict-mode tools, not defaults.
- **Requesting Code Review:** review once per warranted batch, milestone, or final change. Combine requirements and quality in one review.
- **Verification Before Completion:** keep evidence-before-claims, but select evidence by claim, risk, and relevant code state. Reuse successful evidence when no relevant state changed.

Use strict mode only for a named high-risk condition, an unresolved repeated failure, or an explicit user request. State the reason when escalating.

## Final Delivery Contract

Before final delivery, perform one whole-change review and one complete, project-appropriate validation. Include lint or E2E only when the project or changed risk requires them. Inspect final status and diff once.

Report:

- completed functionality;
- focused tests actually run;
- milestones where full tests, build, lint, or E2E ran;
- duplicate validations deliberately skipped;
- independent reviewers used and why;
- hash checks used and why;
- remaining known risks.
