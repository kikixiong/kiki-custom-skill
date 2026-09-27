# Scientific distinctions that change the writing

## Representation and objective

- A gene embedding and a cell embedding are different outputs. Name the readout.
- Geneformer-style masked gene identity prediction over ranked input is not
  continuous masked-expression regression. Local within-cell ranking is also not
  corpus-normalized ranking. Specify the model version and normalization.
- A loss may train a cell embedding through a reconstruction decoder without
  directly imposing pairwise cell geometry. Inspect the actual objective before
  claiming there is no cell-level supervision. scGPT, UCE and STATE offer concrete
  reasons to make this distinction (see their mapped Method sections).
- A transformer over gene tokens is different from attention over sets of cells.
  Inter-cell context can affect the meaning of independent-sample evaluation.
- Lack of intrinsic gene order does not by itself prove transformers inappropriate.
  An encoding may introduce an explicit biological or expression-derived order.
- Do not equate a good reconstruction score with useful frozen representations,
  or a good annotation score with perturbation-response understanding.

## What is observed, held out, and trained?

Before comparing methods record: input layer (raw counts/normalized values/ranks),
candidate gene set and mapping loss, sampling/truncation, pretraining corpus and
overlap, checkpoint identity, readout, downstream normalization, target-data access,
trainable parameters, split unit, selection set, metric and replicate unit.

- Frozen features plus a trained linear head is a linear-probe evaluation. State
  both facts; do not imply that no target labels were used.
- A pretrained encoder can be zero-shot while a comparison method is fit on the
  target dataset. This may be a useful practical comparison, but disclose it.
- Unseen cells, donors, studies, tissues, species, perturbations and unseen
  perturbation-context combinations are different generalization claims.
- An annotation label may be derived or coarse; agreement with it is not independent
  experimental validation. Ontology or cell labels in pretraining count as supervision.
- Matched-input and native-input whole-system tables answer different questions.
  Do not silently replace an unavailable native input with adapted processed data.

## Biological interpretation

Co-expression, attention, embedding similarity, interaction enrichment, perturbation
response and causal regulation require different evidence. Predicting an edge in
a curated GRN benchmark does not make the pretraining graph a causal GRN. An
in-silico deletion is a model intervention, not automatically a cellular intervention.
Preserve the validation scope of the original paper when discussing such results.

Do not treat all observed zeros as technical dropout, unmeasured panel genes as
biological zeros, batch mixing as biological conservation, or a batch label as
purely technical when it is confounded with disease, donor or cell type.

## Metrics and statistical language

- Explain accuracy/macro-F1 and class imbalance; do not confuse macro over classes
  with equal averaging over datasets.
- Report the source of SD: split/head seeds, pretraining seeds, donors or datasets.
  SD is not a confidence interval. Cell counts are not independent donor counts.
- For perturbations distinguish absolute expression from deltas, all genes from
  DE genes, response magnitude from perturbation identity, and the DE selection
  procedure from model fitting. Include meaningful simple controls when warranted.
- For GRN metrics record edge universe, negatives, direction and known-label coverage;
  AUROC and AUPRC have different sensitivities to class prevalence.
- Efficiency claims need hardware, batch size, sequence length and inclusion of
  preprocessing/decoding. A paper's maximum reported speedup is not a general constant.

## Novelty and source calibration

The library is curated rather than exhaustive. Before a headline novelty claim,
check the closest mechanisms and current primary literature. Foundational status
does not make every sentence in a paper a reusable scientific rule. Preserve
historical versions and mark unverified publication decisions or awards explicitly.
