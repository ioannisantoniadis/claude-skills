# white-paper

A [Claude Code](https://claude.com/claude-code) skill that turns the core of an idea (a few
paragraphs, bullets or a voice-note transcript) into a researched, well-argued white paper.

## What it does

- Saves the author's input verbatim (`seed.md`), so there's always a record of the original idea
- Researches the current state, prior art and, first of all, the evidence *against* the idea, with
  dated claims and no invented citations
- Writes the paper from a template built to force what weak idea documents skip:
  - a one-sentence falsifiable thesis
  - load-bearing assumptions, with what would break each
  - scenarios
  - a path with signposts
  - steelmanned counterarguments
  - cheap next steps
  - optional sections for ventures, products, research, policy and projects
- Reviews the draft (with [`skeptical-review`](../skeptical-review/) when it's installed), fixes what
  doesn't need the author, and lists the decisions that do
- Supports full papers (3,000–6,000 words) and briefs (1,500–2,500)

If the working repo has its own template or conventions, those take precedence. The skill was
extracted from a personal "idea garden" repo, where an automated pipeline also drafts and critiques
ideas.

**It never commits or pushes.**

## Layout

```
skills/white-paper/
├── SKILL.md                          workflow
├── assets/template.md                the white-paper template
└── references/research-and-style.md  research rules, style, and guidance per kind
```
