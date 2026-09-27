---
name: lean-modular-coding
description: Use when creating, changing, refactoring, or reviewing code in any language, especially when work may produce oversized entry points, fragmented files, speculative abstractions, defensive scaffolding, or disproportionate testing.
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Lean Modular Coding

## Core Principle

Deliver complete behavior with cohesive modules and proportionate evidence. “Simple” means easy to understand and change, not fewer lines or files.

## Working Recipe

1. State the result, constraints, risks, and behavior that must remain.
2. Read the affected path and project conventions.
3. Trace one direct path; reuse inspected code, native capabilities, and installed dependencies.
4. Add only what current behavior, a binding gate, concrete consequential risk, or observed failure/repetition requires.
5. Organize by responsibility, implement, run the smallest decisive check, and stop.

Reuse scaffolding only when it reduces current complexity. Drafts, sunk effort, authority, “production-ready,” “future-proof,” and “best practice” do not justify machinery.

## Shape Modules by Responsibility

Keep entry points—`main`, `train`, commands, handlers, jobs—as outlines: parse, compose, invoke, present.

Split when parts have independent responsibilities or reasons to change and a coherent contract, or are independently reusable/testable. Keep small code together when extra navigation adds no boundary. Keep local helpers with their capability. Never split by line count, create one file per function, or add forwarding wrappers.

Example when all capabilities exist:

```text
train.py                 # parse, compose, run
training/config.py       # load configuration
training/data.py         # datasets and loaders
training/models.py       # model construction
training/loop.py         # training and optimization
training/evaluation.py   # only if evaluation is required
```

Do not pre-create callbacks, registries, checkpoint, distributed, compatibility, or configuration modules for hypothetical use.

## Admit Defenses by Evidence

Protect untrusted inputs, auth and permissions, money, material data integrity, irreversible effects, concurrency, public contracts, and observed transient failures. Risk must be task-specific and consequential; ordinary I/O or a possible future failure is insufficient.

Otherwise omit redundant validation, broad catch-and-rethrow, retries without observed transience, idempotency, and a bounded exit, checksums without an integrity contract, non-authoritative preflight, bug-hiding fallbacks, and compatibility paths without real legacy consumers. Handle expected errors at the owning boundary; let defects fail clearly.

## Verify in Proportion

| Change | Default evidence |
|---|---|
| Trivial text/config/obvious mapping | Diff; relevant syntax/format check if needed |
| Local non-trivial logic | One focused test, assertion, or run |
| Bug fix | One regression plus nearest tests |
| API/CLI/pipeline/integration | One representative path plus related tests |
| Security, money, migration, deletion, concurrency, integrity | Focused regression plus relevant integration/gates |

Start there. Add checks only for distinct requirements or material risks; do not mirror functions or modules. Use full suites, smoke tests, or preflight only when explicitly requested, mandated by the project, a shared foundation changed, or narrow evidence shows wider impact.

## Finish Check

- Does the requested path work?
- Did every addition earn its cost?
- Is the entry point an outline without file confetti?
- Does the evidence support the completion claim?

Explicit user requirements, safety rules, and mandatory project gates always win.
