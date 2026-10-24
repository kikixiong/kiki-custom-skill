---
name: self-improvement
description: Capture useful learnings from failures, user corrections, missing capabilities, outdated assumptions, and recurring workflow discoveries. Use when a command fails unexpectedly, the user says a prior answer was wrong, a better reusable pattern is found, or durable guidance should be promoted into AGENTS.md or a project learning log.
disable-model-invocation: true
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Self-Improvement

Keep a lightweight learning loop for Codex work without depending on OpenClaw hooks or sessions.

## Core Rule

When something teaches a reusable lesson, record it close to the work:

1. Prefer a project-local `.learnings/` directory when working in a repo or project.
2. Use `AGENTS.md` only for durable rules that should affect future Codex behavior.
3. Keep one-off facts in the current task context, not global memory.
4. Do not log secrets, tokens, passwords, private credentials, or unnecessary personal data.

## What To Log

Use this skill for:

- Command failures with a reusable cause or fix.
- User corrections such as "that's wrong", "不是这个", or "你搞错了".
- Missing tool or workflow capability that should be built later.
- Outdated assumptions about APIs, packages, docs, project layout, or user preferences.
- Better approaches discovered during a task that should be reused.
- Repeated quality issues that should become project rules.

Skip logging for:

- Trivial typos fixed immediately.
- Errors caused only by temporary network or external service downtime.
- Sensitive content that would create a privacy or security risk.

## Logging Targets

Create these files as needed:

```text
.learnings/
├── LEARNINGS.md
├── ERRORS.md
└── FEATURE_REQUESTS.md
```

Use `LEARNINGS.md` for corrections, better patterns, and durable preferences.
Use `ERRORS.md` for reproducible command/tool failures.
Use `FEATURE_REQUESTS.md` for capabilities the user wanted but Codex did not have.

## Learning Entry

Append this format to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-001] short-title

**Logged**: YYYY-MM-DD HH:MM
**Priority**: low | medium | high | critical
**Status**: pending | promoted | obsolete
**Area**: code | docs | tests | infra | research | workflow | user-preference

### Summary
One sentence describing the lesson.

### Context
What happened and why it mattered.

### Reusable Rule
The rule or habit Codex should apply next time.

### Promotion
- Target: AGENTS.md | project docs | skill update | none
- Related files:
```

## Error Entry

Append this format to `.learnings/ERRORS.md`:

````markdown
## [ERR-YYYYMMDD-001] command-or-tool

**Logged**: YYYY-MM-DD HH:MM
**Priority**: low | medium | high | critical
**Status**: pending | fixed | obsolete
**Area**: code | docs | tests | infra | research | workflow

### Error
```text
Paste the relevant error output only.
```

### Context
- Command:
- Working directory:
- Inputs:

### Root Cause
What actually caused the failure.

### Fix
What resolved it, or the next concrete thing to try.

### Prevention
What should be checked or changed to avoid recurrence.
````

## Feature Request Entry

Append this format to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-001] capability-name

**Logged**: YYYY-MM-DD HH:MM
**Priority**: low | medium | high | critical
**Status**: pending | built | rejected | obsolete

### Requested Capability
What the user wanted.

### User Context
Why it mattered.

### Possible Implementation
Skill, plugin, MCP connector, automation, script, or project change.
```

## Promotion Workflow

Promote only after the learning is stable and broadly useful:

- Put repo conventions, test commands, project workflows, and review expectations in `AGENTS.md`.
- Put task-specific facts in task notes or project docs.
- Put repeated procedural knowledge in a Codex skill.
- Put scheduled checks in Codex automations.

Before editing `AGENTS.md`, keep the change small and specific. Avoid turning a single failure into an overbroad rule.
