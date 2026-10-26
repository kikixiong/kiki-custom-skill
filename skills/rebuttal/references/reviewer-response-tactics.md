# Reviewer-response tactics

Adapted from user-provided peer experience. These are decision aids, not evidence
that a particular tactic will change scores. Actual reviews, paper evidence and
the current venue's rules take precedence. Use the relevant sections only.

## Prioritize decisive concerns while covering every reviewer

- Rank issues by scientific severity, explicit conditions for reconsideration,
  evidence available to resolve them, and the time needed. Among comparable
  issues, an answerable, high-confidence negative review can deserve early work.
  Do not assume persuading one reviewer will make others change their scores.
- Record statements such as "I would raise my score if X" verbatim in the issue
  board. Answer X directly and show the matching evidence; if only part is
  resolved, identify the remainder. Do not substitute unrelated improvements or
  imply that satisfying X guarantees a score increase.
- Low confidence does not mean a reviewer failed to understand the work or will
  be easy to persuade. Explain the disputed point clearly and ground the answer.
- Give supportive reviewers a brief thank-you and a substantive answer to their
  remaining questions. Use the venue's score definitions; "6 or above" is not a
  portable definition of a positive review.
- If several reviewers raise the same concern, elevate it as a shared issue and
  check both the method and the paper's explanation. Keep a response under each
  reviewer even when the evidence is shared.

## Make short replies independently useful

Preserve reviewer labels such as `R2-W1` and `R2-Q3`, or assign stable labels when
none exist. Use a short topic label rather than repeating the full question.
Keep the raw question and its mapping in the internal issue board.

Each response should contain a direct answer and enough evidence to understand
it. A cross-reference supplements that answer: name the exact reviewer, issue,
and table/section as applicable, and verify that the reader can access it.
If responses are private to individual reviewers, include the needed evidence
locally instead of relying on another thread.

For example, when supported by actual results: "R2-Q1: The alternate split
preserves the reported ordering; Table A below gives the results. Protocol
details are in our response to Reviewer R3, Q2." Do not copy this conclusion
without matching evidence, and never use only "see our response to others".

Compress experimental evidence into one small table when the venue allows it.
Keep the comparison, split/protocol, metric direction, actual number of seeds
and uncertainty needed to interpret the numbers. Use a plain-text table or
compact lines when rich formatting is unavailable. Cut repeated thanks and
questions before removing substantive answers, including supportive replies.

## Evidence and honest limitations

Lead with the answer and strongest relevant evidence, then state what that
evidence does and does not establish. Avoid opening with blanket apologies or
an unsupported claim that the whole work is weak. A confirmed error should be
acknowledged promptly and its effect explained; additional experiments are not
a reason to hide or postpone a material correction.

When new experiments would resolve an issue, propose the smallest informative
test within the deadline and resource constraints. Execution still requires
the user's authorization for that scope and the configured execution host.
Report negative or inconclusive results honestly. Separate completed evidence,
approved plans and untested limitations; do not present planned work as done.

## Common disputes

### A requested comparison appeared after submission

Verify the submission cutoff, the cited work's earliest relevant public version
and any earlier available version, using dated primary sources. Check the
venue's policy on concurrent work and rebuttal additions. If the timing supports
it, explain neutrally that it is concurrent or later work, acknowledge its
relevance, and state the precise relationship to the contribution. A later
publication date alone does not prove the work was unavailable at submission.
Do not use the timeline to dismiss a substantive overlap or fairness concern;
offer a feasible comparison or textual distinction when appropriate and allowed.

### Code and paper appear inconsistent

Inspect the exact revision, entrypoint, configuration and executed path used
for the reported results. Determine whether the disputed code is unused
exploration/ablation code, an equivalent implementation, or a real discrepancy.
Only explain it as exploration or a simplification when the evidence supports
that account; "the core method is consistent" also requires verification.
If the mismatch changes the algorithm, protocol or results, acknowledge it,
identify affected claims and propose the correction or authorized rerun. Do not
invent a post hoc rationale for the mismatch.

### Several reviewers challenge the data split or protocol

Treat repetition as a reason to investigate, not as proof that reviewers are
wrong. Cite primary protocol/benchmark sources if claiming the setup is common,
then explain why it fits this paper's scientific question. Common practice alone
does not rule out leakage or establish validity. Check relevant independence
boundaries, such as subject, dataset, time or site. Where feasible and authorized,
evaluate the suggested alternative while holding other factors comparable;
otherwise identify the evidence gap and limit the claim accordingly.

### More random seeds are requested than the deadline allows

Choose a feasible seed budget and selection rule before inspecting outcomes,
subject to existing experiment authorization. Report all completed runs, actual
`n`, the aggregation/variability measure, and incomplete or failed runs as
relevant. Do not cherry-pick favorable seeds or mix unmatched protocols. Label
partial evidence as partial; one run cannot establish variation across seeds.
Explain the deadline constraint briefly, without promising unavailable results
or claiming that the requested robustness check is fully satisfied.

## Learn from the original model's public discussion

For an extension of an existing model, the original paper's public OpenReview
reviews and rebuttal can reveal how similar questions were framed. Read them
when relevant and available; retain source links in the strategy notes. Reuse
useful reasoning patterns only after checking that the assumptions apply here.
The original authors' claims, results and reviewer acceptance are not evidence
for the extension. Do not copy unsupported claims or seek private reviewer data.

## A review appears to describe a different paper

First compare the alleged mismatch against the submitted version, supplement
and cited material. Distinguish a misunderstanding from clear signs of a
misassigned review. Preserve short concrete examples and prepare a neutral,
confidential note to the AC through the venue's designated channel, asking for
verification and guidance. Keep any applicable technical responses separate.

Draft the note for the user. Posting it or emailing organizers requires explicit
authorization; a skill invocation or a suspected mismatch does not authorize
contact. Use email only when venue guidance calls for it or the official channel
is inadequate, and then use the verified official contact. Do not speculate
publicly about reviewer identity or misconduct.
