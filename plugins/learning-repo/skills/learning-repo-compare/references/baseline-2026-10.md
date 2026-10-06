# Baseline: four books, October 2026 (protocol v1–v3)

The first run of this protocol, on four sibling learning repos. Use it as a reference point
for later runs (densities, planted-error sensitivity, token cost), not as a ranking: the
audits were not equally deep (see the caveat).

Every defect counted here was reported by two auditors independently, or by one and then
checked against the original repository by the orchestrator. Planted errors are excluded.

| Book | Audits | Prose words (approx.) | Confirmed defects | Per 10,000 words | Major | Planted errors found |
|---|---|---|---|---|---|---|
| data-lab | v1, 2 auditors | 26,000 | 8 | about 3 | 0 | 7 of 8 |
| optimization-lab | v3 lean, 1 auditor (Sonnet) | 11,000 | 4 | about 3.5 | 0 | 4 of 4 |
| rl-for-llms | v1 + v2, 4 auditors | 32,000 | about 26 | about 8 | 1 | 7 of 8 (v1), 7 of 8 (v2) |
| loss-functions-lab | v2, 2 auditors | 29,000 | about 41 | about 14 | 1 | 8 of 8 |

Overall sensitivity to planted errors: 33 of 36 (92%).

**Caveat.** The audits were not equally deep. rl-for-llms had four full reads and
loss-functions-lab two v2 full reads, while data-lab had two v1 reads and optimization-lab one
lean read. More reading finds more minor defects, so the densities are comparable in order of
magnitude, not to one decimal place. The two v2 books would likely score lower if audited as
lightly as the others, and vice versa.

## What it shows

1. **Process did not buy correctness.** data-lab, built with the most structure (spec,
   gates, audits), and optimization-lab, built with little, have the same low density.
   loss-functions-lab has the highest.
2. **What distinguishes the books is verifiability.** data-lab writes its numbers from
   scripts and names a test for most claims; optimization-lab computes its results in
   executable cells and names tests in the prose. Both had few numeric errors. rl-for-llms and
   loss-functions-lab type their numbers by hand; most of their wrong numbers were typed
   values that drifted from the script output.
3. **The common defects are not computational.** Across all four books the bulk were
   cross-references to content that does not exist, captions that misdescribe their figures,
   near-verbatim quotations, and symbols reused against the book's own notation rule. Every
   build reproduced exactly.
4. **A lean single auditor is enough for monitoring.** The Sonnet auditor in lean mode found
   all 4 planted errors in optimization-lab for about 40% of the tokens of a full Opus audit.

## Actions

- data-lab: 8 defects fixed ([commit d85d7ec](https://github.com/ioannisantoniadis/data-lab/commit/d85d7ec)).
- [loss-functions-lab#1](https://github.com/ioannisantoniadis/loss-functions-lab/issues/1),
  [rl-for-llms#1](https://github.com/ioannisantoniadis/rl-for-llms/issues/1),
  [optimization-lab#2](https://github.com/ioannisantoniadis/optimization-lab/issues/2): the
  confirmed defects, for sessions working in those repositories.

## For the merge

- **Notation:** β (learning-curve exponent, KL strength), α (Zipf exponent, step size, ridge
  weight, Hoffmann's exponent), λ, γ, q, r, μ, τ, σ and π (policy vs permutation) mean
  different things across the books, and several are reused within a book. A shared notation
  appendix has to be designed before content is merged.
- **Devices already aligned:** generated cards with fixed fields (data cards, method cards),
  lineage callouts, Definition boxes, evidence labels with dates, one script or cell per
  figure.
- **To harmonize:** chapter templates (data-lab adds "What the toy cannot show"), number
  generation (adopt generated numbers everywhere), and test naming.

## What the v1 pilot taught (now in the protocol)

1. **Sample size.** At 30 items the rate cannot separate books. Use the full-read defect
   density (confirmed defects per 10,000 words, by severity) as the primary metric, and a
   sample of 100 items when a rate is wanted.
2. **Classifier.** 3–4 of 30 sampled items had no checkable statement; require a verb of
   assertion or a number tied to a result, and drop cross-reference-only sentences.
3. **Blinding must not break the build.** Keep the README's original build commands (the
   neutral README dropped rl-for-llms's `--extra` flags, which one auditor reported as a
   defect), and keep files that tests read (data-lab's `COVERAGE.md`), or mark those tests.
4. **Reports come back as text.** Subagents cannot write report files; the brief should ask
   for the report in the final message, and give each auditor its own work directory (two
   wrote scratch files outside their copies).
5. **Adjudication step.** The orchestrator checks every non-planted defect against the
   original before it is counted (done here by hand), and resolves disagreements (one item).
