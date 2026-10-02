# Build playbook

Detail for each phase of `learning-repo-build`. Read the section you need.

Contents:
1. [Research](#research)
2. [Ground-truth testbed](#ground-truth-testbed)
3. [Tests](#tests)
4. [Figures](#figures)
5. [Writing devices](#writing-devices)
6. [Single source of truth](#single-source-of-truth)
7. [Project docs templates](#project-docs-templates)
8. [Quarto book setup](#quarto-book-setup)
9. [Other profiles](#other-profiles)
10. [Pitfalls seen in practice](#pitfalls-seen-in-practice)

## Research

- **Primary sources only for technical content.** Use the paper, the official docs, the author's
  own blog post. A survey or secondary summary is fine for finding sources, never for content.
- **Verify bibliography metadata by API, not by memory.** For arXiv, query
  `http://export.arxiv.org/api/query?id_list=<id1>,<id2>,…` (batch up to ~100 ids, and back off
  on HTTP 429). For DOIs, use `https://doi.org/api/handles/<doi>`. Copy titles, author lists and
  years from the response. Give every bib entry a DOI, arXiv `eprint` or URL, so an audit can
  check it mechanically.
- **Read the paper text** for equations, defaults and results. WebFetch often can't parse PDFs:
  `curl -sL <pdf-url> -o x.pdf && pdftotext -layout x.pdf -`, then grep.
- **Search for what corrects each source**: follow-up papers, errata, replications, critiques.
  Cite them alongside the original.
- **For vendor or frontier claims,** find the primary announcement and note the date, what is
  disclosed and what isn't. Site-build timestamps are not publication dates: check the page
  itself.
- **Log as you go**, in `research-log.md`: one entry per source, with URL, date accessed, what
  was checked, what was verified, what couldn't be, and any discrepancy with the spec or with
  earlier text. This is the audit trail that makes the repo trustworthy.

## Ground-truth testbed

The single highest-leverage decision. Pick the smallest setting where the quantity the repo is
about can be **computed exactly**, so every method is measured against the truth instead of
against another approximation.

- **Patterns:**
  - an enumerable space (e.g. a toy language with 5 tokens × length 4 = 625 sequences, so every
    expectation is a sum);
  - a closed-form optimum (quadratics for optimizers; conjugate priors; a known
    KL-regularized optimum);
  - tiny MDPs solvable by value iteration;
  - synthetic data with known generating parameters.
- **Make it expressive enough** that failures are the method's, not the model's capacity, and
  say so explicitly. Add capacity-limited variants only where a lesson needs them (e.g. shared
  features for a generalization effect).
- **Choose parameters by scanning, and document the choice.** For example: seeds scanned so
  the tasks span easy to hard.
- **One shared core API** that every method ends in, so methods differ only in what they pass to
  it. If the thesis is that methods are variants of one idea, make that literally true in code.
- **Use the same optimizer, step budget and schedule for every method**, so comparisons are of
  methods, not of tuning.
- **Write the testbed and its limits on one appendix page:** what can be computed exactly, the
  variants, and what the toy cannot show (scale, wall-clock, generalization).

- **If the field has a reference implementation, calibrate against it.** Reproduce its
  published golden outputs first (proves your build of it is right), then compare your
  engine's *population-level* statistics with it on the same inputs. Bit-for-bit agreement
  is not expected when RNGs differ; agreement within a confidence interval is. Freeze a few
  real outputs from it as positive-control test fixtures, with provenance (commit, flags,
  seed, epoch) in the test docstring.

## Tests

Tests exist to check the repo's *claims*, not just that code runs.

- **Check derivations against ground truth.** Examples:
  - a closed-form optimum matches a brute-force optimum;
  - an estimator's expectation, by enumeration, equals the exact value;
  - a gradient matches finite differences;
  - two "equivalent" objectives have the same optimum.
- **Write a test for every checkable claim in the text** ("X is unbiased", "Y has zero expected
  gradient", "Z converges to the optimum").
- **Make method tests convergence tests:** each method reaches the known optimum within a stated
  tolerance on the testbed.
- **For seed-dependent effects,** test the multi-seed statistic the text quotes (e.g. "the median
  over 10 seeds"), not one lucky seed.
- **Run lint and tests in CI** on every push.

## Figures

- **One script per figure** (`scripts/figures/fig_<slug>.py`), importing the real library code
  (never re-implementing it) and writing `docs/images/<slug>.png`. Pre-generate the images and
  commit them, unless the repo's convention is executing at render.
- **Give the script a docstring** that finishes "this figure makes visible that …".
- **Use a shared theme module** for palette, fonts and a `savefig` helper. Color follows a
  semantic grouping (method family, model type), consistently across figures. Validate the
  palette for color-vision deficiency; with three or more series, add direct labels or distinct
  line styles as well as color.
- **Look at every PNG** after every change. Typical defects only visible by looking:
  - overlapping labels;
  - legends covering data;
  - symlog or log axes distorting the story;
  - layouts whose coordinates don't match the labels;
  - crowded timelines.
- **Write captions that state what is plotted and the lesson.** The prose must not claim more than
  the image shows.
- **Fix seeds, and show spread** (median plus a band) when the claim is about typical behavior.
- **Keep a figures README:** a table of script, image, the chapter that uses it, and the lesson.

## Writing devices

Use them consistently: a device used everywhere becomes a tool for the reader.

- **The chapter template**: opening problem → assumptions → derivation → boxed definition →
  summary card → interpretation → failure modes with a figure → connections (2–4 neighbors, with
  why).
- **Fixed-field summary cards.** Every method or concept gets the same fields in the same order
  (for an RL book: signal, sampling distribution, weight, stability mechanism, credit
  granularity, models in memory, target, classical lineage). These make cross-cutting comparison
  possible and feed a generated table.
- **Lineage callouts**, e.g. "Classical lineage — this is <idea>": where a new method reuses an
  old idea, name it. This is how a reader's prior knowledge connects to new vocabulary.
- **Evidence levels.** Each empirical claim is a mathematical fact (state it plainly), a
  replicated finding ("several groups report", with cites) or recent/contested ("the paper
  reports", dated, with counter-evidence). Vendor claims are attributed, never restated as fact.
  First-principles reconstructions of undisclosed methods are labeled as reconstructions.
- **Distinctions to never blur**: list the field's commonly conflated pairs in `CONVENTIONS.md`
  and enforce them.
- **Cross-reference by title and link**, not by bare chapter number, which shifts when chapters
  move.
- **Date-stamp frontier content**: "as of <Month YYYY>".

## Single source of truth

Anything that appears in more than one place is generated from one record:

- method or concept records (`scripts/<name>_data.py`) → summary table, lineage graph, map, timeline;
- the notation appendix → the only place symbols are defined; a new symbol is added in the same
  change;
- counts in the README, the repo description and the profile README → checked against the repo
  before publishing.

## Project docs templates

**`CONVENTIONS.md`** should cover:
- what the repo is, in one paragraph (the thesis);
- the standing rules (research first; scope test);
- the file and frontmatter format;
- the chapter template;
- the summary-card fields;
- the callout conventions;
- the evidence levels;
- the distinctions never to blur;
- the math, code and citation mechanics;
- the figure rules;
- the code rules.

**`ROADMAP.md`**:
```markdown
# Roadmap
Status markers: planned · researching · drafted · done (passes the quality bar) · blocked
## Phase N: <name> (<date>): <status>
- [x] step … (what was done, with counts)
### What <experiment> showed (and why it changes the plan)
## Decision log
- <date> — <decision>. Why: <reasoning>. Alternatives: <…>.
```

**`research-log.md`**:
```markdown
# Research log
## <Chapter or topic>
| Source | URL | Accessed | Checked | Verified | Not verifiable / notes |
## Discrepancies with the spec
- <claim in spec> → <what the evidence says> (source). Resolution: <…>. User told: <date>.
```

**`CLAUDE.md`** should give:
- the build, test and render commands;
- where things live;
- the standing rules;
- the files that are local-only.

## Quarto book setup

- **`_quarto.yml`**: book project, chapters in parts, appendices, bibliography, `site-url`,
  `repo-url`, `open-graph: true`, `twitter-card: {card-style: summary_large_image}` and a social
  preview `image:` (a 1280×640 PNG, generated by a script like any other figure).
- **No code execution at render**, unless the repo's convention is executed notebooks. Fenced
  code blocks are display excerpts of real library code, kept in sync.
- **Render with `quarto render docs` and fix every warning**: unresolved cross-references and
  missing citation keys are warnings, not errors, and ship silently otherwise.
- **Deploy from a GitHub Actions Pages workflow** (`build_type=workflow`), and check that the live
  site matches after the deploy.

## Other profiles

- **Notes** (Markdown folders): one template per entry, a generated index or map, sources per
  entry, dated frontier entries. If an index or graph exists, generate it from the entries.
- **App** (Streamlit and similar): one module per demo; the from-scratch algorithm is tested
  against a reference library on the same inputs; the visualization steps through the real run;
  each page is smoke-tested headless (`streamlit.testing.v1.AppTest`) in CI.
- **Research codebase**: configs and seeds logged per result; every results table and plot
  regenerates from a script; the write-up states what was and wasn't run.

## Pitfalls seen in practice

- **Rate limits**: arXiv returns 429 on bursts. Batch ids, and sleep and retry. Some vendor sites
  block plain fetches; use `curl` with a user agent.
- **Linters rewriting imports** (e.g. `ruff --fix`): this invalidates exact-string edits made
  afterwards. Re-read a file before editing it.
- **Packaging**: `uv sync` with a `readme =` in `pyproject.toml` fails if the README doesn't
  exist yet.
- **MathJax in generated Markdown tables**: `\|` renders oddly. Use `\lvert … \rvert`, and avoid
  bare `|` inside math in tables.
- **Seed luck**: an effect seen on one seed may hold on only 6 of 10. Check before writing it into
  a test, a figure or a sentence, and quote the multi-seed statistic.
- **Stale numbers**: after any change to the testbed or a method, re-run every figure and grep
  the prose for the numbers it quotes.
- **Dangling doc references**: READMEs (including `scripts/figures/README.md`) naming scripts
  that were renamed or never written. The audit script catches these.
- **Accounts and identity**: check which GitHub account `gh` is authenticated as before
  creating repos or setting URLs (`gh api user`).
