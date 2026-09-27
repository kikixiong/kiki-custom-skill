# Reading cards: choose an argument, then read its source

These are original analytical notes, not quotations or performance rankings.
Page locators refer to the exact PDFs in `manifest.json`. Only the listed sections
were inspected for writing analysis; the corpus is not an experimental audit.
No official Best Paper or Test of Time award is asserted for these papers.

## geneformer — biological bottleneck to experimental validation

**Read:** archived HTML introduction in unit 15; architecture unit 17;
rank encoding unit 34; embedding definitions units 40-42; treatment analysis
units 28-29; Discussion unit 30. These are HTML units, not PDF pages.

**Argument:** limited disease-specific data motivates transfer from broad
observational data; computational predictions lead to targeted biological tests.

**Use:** ground the need for transfer in a concrete experimental constraint;
explain what information the encoding preserves and sacrifices; separate model
predictions from subsequent experimental validation.

**Boundary:** ranks use corpus-normalized expression, not simply raw within-cell
order. The original objective predicts masked gene identities. The reported
experimental validation concerns selected targets and disease models; it does
not establish that every attention edge is causal or every embedding is clinically
validated. The full author-manuscript HTML is archived; PDF download was blocked
by website verification and is not claimed as acquired.

## scvi — classic statistical modeling argument

**Read:** archived HTML Introduction unit 10; probabilistic model unit 21;
inference unit 22; modeling choices unit 24; Discussion unit 19.

**Argument:** technical variation and uncertainty motivate explicit latent
variables and a likelihood, then a shared model supports several analyses.

**Use:** justify a mathematical assumption by the property it models; distinguish
generative specification from approximate inference; explain the role of each
nuisance variable before reporting downstream utility.

**Boundary:** this is a classic task-fitting representation model, not a pretrained
scFM. Historical likelihood choices are not universal prescriptions for modern
assays. Target-data fitting and batch-label access must remain visible in a
comparison against frozen encoders. The archived source is HTML; no formal
Test of Time award or acquired publisher PDF is asserted.

## scgpt — representative foundation-model narrative

**Read:** opening pp. 1-2; Results pp. 2-10; Methods pp. 12-19;
Discussion p. 10; Figure 1 p. 3.

**Argument:** increasing data diversity motivates reusable pretraining, followed
by distinct adaptations for different biological tasks. The Methods separate
gene identities, expression values and conditions before defining objectives.

**Use:** connect each type of input information to its modeling role; separate
universal pretraining from task-specific adaptation in the paper structure.

**Boundary:** annotation in the main results involves model fine-tuning. Do not
reuse that evidence as frozen-probe performance. The Discussion explicitly limits
zero-shot behavior under technical variation. Inspect reconstruction through the
cell embedding before claiming absent cell-level training. Do not adopt the
paper's broad biological language without corresponding project evidence.

## scconcept — closest cell-view contrastive comparison

**Read:** Introduction pp. 2-3; model narrative pp. 3-4; Methods pp. 29-33;
Discussion pp. 19-20.

**Argument:** the intended downstream object is the cell representation, which
motivates a cell-level identification task and panel-robust representations.
The paper connects cross-technology challenges to view construction and encoding.

**Use:** explain the exact discrepancy between proxy objective and downstream use;
define cell views before the contrastive loss; connect invariances to use cases.

**Boundary:** disjoint panels, within-view negatives and direct cell contrast are
already present. Do not claim them as first contributions. Local gene ranking,
technology transfer and replacing reconstruction differ from retaining numerical
expression with a joint reconstruction objective. These differences need matched
evidence before being called improvements. The supplied source is a preprint.

## screbound — efficiency and supervision-aware structure

**Read:** Introduction/Related Work pp. 1-3; overview and compression pp. 3-4;
contrastive regularization and stages pp. 4-6; experiments pp. 6-9.

**Argument:** token cost and batch variation motivate distinct mechanisms, then
efficiency and representation tests evaluate those mechanisms.

**Use:** map bottlenecks to method components; distinguish architectural compression,
batch conditioning and representation regularization in the exposition.

**Boundary:** the contrastive regularizer uses cell-label ontology information;
it is not purely self-supervised cell-instance contrast. Staged training is prior
art but is not identical to every onset policy. Do not import the reported speedup
without its hardware and timing scope. The downloaded submission says under review;
it does not establish acceptance, an award, or clinical readiness.

## scbenchmark — data properties lead to controlled comparisons

**Read:** Introduction pp. 1-2; adaptations pp. 3-4; benchmark/task tables pp. 4-7.

**Argument:** properties of expression measurements motivate sampling and architecture
comparisons, followed by common downstream evaluations.

**Use:** make a motivation figure pose questions that the experimental tables answer;
define a common comparison protocol rather than narrating isolated scores.

**Boundary:** a high expression value is not universally more biologically important.
Historical table settings do not override the project's later frozen protocol.
The supplied title differs in word order from the repository's published citation;
verify proceedings metadata for the bibliography. This is the project's baseline
paper, not an independent validation of the current CoCoS extension.

## state — measurement constraints motivate the prediction unit

**Read:** Introduction pp. 2-4; task definitions pp. 19-20; ST pp. 21-25;
SE pp. 25-29; Figure 2 pp. 7-8.

**Argument:** destructive measurement prevents observing a cell's paired before/after
state; heterogeneity motivates prediction over populations, with separate embedding
and transition modules.

**Use:** introduce the unobservable quantity before its operational approximation;
define what a held-out context means before claiming generalization.

**Boundary:** the context-generalization and zero-shot-adaptation tasks permit
different training information. Neither is automatically unseen-perturbation
prediction. SE uses reconstruction through cell embeddings, which matters when
criticizing reconstruction objectives. Read its loss definitions rather than
inferring the mechanism from a label such as cell-level loss. This corpus uses v1;
the author repository links a newer v2, not inspected here.

## uce — biological use case connects to the representation interface

**Read:** Introduction pp. 1-2; Figure 1 p. 2; Methods pp. 10-11;
case study p. 7 and Discussion pp. 7-8.

**Argument:** extending an embedding space to new datasets motivates reusable
representations, biological token information and explicit input construction.

**Use:** state what a user can do with the embedding; explain input flexibility
through the representation's actual mechanism; separate exploratory visualizations
from analyses on the full embedding.

**Boundary:** sampling with replacement and protein-derived inputs differ from
SCBenchmark's input adapter. An embedding-space biological hypothesis is not itself
causal validation. The mapped source is the 2026 Nature article; the separately
downloaded earlier preprint is archival and excluded from default retrieval.

## cellplm — conference method and experiment organization

**Read:** Introduction pp. 1-2; Related Work pp. 2-3; Method pp. 3-6;
research questions p. 7 and task comparisons pp. 7-9.

**Argument:** changing the conditioning information from one cell to multiple
cells motivates a different token unit; explicit research questions organize tests.

**Use:** contrast conditional distributions before introducing modules; distinguish
pretraining and fine-tuning; connect experiment subsections to research questions.

**Boundary:** attention over cells changes context dependence. Several task tables
separate zero-shot, from-scratch and fine-tuned variants; maintain that distinction.
The timing table excludes preprocessing and decoding and uses different batch
sizes. Such a speed comparison needs its conditions. Some baseline scores are
imported from earlier work, not all rerun in a common pipeline.

## zero-shot — critical evaluation with an explicit boundary

**Read:** Background pp. 1-2; Results pp. 3-5; Conclusions pp. 6-7;
Models and baselines pp. 7-8; metrics pp. 9-10.

**Argument:** test the promised representation directly, compare useful simple
alternatives, then delimit what the observed failures imply.

**Use:** state the target capability and chosen evaluation regime early; disclose
target-data access by baselines; identify corpus overlap as a limitation.

**Boundary:** the findings cover selected model versions, datasets and tasks.
They do not show that every scFM or reconstruction objective fails. scVI and
Harmony are fit on target datasets while foundation encoders are frozen; this is
a practical-system comparison. Use the original model Methods for precise
tokenization details rather than treating this benchmark's summary as canonical.

## scfoundation — challenge-to-design correspondence

**Read:** Introduction pp. 1-2; framework pp. 2-4; Methods pp. 14-18;
Discussion pp. 13-14 of the downloaded preprint.

**Argument:** corpus diversity, long gene inputs and read-depth differences motivate
data collection, asymmetric computation and a corresponding pretraining task.

**Use:** make the architecture answer a specified data constraint; describe source
and target depth separately; distinguish gene and pooled cell outputs.

**Boundary:** downstream models operating on frozen representations are not necessarily
linear probes. The downloaded file is a 2023 preprint, not the verified 2024
journal version. Scale and superiority statements are historical author claims;
do not adopt them as current rankings or as evidence for our own method.

## cocos — project manuscript, excluded by default

Use the supplied v1 only as a revision target. Its text, figures and historical
tables do not independently verify its own claims. Check current project records
before adopting its method variant, baseline labels or scores. See
[project-bridge.md](project-bridge.md) for the identified version boundary.
