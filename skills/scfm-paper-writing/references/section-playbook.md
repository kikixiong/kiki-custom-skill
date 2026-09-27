# Section-specific retrieval and adaptation

Use these as optional argument shapes, not fixed paragraph counts. Source IDs
resolve through the manifest; PDF page numbers always mean physical pages.
Geneformer and scVI use archived HTML heading units and anchors instead.

## Abstract

Retrieve `--section abstract` with the actual task and mechanism.
Choose the biological capability first, then the concrete obstacle, method action,
decisive test and bounded outcome. A benchmark paper should name the tested
assumption; an embedding paper should name the representation's intended use;
a perturbation paper should name the held-out axis. Avoid opening every abstract
with a generic success-of-LLMs paragraph, even when exemplars do so.

## Introduction

Useful routes:

| Writing problem | Start with | Transferable move |
|---|---|---|
| Cell embedding objective versus reconstruction | scconcept; zero-shot; scgpt | Establish intended use, inspect what the loss supervises, then specify the remaining criterion |
| Why change the token or attention unit? | cellplm; screbound; uce | Identify a biological/data property before presenting architecture |
| Limited data and biological discovery | geneformer | Move from an experimentally consequential bottleneck to transfer and validation |
| Probabilistic modeling and nuisance factors | scvi | Motivate each variable and assumption from the measured process |
| Heterogeneity in perturbation response | state | Explain the measurement obstacle before defining a population-level task |
| Fair, useful benchmarking | scbenchmark; zero-shot | Link a criticized assumption to a controlled comparison |

Use: biological need -> operational failure -> closest existing response ->
remaining gap -> evidence-backed insight -> method actions -> scope of evaluation.
Do not convert a critical benchmark's conditional failure into a theorem that
reconstruction cannot learn cell biology. Compare auxiliary objectives and readouts.

## Related Work

Group by the scientific decision at issue: expression-value/rank inputs,
gene/cell attention units, gene reconstruction/cell metric objectives,
technical-condition handling, or the relevant transfer regime. Avoid a chronology
of names with no comparison criterion. Include direct competitors even when they
weaken the initial novelty story. Cite original methods for their details; a
benchmark's description can contain simplifications or refer to older checkpoints.

## Method

Retrieve `--section method` with a narrow operation, then read full definitions.
Useful specification order: measured input -> mapping/selection -> transformed
values -> tokens -> encoder/readout -> objectives -> training stages -> inference.
Define what an index ranges over: genes, cells, biological samples, experiments,
or optimization minibatches. State missing measured genes separately from zeros.

For contrastive work, specify panel construction and its sharing across cells,
positive identities, negative pools, self-pair exclusion, similarity normalization,
temperature, symmetry and onset/schedule. Distinguish ontology supervision from
self-supervised cell identity. Do not assume every InfoNCE formula has the same
denominator. Borrow scConcept's definition-before-loss approach, not its formula
without checking our implementation.

For biological priors, name their provenance and statistical role. A protein
similarity graph, co-expression graph, ontology and experimentally validated
regulatory network are distinct objects. For STATE-like work, separate embedding
pretraining from transition learning and define the observation unit and split.

## Experiments / Results

Organize by the promised capability and the evidence needed to test it:
representation quality; transfer regime; mechanism ablation; efficiency if claimed;
biological validation if claimed. Each subsection should contain the question,
setup/comparator, observation, interpretation and boundary.

Use CellPLM's explicit research questions as an organizational example, the
zero-shot evaluation paper for transparent target-data baseline access, and STATE
for explicitly defined context/perturbation splits. These are writing examples,
not permission to inherit their settings or numbers.

For a causal component claim, use the matched ablation and identify residual
changes. A paper that swaps tokenizer, corpus, loss and architecture simultaneously
supports whole-system evidence unless additional controls isolate the component.

## Figures and captions

Retrieve `--section caption`; render the selected PDF page. Build a motivation
figure around an observed failure, and a framework figure around inputs, shared
states, objectives and inference outputs. Captions must specify what panels
establish, encodings, comparison regime, metric direction, replicate unit and
uncertainty. UMAP separation is illustrative; it does not establish a metric-space
claim or mechanistic biological validity. Never infer a caption's writing quality
from extracted text with scrambled panel labels.

## Discussion / Conclusion

Use supported capability -> interpretation -> demonstrated limits -> concrete next
test. Keep additional species/modalities, causal biology and clinical translation
as future work unless measured. A known limitation should constrain the Abstract
and Introduction too. The limitations in scGPT and the zero-shot evaluation paper
are useful examples of delimiting pretraining and downstream utility.
