# ai-topic-note

A [Claude Code](https://claude.com/claude-code) skill that adds a new topic — or extends an
existing one — to an existing personal AI/ML knowledge-base repo, in its established
terse, declarative, no-citation reference style.

## What it does

Given a topic or concept, and roughly how well it's already understood, it:

- Decides where the addition actually belongs first — a new subsection inside an existing
  topic file (cheapest, default), a genuinely new top-level topic file (only for real new
  ground, appended rather than inserted mid-sequence to avoid a renumbering cascade), or —
  rarely — a narrower single-technique entry
- Writes it in the repo's real voice: `## Core Idea` → bespoke middle → `## Interview
  Check`, dense and declarative, no padding, no inline citations
- Updates only the index files that actually apply — a repo like this accumulates several
  (a topic spine table, a problem-type map, a glossary, gap-scoped checkpoint files, a
  Mermaid field-connection diagram) and touching all of them by default would be wrong as
  often as it'd be right

**It never commits or pushes.** Changes are left as uncommitted working-tree edits for
review.

## Design notes

Built by auditing a real 15-topic personal knowledge-base repo and finding, among other
things, that its own `templates/method-card.md` had never actually been used anywhere —
the kind of thing that only shows up from reading the real repo rather than assuming its
templates are load-bearing. See `skills/ai-topic-note/references/` for the full findings.

## Install

```
/plugin marketplace add ioannisantoniadis/claude-skills
/plugin install ai-topic-note@claude-skills
```
