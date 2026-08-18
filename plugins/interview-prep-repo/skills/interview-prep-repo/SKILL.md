---
name: interview-prep-repo
description: Scaffold a new standalone interview-prep GitHub repo under ~/GitHub for an upcoming job interview, following the "<company>-<role>-<topic>-prep" naming and structure convention (e.g. acme-mle-recsys-prep, globex-swe-systems-design-prep) — matching any sibling *-prep repos the user already has, or the built-in reference structure if this is the first one. Use whenever the user has an interview or interview round coming up and wants to study for it, asks for a "prep repo" / "study repo" / "prep kit", gives an interview topic with optionally a company name and/or a job description, or asks to research a company's interview process and build materials around it. Trigger even without the words "skill" or "repo" — e.g. "I have an onsite with Netflix for a recsys role next month, help me get ready" or "set me up something like my other prep repos but for a Stripe fraud-detection ML role" should both trigger this.
---

# Interview Prep Repo Generator

Generates a new, self-contained interview-prep repository following a proven
`<company>-<role>-<topic>-prep` convention: the same shape as any sibling `*-prep` repos
already sitting in `~/GitHub`, or the reference structure documented in `references/` if
this is the first one. That convention wasn't invented for this skill — it's what a prep
repo settles into after enough rounds of hand-building one per interview; this skill
reproduces it faster and more completely, while researching the specific company and role
so content is genuinely tailored rather than generic.

The output is a repo the user studies from over days or weeks before an interview: topic
pages, a cram brief, rehearsable scenario prompts, a glossary, notes on real papers/blog
posts distilled from actual research, and — for hands-on rounds — a small runnable code
scaffold with passing tests.

## Why the structure matters

The existing repos are not a random pile of notes — every file type plays a specific role
in spaced, rehearsable prep: `interview-brief.md` is the "read this right before the call"
cram sheet, `deep-dive-priorities.md` triages study time against likely question weight
(explicitly tied to the job description when one exists), `interview-prompts.md` is for
saying answers out loud, `topics/*.md` is reference depth, and `notes/` is where real
external sources get distilled so the user studies from evidence, not vibes. Keep this
division of labor intact — don't collapse everything into one giant README.

## Step 1 — Gather inputs

Required:
- **Topic**: the role/round focus (e.g. "LLM evaluation", "recsys ranking", "ML systems
  design", "Python coding round", "analytics + data viz").

Optional — infer sensible defaults and move on if the user clearly wants to move fast;
don't interrogate:
- **Company** (or none, for a generic topic-only repo).
- **Job spec / JD**: pasted text, file path, or URL. This is the single highest-leverage
  input — it drives topic emphasis and the "Why" lines in `deep-dive-priorities.md`. Quote
  it verbatim where referenced; don't paraphrase away specific tools/responsibilities.
- **Known interview format**: round names, time limits, whiteboard/CoderPad/take-home,
  number of rounds, anything a recruiter already shared. Shapes `interview-brief.md`'s
  format section.
- **Timeline**: days until the interview — shapes whether `roadmap.md` gets built and how
  aggressively `deep-dive-priorities.md` triages.
- **Existing sibling repos**: check `~/GitHub` for other `*-prep` repos (same company or
  adjacent topic) to cross-link in a "Related Prep Repos" table — a real pattern in the
  existing repos, not decoration.

## Step 2 — Name and place the repo

Follow the existing naming convention exactly:
- With a company: `<company>-<role-abbrev>-<topic>-prep` (kebab-case), e.g.
  `netflix-mle-recsys-prep`, `stripe-mle-fraud-detection-prep`. Infer the role abbreviation
  from the JD/role title (`mle`, `swe`, `ds`, `sre`, ...); use a precedent from the user's
  other repos if one exists.
- Without a company: `<topic>-interview-prep`, e.g.
  `distributed-systems-design-interview-prep`.

Target location: `~/GitHub/<repo-name>/`, sibling to the existing prep repos. Check the
path doesn't already exist before creating it; if it does, ask whether to reuse, rename, or
update in place.

## Step 3 — Decide the variant: code-backed or design-only

This is a real, deliberate fork in the existing repos, not an inconsistency — replicate it.

| Signal in topic/role | Variant |
|---|---|
| Coding round, Python/algorithms round, LLM software-engineering round, applied-ML round with implementation discussion, evaluation-pipeline round | **Code-backed** — add `src/<pkg_name>/`, `tests/`, `examples/run_*.py`, `pyproject.toml` |
| Pure systems/product design round, analytics/data-viz round, behavioral-only round | **Design-only** — skip `src/`, `tests/`, `pyproject.toml` entirely; no apologetic stub code |

If genuinely unsure, default to design-only — runnable code is earned by an actually
hands-on round, not a default add-on. One documented nuance: an analytics/data-viz round
can still warrant a small standalone `scripts/generate_figures.py` (+ `requirements.txt`)
purely to produce chart images referenced from case studies — that's not the same as going
fully code-backed (no package, no tests, no `pyproject.toml`).

Read `references/repo-skeleton.md` now for the exact file tree for each variant, including
how many `topics/*.md` and `notes/*.md` files are typical (scales with topic breadth: 7-10
for a narrow round, up to 15-17 for a broad one like recsys ranking — never pad).

## Step 4 — Research before writing anything

This is what makes the repo worth more than what the user could write from memory alone.
Budget real search effort here before scaffolding files.

Search for and read (WebSearch/WebFetch):
1. **Company engineering blog posts** on the topic — become `notes/blogs/*.md` and
   `references/blogs.md`.
2. **Canonical papers** underpinning the topic — `notes/papers/*.md` and
   `references/papers.md`. Prefer papers the company itself published or is known to cite.
3. **Public interview-experience threads** (Blind, Glassdoor, Reddit, LeetCode Discuss,
   levels.fyi forums) for this company+role. Authenticated/paywalled content can't be
   scraped — search for excerpts, summaries, or publicly indexed snippets instead, and
   always cite the source link rather than reproducing large verbatim chunks. Use these to
   calibrate `interview-brief.md`'s format/likely-question sections and to ground
   `interview-prompts.md` scenarios in what people actually report being asked.
4. **If a job spec was provided**: pull its explicit skill/tool/responsibility mentions into
   `deep-dive-priorities.md`'s "Why" lines directly (e.g. "the JD explicitly asks for
   translating qualitative failures into training signals") — this is what makes the repo
   feel tailored rather than templated.

Keep a running list of every source actually used — it becomes `references/papers.md` /
`references/blogs.md`, and drives which `notes/` files get written. Never invent a source;
every `notes/` and `references/` entry must trace to something actually found this run.

Given the research volume plus the number of files this produces, prefer running Steps 4-5
as a background fork rather than inline, so a single repo generation doesn't consume the
whole conversation's context.

## Step 5 — Scaffold and write content

Read `references/content-style-guide.md` now — it defines section structure and tone for
every file type (README, interview-brief, deep-dive-priorities, interview-prompts, topic
pages, glossary, case studies, paper/blog notes) with real calibration excerpts.

Copy the relevant blank scaffolds from `assets/templates/` into the new repo's own
`templates/` directory verbatim (every existing repo ships these so the user can keep
adding notes after prep is "done" — don't skip it). Always include `topic-note.md`; add
`paper-note.md` + `blog-note.md` when `notes/papers|blogs` is used; add `case-study.md`
when `notes/case-studies` is used; add `coding-drill.md` + `system-design-answer.md` for
engineering-flavored code-backed rounds.

Then write, in this order (later files can reference earlier ones):
1. `topics/NN-*.md` — reference depth, one file per subtopic, 2-digit zero-padded, topic
   `01` is always an answer-framework/interview-strategy primer.
2. `notes/papers/*.md`, `notes/blogs/*.md`, `notes/case-studies/*.md` — populated from Step
   4's research, using the copied templates as structure but fully filled in (no `TODO:`
   placeholders — those exist only in the blank `templates/` copies for later use).
3. `references/papers.md`, `references/blogs.md`, `references/tools.md` — index
   tables/lists pointing at the notes.
4. `glossary.md` — alphabetized terms actually used in the topic pages, `Term | Definition`
   table, one-sentence definitions meant to be spoken aloud.
5. `interview-brief.md` — the cram sheet: interviewer background where known, round
   format/tool/length, a likelihood table of question types. When no JD, recruiter intel,
   or known format was given (a generic topic-only run), lean on Step 4's public
   interview-experience research and general round conventions for this company/role
   instead — say so plainly rather than inventing specifics (e.g. "no confirmed format;
   based on public reports, expect ..."). This section will read a little softer than one
   built from real JD/recruiter intel — that's expected, not a bug to paper over.
6. `deep-dive-priorities.md` — 10-20 ranked items (Terms/Why/Study/Practice), tiered
   Highest/Medium/Lower, plus time-boxed cram plans (1hr/4hr/1day/2day), "Why" tied to the
   JD where available.
7. `interview-prompts.md` — 5-8 full rehearsable scenarios (each with follow-ups) plus one
   rapid-fire list of 8-15 short questions.
8. `roadmap.md` — only if a timeline was given or the topic is broad enough to need
   phasing. **This file is local-only**: every precedent repo's `.gitignore` excludes it
   (along with `private-notes.md`, a scratch file the skill should never create but should
   preserve in `.gitignore` for the user's own use). Write it to disk for the user, but it
   won't be part of the git-tracked content.
9. `diagrams/README.md` — 3-6 Mermaid diagrams for the highest-value system/process flows,
   each with a one-line "Key interview point"; omit only if the round has no system/pipeline
   worth diagramming (e.g. pure algorithmic coding rounds).
10. `README.md` last, once the full contents are known — hero framing paragraph, "How To
    Use This Repo", Topic Map table, repo-specific sections (Starter Implementation for
    code-backed, Case Studies table, Reference Indexes), "Guiding Questions", "Related Prep
    Repos" table if siblings exist in `~/GitHub`, License line last.
11. `LICENSE` (MIT — copy `assets/templates/LICENSE.tpl`) and `.gitignore` (copy
    `assets/templates/gitignore.tpl`).
12. **Code-backed variant only**: `pyproject.toml` (adapt
    `assets/templates/pyproject.toml.tpl`), `src/<pkg>/` modules relevant to the topic
    (small, dependency-free or `pytest`-only, docstring-annotated, each with explicit
    complexity notes and a "Production:" line — under ~150 lines/module), matching
    `tests/test_*.py` (one per module, terse, edge-case-driven), one `examples/run_*.py`,
    and optionally `data/*.jsonl` synthetic examples for a runnable pipeline. For
    pure-algorithmic coding rounds, also add `exercises/README.md` with blank practice
    stubs mirroring `src/`, noting "solutions live in `src/`". Then actually run
    `uv sync --dev && uv run pytest` and confirm green before finishing — every existing
    repo's tests pass; never ship broken starter code.

## Step 6 — Wire up and hand off

- `git init` and one initial local commit, using whatever `user.name`/`user.email` git
  already resolves (global config or existing repo-local config) — don't invent an identity
  or prompt for one. Do **not** create a GitHub remote or push — that is the user's call
  each time, not a default action of this skill.
- If sibling `*-prep` repos exist in `~/GitHub`, add the "Related Prep Repos" table to the
  new README, and — only if it clearly helps — ask before adding a one-line back-reference
  to a sibling's own README.
- Finish with a short summary: repo path, topic map, and where to start reading first
  (mirroring the "interview within 48 hours? start with `deep-dive-priorities.md`" pattern
  used when time is short).

## Quality bar

- No generic filler. Every topic page, case study, and prompt should read as if written by
  someone who actually knows this domain, not a listicle.
- No placeholder `TODO:` text in any file outside `templates/`.
- Every claim of "the JD says X" or "candidates report Y" must trace to something actually
  read this run, not something plausible-sounding.
- Match the terse, bullet-heavy, second-person-imperative tone documented in
  `references/content-style-guide.md` — a deliberate choice for fast rehearsal, not a style
  to "improve on."
