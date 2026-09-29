# skeptical-review

A [Claude Code](https://claude.com/claude-code) skill that critiques a document the way a hard but
fair expert referee would.

## What it does

- States the document's core claim in one sentence, or flags that it can't
- Opens and checks the citations the argument depends on
- Searches for the strongest counter-evidence and the closest prior art
- Scores with anchored 1–5 rubrics for three kinds of document (*arguments*, *proposals*, *plans*),
  calibrated so a 3 means "decent" and 5s are rare
- Flags hard fails: fabricated citations, fatal flaws, ideas that already exist, harm
- Ranks issues by how much they change the conclusion, each with a fix, and separates them from the
  decisions only the author can make
- Supports repeated rounds (it checks whether earlier issues were really fixed)

It reviews; it doesn't rewrite unless asked. It pairs with [`white-paper`](../white-paper/), which
uses it for its review step.

## Layout

```
skills/skeptical-review/
├── SKILL.md               workflow, calibration, output format
└── references/rubrics.md  anchored rubrics per document type, and hard fails
```
