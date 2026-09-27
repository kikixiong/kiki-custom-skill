---
name: scfm-paper-writing
description: Write or revise single-cell foundation model papers using a local, section-aware literature library. Retrieve close scFM exemplars, compare scientific positioning, and adapt argument structure to the user's evidence; use alongside kiki-paper-writing for scGPT, Geneformer, cell representations, contrastive pretraining, or perturbation-model manuscripts.
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Single-cell foundation model paper writing

Use this as the domain layer over the installed `kiki-paper-writing` skill. Read its
`SKILL.md` and the relevant section workflow; retain its priority of evidence,
logic, paragraph role, terminology, then style. This skill contributes a real
local retrieval library, domain distinctions, and source-grounded writing moves.
It does not authorize experiments or manuscript synchronization.

## Start with a writing request

Identify the target section, scientific question, actual method, evidence available,
and intended venue. Read [section-playbook.md](references/section-playbook.md)
for the requested section and [domain-checks.md](references/domain-checks.md)
for scientific boundaries. Read [project-bridge.md](references/project-bridge.md)
only for SCBenchmark/CoCoS work.

The paper library is configured in [library.json](references/library.json).
It lives outside the skill so original PDFs are not duplicated into the skill.
The library's `manifest.json` records source URLs, exact local versions, selection
rationale, and curated section page windows. [paper-cards.md](references/paper-cards.md)
contains short reading notes. These are selection aids, not substitutes for sources.

## Retrieve before drafting a substantial section

Run from this skill directory, or use the script's absolute path:

```bash
python3 scripts/library.py search "contrastive disjoint views cell embeddings" --section introduction --top 3
python3 scripts/library.py search "sampling gene expression objective" --section method --top 3
python3 scripts/library.py search "frozen annotation batch generalization" --section experiments --top 3
python3 scripts/library.py read scconcept --pages 29:32
```

Search uses local BM25 lexical retrieval over curated section windows. It requires
no embedding model, accelerator, network service, or research checkpoint. English
technical terms are preferred; common Chinese terms are expanded automatically.
It returns distinct papers, page locators, selection tags, source/version information,
and a short excerpt. Geneformer and scVI have archived full-text HTML with heading
units and anchors instead of PDF pages; use the returned `read --units` command.
`--paper ID` restricts a paper. `--include-project` explicitly
allows the user's CoCoS draft, excluded by default to avoid circular evidence.

1. Retrieve typically 2-4 distinct papers. Prefer a close mechanism/problem match
   and a relevant evaluation paper; venue prestige alone does not rank relevance.
2. Read the retrieved section and neighboring paragraphs using `read`. Page
   windows may overlap adjacent sections; HTML units may also include subsequent
   unheaded text. Check the named heading and the preserved source location.
   For equations, figures, captions or two-column ordering, inspect the PDF visually.
3. Rerank by problem, mechanism, evaluation regime, and target section's job.
   Return no forced match when the corpus has no useful precedent. Search primary
   literature or state the gap; do not claim semantic exhaustiveness for lexical RAG.
4. Create a short adaptation note: source and pages; paragraph job; transferable
   argument; nontransferable scientific assumptions; the user's matching evidence.
5. Draft from the user's claim-evidence ledger. Reuse reasoning organization, not
   distinctive sentences, paragraph paraphrase chains, source results, or novelty claims.
6. Audit the draft against its closest competitor and its actual protocol. Keep
   literature claims, our results, and proposed tests explicitly distinct.

For short copy edits, reuse an already inspected source packet when relevant;
do not repeat retrieval without a change in section, claim, or evidence.

## Deliver what the writing turn needs

For substantive writing, provide the draft and a compact provenance note naming
the exemplars, sections/pages, structure borrowed, and material evidence gaps.
Scientific citations belong in the manuscript where claims rely on prior work.
A rhetorical exemplar is not automatically a scientific citation. Do not output
long source excerpts in the draft. Preserve accepted text and version history.

## Maintain the library

See [library-maintenance.md](references/library-maintenance.md) for ingestion,
version checks, index rebuilding, and limitations. Adding literature means
obtaining a legitimate public source, inspecting its identity and section
boundaries, and updating the manifest. Download success is not reading completion.
Do not label papers Best Paper or Test of Time without an official award source.
Classic background methods, representative scFMs, close competitors, and critical
benchmarks serve different purposes and must retain those labels.

## External paper library on a new machine

The source PDFs and private literature index are not bundled. Configure `KIKI_SCFM_LIBRARY` or pass `--library /actual/library/path` to `scripts/library.py` before library-dependent work. Do not guess a Mac Desktop path. The self-contained Kiki writing guidance remains available without that external corpus.
