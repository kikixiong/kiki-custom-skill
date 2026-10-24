---
name: research-wiki-organization-prompts
description: 提供知识库组织、论文摄入、领域地图和研究空白整理流程。
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

# Research Wiki Organization And Prompts

Use this skill to build and operate a disciplined research wiki for idea generation and paper accumulation. The original author used a private source PDF that is not included in this collection. The workflow and scaffold below are self-contained; do not look for that author-local PDF.

## Core Structure

The PDF's central design is:

```text
your-research-wiki/
├── CLAUDE.md
├── raw/
│   ├── papers/
│   ├── notes/
│   └── assets/
└── wiki/
    ├── index.md
    ├── log.md
    ├── overview.md
    ├── papers/
    ├── concepts/
    ├── entities/
    ├── comparisons/
    ├── gaps/
    │   ├── confirmed-gaps.md
    │   ├── hypotheses.md
    │   └── questions.md
    └── synthesis/
        ├── field-map.md
        ├── shared-assumptions.md
        └── discussion-[date].md
```

`raw/` is read-only source material. `wiki/` is agent-maintained structured knowledge. Good answers should be written back into `wiki/` so research understanding compounds.

## Workflows

- `Ingest`: raw paper markdown -> wiki paper page -> related concept/entity updates -> gap/question updates -> index/log.
- `Query`: read index first, answer from relevant pages, write useful comparisons or synthesis back.
- `Lint`: detect orphan pages, contradictions, stale claims, high-frequency missing concepts, and gap status changes.
- `Idea generation`: read shared assumptions and confirmed gaps, propose hypotheses, challenge them with counterexamples, and write consensus into hypotheses.
- `Multi-model debate`: prepare a shared discussion note with wiki excerpts, prior conclusions, and roles for external web search and counterexample hunting.

## Scaffold

When the user wants a new research wiki, run:

```bash
python3 @@KIKI_SKILLS_DIR@@/research-wiki-organization-prompts/scripts/scaffold_research_wiki.py PATH
```

Then adapt `CLAUDE.md` or `AGENTS.md` in that project if needed.

## Output Rules

- Prefer durable wiki files over chat-only summaries when a project path is obvious.
- Preserve confidence labels: `high`, `medium`, `low`.
- Preserve hypothesis status: `draft`, `testing`, `confirmed`, `rejected`.
- Do not claim a research gap is confirmed without a cited comparison or direct literature evidence.
