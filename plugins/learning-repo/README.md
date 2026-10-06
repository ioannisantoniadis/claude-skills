# learning-repo

Three [Claude Code](https://claude.com/claude-code) skills. Two share one rubric: one builds
learning repositories (technical books, notes collections, algorithm demos, research write-ups),
the other audits them. The third compares several repos on equal terms by counting confirmed
defects. A learning repo promises its reader that *what it says is true, and what it shows was
actually computed*. The rubric spells out what keeping that promise takes.

## Skills

- **`learning-repo-audit`**: measures and reports, never fixes.
  - Runs exhaustive mechanical checks with a bundled script: missing and orphan figures, figures
    with no generating script, citation keys, arXiv/DOI existence and title match, dangling paths
    in READMEs, broken links, tests, CI.
  - Builds, tests and renders from a scratch clone.
  - Verifies a sample of about 10 claims against primary sources, weighted toward frontier
    material and specific numbers.
  - Re-runs figure scripts, including with other seeds.
  - Scores nine criteria and writes a severity-ranked report.
  - Can compare several repos in one summary.
- **`learning-repo-build`**: builds a new repo, or upgrades one from an audit report.
  - Researches before writing and logs every source.
  - Builds a ground-truth testbed where the right answer is computable exactly.
  - Writes tests that check the claims.
  - Makes one script per figure, and inspects every image.
  - Generates tables from a single source of truth; keeps a notation appendix, a decision log,
    CI and a clean render.
  - Follows the evidence when it contradicts the spec, and says so.

- **`learning-repo-compare`**: compares repos (or one repo over time) on output quality.
  - Blinded copies: plans, decision logs, research logs and earlier audits removed.
  - Four planted errors per repo, to measure the auditor's own miss rate.
  - A seeded sample of checkable claims plus a full read, by one fresh low-cost auditor per
    repo.
  - Every reported defect confirmed against the original before it counts; the result is
    confirmed defects per 10,000 words, plus a merge-readiness inventory (notation clashes,
    shared devices).
  - Ships the protocol, its scripts and a baseline from the first run on four books.

## The rubric

There are nine criteria, each scored 1–5 against anchors:

1. source fidelity
2. computed evidence
3. claims match measurements
4. correctness
5. pedagogy
6. honesty and currency
7. internal consistency
8. engineering hygiene
9. economy

Three hard fails: a fabricated source, a fabricated result, or a wrong core claim. Severity
runs blocker / major / minor / polish. Profiles cover books, notes, apps and research codebases.
The rubric lives in `learning-repo-audit/references/rubric.md`; the build skill links to it, so
there is one copy.

## Layout

```
skills/
├── learning-repo-audit/
│   ├── SKILL.md                    workflow, ground rules, report format
│   ├── references/rubric.md        the shared rubric
│   └── scripts/
│       ├── mechanical_checks.py    exhaustive checks (images, scripts, citations, paths, hygiene)
│       └── compare_figures.py      triage regenerated figures against the committed ones
├── learning-repo-compare/
│   ├── SKILL.md                    workflow, ground rules, pitfalls
│   ├── references/
│   │   ├── protocol.md             blinding, planting, sampling, auditing, metrics
│   │   └── baseline-2026-10.md     first run: four books, densities, sensitivity
│   └── scripts/
│       ├── blind_copy.py           blinded copy of a repo
│       ├── inventory.py            claim inventory and seeded stratified sample
│       └── metrics.py              defect rates, Wilson intervals, kappa
└── learning-repo-build/
    ├── SKILL.md                    phases, standing rules
    └── references/
        ├── playbook.md             research, testbed, tests, figures, devices, templates, pitfalls
        └── rubric.md -> ../../learning-repo-audit/references/rubric.md
```

The build and audit skills were distilled from building
[rl-for-llms](https://github.com/ioannisantoniadis/rl-for-llms); the compare skill from assessing
it against its siblings while building [data-lab](https://github.com/ioannisantoniadis/data-lab).
