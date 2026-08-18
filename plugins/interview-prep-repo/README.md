# interview-prep-repo

A [Claude Code](https://claude.com/claude-code) skill that scaffolds a complete,
research-backed interview-prep repository for an upcoming job interview — instead of
re-explaining the same structure to an agent every time a new interview comes up.

## What it generates

Given a topic (e.g. "recsys ranking", "LLM evaluation", "ML systems design"), optionally a
company name, and optionally a job description, it produces a new sibling repo under
`~/GitHub` with:

- `topics/*.md` — reference-depth notes per subtopic, each ending in a spoken-paragraph
  "Interview Answer Template"
- `notes/papers/`, `notes/blogs/` — distilled notes on real papers and engineering blog
  posts actually found via web research (no fabricated sources or citations)
- `notes/case-studies/` — full worked design scenarios, each closing with a rehearsable
  "Say This Out Loud" summary
- `interview-brief.md` — the cram sheet: format, likely question types, what to expect
- `deep-dive-priorities.md` — study time triaged by likely question weight, tied to the job
  description when one is provided
- `interview-prompts.md` — rehearsable scenario prompts plus a rapid-fire question list
- for hands-on rounds only: a small, dependency-free `src/` package with passing `tests/`,
  so there's something concrete to talk through live

The skill decides between a "code-backed" and "design-only" repo variant based on the round
type, and prefers doing its research and file-writing as a background task so a single
generation doesn't consume the whole conversation.

## Design notes

This was built by auditing a set of real interview-prep repos that converged on a
consistent structure across several independent job searches — the skill's `references/`
directory documents that convention (file skeletons, naming rules, content style per file
type) so generated repos read as a genuine continuation of the pattern rather than generic
AI output. See [`skills/interview-prep-repo/SKILL.md`](skills/interview-prep-repo/SKILL.md)
for the full process.

## Install

```
/plugin marketplace add ioannisantoniadis/claude-skills
/plugin install interview-prep-repo@claude-skills
```

Or, for local development without the marketplace flow, symlink the skill directly:

```
ln -s "$(pwd)/skills/interview-prep-repo" ~/.claude/skills/interview-prep-repo
```
