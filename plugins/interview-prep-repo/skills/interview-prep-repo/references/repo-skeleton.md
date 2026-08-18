# Repo Skeleton Reference

Canonical file trees for a generated interview-prep repo, derived from auditing a set of
real interview-prep repos spanning a Python/algorithms coding round, an applied-ML round,
an LLM-evaluation round, an LLM software-engineering round, an ML-systems-design round, an
analytics/data-viz round, and a recsys-ranking round — all independently converging on the
same personal convention across several real job searches.

## Design-only variant

Use for pure systems/product-design rounds, analytics/data-viz rounds, behavioral-only
rounds. Precedents: an ML-systems-design round, a product/marketplace systems-design
round, and an analytics/data-viz round — all pure-markdown, no code.

```
<repo-name>/
├── .gitignore
├── LICENSE
├── README.md
├── interview-brief.md
├── deep-dive-priorities.md
├── interview-prompts.md
├── glossary.md
├── roadmap.md                  # optional, LOCAL ONLY — .gitignore'd in every precedent repo
├── diagrams/
│   └── README.md                # omit only if there's no system/pipeline worth diagramming
├── topics/
│   ├── 01-<answer-framework-or-strategy>.md
│   ├── 02-...md
│   └── NN-...md                 # 7-10 files for a narrow round, up to 15-17 for a broad one (see Scaling rules below)
├── notes/
│   └── case-studies/
│       └── <scenario-name>.md   # 2-5 full worked case studies, options+tradeoffs at each stage
├── references/
│   ├── papers.md
│   ├── blogs.md
│   └── tools.md
└── templates/
    └── case-study.md
```

**Named exception — analytics/data-viz rounds**: may additionally include a small,
standalone `scripts/generate_figures.py` + `requirements.txt` purely to produce chart
images referenced from case studies. No package structure, no tests, no `pyproject.toml` —
this does not make the repo "code-backed"; it stays in the design-only family.

## Code-backed variant

Use for coding rounds, Python/algorithms rounds, LLM software-engineering rounds,
applied-ML rounds with implementation discussion, evaluation-pipeline rounds. Precedents:
a Python/algorithms coding round, an applied-ML round, an LLM-evaluation round, and an LLM
software-engineering round — all shipped runnable `src/` + `tests/`.

```
<repo-name>/
├── .gitignore
├── LICENSE
├── README.md
├── interview-brief.md
├── deep-dive-priorities.md
├── interview-prompts.md
├── glossary.md
├── roadmap.md                          # optional, as above
├── pyproject.toml
├── diagrams/
│   └── README.md                       # omit for pure-algorithmic coding rounds
├── data/
│   └── <topic>_cases.jsonl             # optional — small synthetic dataset the example script runs against
├── examples/
│   └── run_<verb>.py                   # one runnable script exercising src/
├── exercises/
│   └── README.md                       # pure-algorithmic rounds only — blank stubs; "solutions live in src/"
├── src/
│   └── <pkg_name>/                     # snake_case package name derived from the topic
│       ├── __init__.py
│       ├── schemas.py                  # typed dataclasses for the domain's core objects
│       ├── metrics.py                  # the domain's actual metrics, not generic accuracy
│       └── pipeline.py                 # loads data, runs the toy pipeline, aggregates results
├── tests/
│   └── test_*.py                       # one test file per src module, real assertions
├── topics/
│   └── ...                             # same numbering convention as design-only
├── notes/
│   ├── papers/
│   │   └── <paper-slug>.md
│   ├── blogs/
│   │   └── <post-slug>.md
│   └── case-studies/                   # only if the round also has a design component
│       └── <scenario-name>.md
├── references/
│   ├── papers.md
│   ├── blogs.md
│   └── tools.md
└── templates/
    ├── paper-note.md
    ├── blog-note.md                    # if notes/blogs/ is used
    └── topic-note.md
```

`src/` is intentionally small and dependency-free (stdlib only, or `pytest` as the sole dev
dependency) — it exists to give the user something concrete to talk through in the
interview, not to be a production framework. Keep modules under ~150 lines each.

**Named variant — engineering-flavored code-backed rounds** (e.g. LLM software
engineering): swap `templates/paper-note.md` + `topic-note.md` for `templates/coding-drill.md`
+ `templates/system-design-answer.md` — the precedent repo for this flavor uses those
instead.

## Scaling rules of thumb

- **Topic file count**: narrow single-round topic → 7-10 files. Broad topic spanning many
  subareas (e.g. recsys ranking spanning CF, deep ranking, sequential models, bandits,
  serving) → up to 15-17 files, *if* the research in Step 4 actually turned up that much
  distinct depth. This is a ceiling, not a target — let the real breadth of what you found
  drive the count. A broad topic covered by shallow research should land well below 15-17
  (e.g. 8-10) rather than being padded to hit the range; a thin topic count is a sign of
  thin research, not a defect on its own, as long as every topic file is substantive.
- **Paper/blog note count**: scale to what real, relevant sources you found in Step 4
  research. A narrow round might justify 3-6 papers; a research-heavy round (recsys, LLM
  evaluation) can justify 20-60. Never invent a note for a source you didn't actually read.
- **Case study count**: 2-5 full worked case studies for design-flavored rounds. Each should
  be a genuinely different scenario (e.g. home-feed ranking vs. search ranking vs.
  cold-start), not variations on one scenario.
- **Interview prompt scenarios**: 5-8 full scenarios (each with Cover + Follow-ups) plus one
  rapid-fire list of 8-15 short questions.
- **Deep-dive priorities**: 10-20 ranked items, each with Terms/Why/Study/Practice.

## Local-only files

`roadmap.md` and `private-notes.md` are both `.gitignore`'d by convention in every
precedent repo — they hold content that's useful to the user locally but isn't meant to be
committed (a personal cram schedule, scratch thoughts). The skill may write `roadmap.md`
to disk; it should never create `private-notes.md` itself, just preserve the `.gitignore`
entry so the user has the option.

## Naming conventions

- Repo: kebab-case, `<company>-<role-abbrev>-<topic>-prep` or `<topic>-interview-prep` (no
  company).
- Files: kebab-case. `topics/` files get a leading two-digit number (`01-`, `02-`, ...);
  `notes/` subfolder files use descriptive slugs without numbering, sorted alphabetically by
  filename.
- Python package in `src/`: snake_case derived from the topic (e.g. `llm_eval_prep`,
  `recsys_ranking_prep`, `fraud_detection_prep`).
