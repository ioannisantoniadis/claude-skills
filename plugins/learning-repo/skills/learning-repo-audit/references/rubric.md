# The learning-repo rubric

One rubric shared by `learning-repo-audit` (which scores a repo against it) and
`learning-repo-build` (which builds to it). A *learning repo* teaches a technical subject through
prose plus computation: a Quarto or Markdown book with figures, a set of interactive demos, or a
research codebase with write-ups. What the reader is paying for is the guarantee that **what the
repo says is true, and what it shows was actually computed**. Every criterion below protects that
guarantee or the reader's time.

Contents: [criteria](#criteria) · [hard fails](#hard-fails) · [severity](#severity) ·
[profiles](#profiles) · [calibration](#calibration)

## Criteria

Score each criterion 1–5. Anchors define 1, 3 and 5; 2 and 4 sit between. Each criterion lists
the **mechanical checks** (run them all; they're cheap and exhaustive) and the **sampled checks**
(judgment-heavy; done on a sample, so say how big the sample was).

### 1. Source fidelity

Technical claims trace to primary sources, and the sources say what the repo says they say.

| 1 | 3 | 5 |
|---|---|---|
| Claims are unsourced, or citations are wrong, invented or misattributed. | Main claims cited; some details (defaults, numbers, dates, author lists) are from memory or secondary summaries and a few are off. | Every load-bearing claim cites a primary source that was opened; a research log records what was checked and what couldn't be; corrections to the literature are cited too. |

- *Mechanical:* every citation key resolves to a bibliography entry; every entry has a DOI, arXiv
  id or URL; every arXiv id / DOI exists (API lookup, not memory); a research log or source list
  exists.
- *Sampled:* about 10 claims per repo, weighted toward (a) recent or frontier material, where
  model recall is worst, (b) specific numbers, defaults and equations, (c) claims the argument
  rests on. Open the source and give each a verdict: ok · imprecise · wrong · not-found ·
  unreachable.

### 2. Computed evidence

Figures and numerical results come from code in the repo that actually runs, and regenerating
them gives what the page shows.

| 1 | 3 | 5 |
|---|---|---|
| Figures are hand-drawn, AI-generated, or plotted from hard-coded "illustrative" numbers presented as results; no scripts. | Most figures have scripts; some are decorative or schematic without saying so, or scripts no longer run. | Every figure is produced by a committed script from a real computation; schematic figures are labeled as schematic; regenerating reproduces the published image. |

- *Mechanical:* every image referenced from the content exists; every image in the image folder
  is referenced (orphans are noise or leftovers); every data figure maps to a generating script;
  a sample of scripts (at least 3, and the signature figure) run cleanly from a fresh environment.
- *Sampled:* look at each sampled figure next to its script. Does the script compute what the
  caption says? Are numbers hard-coded? Is randomness seeded, and is the claimed effect robust
  to the seed (re-run with another seed when the claim is about typical behavior)?

### 3. Claims match measurements

The prose says what the computation shows: no more, no less, and the same numbers.

| 1 | 3 | 5 |
|---|---|---|
| Prose describes effects the figures don't show, or numbers in the text don't match the code's output. | Broadly consistent; some overreach ("always", "never", "converges") beyond what one toy run shows; some quoted numbers are stale. | Every quoted number matches a fresh run; generalizations are scoped to what was measured; negative and seed-dependent results are reported as such; the limits of the toy are stated. |

- *Mechanical:* none fully mechanical. Grep numbers in captions and prose that cite a figure or
  experiment, and list them.
- *Sampled:* for 3–5 of those numbers, re-run the script and compare. For each sampled figure,
  read its caption and the paragraph that cites it and check every factual statement against the
  image.

### 4. Correctness

Derivations, definitions and implementations are right, and tests check the claims rather than
merely exercising the code.

| 1 | 3 | 5 |
|---|---|---|
| A core derivation or definition is wrong, or the implementation doesn't do what the text says. | Correct on the main line; edge cases, signs, normalizations or conventions are sloppy in places; tests are smoke tests. | Derivations are complete and checked; implementations are tested against ground truth (closed forms, exact enumeration, finite differences, a reference library); a claim in the text that can be checked numerically has a test. |

- *Mechanical:* the test suite passes; count tests that assert a numerical property (against a
  closed form, enumeration, finite differences, a reference implementation) versus tests that
  only check shapes or that code runs.
- *Sampled:* re-derive 2–3 key results by hand or numerically. Read 2–3 core implementations
  against their text.
  For an optimizer or solver, compare the *objective value* it reaches with a reference
  solver's, not just its predictions: agreeing predictions can hide a solution well short of
  the optimum (an SVM can separate the data perfectly with a far-from-maximal margin).

### 5. Pedagogy

The repo teaches. It motivates before it defines, derives before it states, and connects ideas.

| 1 | 3 | 5 |
|---|---|---|
| A glossary or catalogue: definitions without motivation, no thread between sections. | Motivated and mostly derived, but sections stand alone; the reader gets facts without the unifying view. | One clear thesis; each section says what problem it solves and what earlier limitation motivates it; objects are derived, not announced; assumptions are named with what breaks; sections link to their neighbors and say why. |

- *Mechanical:* every chapter or page has a closing connections or next-steps element, if the
  repo's conventions call for one; prerequisites or reading paths are stated.
- *Sampled:* read 2 sections in full, one foundational and one advanced. Could the target reader
  reconstruct the key result from the page alone?

### 6. Honesty and currency

The repo says how sure it is, and when.

| 1 | 3 | 5 |
|---|---|---|
| Vendor claims, single papers and speculation are stated as fact; nothing is dated in a fast-moving field. | Some hedging; frontier material is undated or not separated from established results. | Each empirical claim is labeled as mathematical fact, replicated finding or contested/recent; frontier content is dated ("as of <month year>"); unrefereed and vendor sources are flagged; reconstructions are labeled as reconstructions; known corrections and disputes are cited. |

- *Mechanical:* grep for date stamps and hedging vocabulary in frontier sections; list papers
  from the last ~18 months and check each is dated or attributed.
- *Sampled:* covered by the criterion-1 sample. Check how each sampled frontier claim is framed,
  not only whether it's true.

### 7. Internal consistency

The repo agrees with itself, and its descriptions agree with the repo.

| 1 | 3 | 5 |
|---|---|---|
| Notation changes between sections; links are broken; the README describes files or counts that don't exist. | Mostly consistent; a few stale counts, dangling references or renamed symbols. | One notation table, used everywhere; all internal links resolve; every count and file named in the README, repo description, site metadata and the author's profile matches the repo; tables derived from data are generated, not hand-copied. |

- *Mechanical:* the site renders with zero warnings (broken cross-refs, missing citations); every
  path named in README / CLAUDE.md / CONVENTIONS / docs exists; counts in the README, GitHub
  description and profile README match reality (chapters, apps, figures, tests); one term per
  concept across files.
- *Sampled:* compare notation across 3 sections that share symbols.

### 8. Engineering hygiene

The repo builds, tests and deploys from a clean checkout with the documented commands.

| 1 | 3 | 5 |
|---|---|---|
| Documented build commands fail; no tests or CI; the deployed site is stale or down. | Builds with some fiddling; CI exists but is red or doesn't cover tests; dependencies unpinned. | The documented commands work verbatim from a fresh clone; lint and tests run in CI and are green; the deploy is automated and the live site matches `main`; dependencies are locked. |

- *Mechanical:* run the README's install, test, lint and render commands verbatim; latest CI runs
  on the default branch (`gh run list`); the live site responds and its content matches the
  current build; a lockfile exists.

### 9. Economy

The reader's time is respected: concise, no filler, nothing repeated without reason.

| 1 | 3 | 5 |
|---|---|---|
| Padded: restated introductions, generic filler ("In today's fast-moving world"), bullet lists where an argument should be, the same explanation in several places. | Mostly tight; some sections ramble or repeat; some figures add nothing. | Every section, figure and paragraph earns its place; scope is stated and enforced (adjacent topics link to where they live); length matches content. |

- *Sampled:* read the two sampled sections for padding; check whether any figure could be
  deleted without loss.

## Hard fails

Any one of these caps the overall verdict at **needs rework**, whatever the scores, because each
breaks the guarantee the repo exists to offer:

- **fabricated-source**: a cited paper, author list, quote or result doesn't exist or doesn't say
  what's claimed.
- **fabricated-result**: a figure or number is presented as computed but was not (hard-coded,
  drawn, or from a script that can't produce it).
- **wrong-core-claim**: a derivation, definition or result the repo's argument depends on is
  false.

A single instance counts. The report must quote it, give its location and give the evidence.

## Severity

Rank findings by what they do to a reader who trusts the repo:

| Severity | Meaning | Examples |
|---|---|---|
| **blocker** | The reader learns something false, or the repo can't be built. | a hard fail; a wrong equation in a definition box; tests or render broken on `main` |
| **major** | The reader is misled about strength of evidence, or can't reproduce. | an undated frontier claim stated as fact; a figure whose script is missing; a caption that overclaims; a stale headline number |
| **minor** | Friction, not falsehood. | a dangling README path; an orphan image; inconsistent notation in one place; a stale count |
| **polish** | Taste. | wording, figure styling, ordering |

## Profiles

Not every criterion applies the same way to every kind of repo. Identify the profile first and
adapt the mechanical checks; don't penalize a repo for lacking what its form doesn't need.

| Profile | Recognize it by | Adapt |
|---|---|---|
| **book** | `_quarto.yml` or mdBook/Jupyter Book config; chapters; `docs/images/` | All criteria apply. Check whether figures are pre-generated (scripts → PNGs) or executed at render (code cells). For executed figures, criterion 2's "script" is the cell, and a clean render *is* the regeneration test. |
| **notes** | Markdown folders, maybe a static HTML index; few or no figures | Criteria 2–3 apply only to figures and numbers present; weight 1, 5, 6, 7 and 9 more. A static map or graph counts as a figure: check it's generated from the notes and not hand-maintained. |
| **app** | Streamlit, Gradio or a JS app; one module per demo | Criterion 2 → "the visualization is driven by the real algorithm run, step by step, not a canned animation". Criterion 4 → the from-scratch implementation matches a reference library on the same inputs. Criterion 8 → each app imports and runs headless (e.g. `streamlit.testing.v1.AppTest`; for a multipage app, load the entry page and `switch_page` to each page, because running a page file directly can shadow packages that share its name). |
| **research** | Experiment code plus results or a write-up; maybe no site | Criterion 3 dominates: results tables and plots regenerate from logged configs and seeds. Criterion 5 → the write-up explains the method and the result for an outsider. |

## Calibration

A **3** is a competent repo that a reader could learn from but should double-check. A **5** is
rare: you would trust it without checking, and recommend it. If most scores come out at 4–5,
recalibrate before writing. An inflated audit is worse than none, because the author then stops
looking. Score what's in the repo, not what its plan promises.
