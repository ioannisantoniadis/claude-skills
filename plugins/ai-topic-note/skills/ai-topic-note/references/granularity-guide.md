# Granularity Guide

The decision that matters most before writing a word. Three shapes, in order of
preference (cheapest/lowest-risk first):

## 1. New subsection inside an existing `topics/NN-*.md` file (default)

Use when the new material extends, specializes, or fills in more depth on a subject an
existing topic file already covers. Zero cross-file bookkeeping is mandatory (README's
Topic Spine row already exists for the parent topic). This should be the default choice
whenever it's plausible — most "I learned about X" additions specialize something already
in the spine rather than opening a genuinely new area.

To decide: skim the 15 existing `topics/*.md` headers (or `README.md`'s Topic Spine table
for the one-line area names) and ask whether the new material is a *deeper look at* one of
them, or something none of them actually cover.

## 2. New top-level `topics/NN-*.md` file

Use only when the topic is a genuinely distinct subject area — not a deeper look at
something existing, but new ground.

**Numbering**: default to appending as the next number (check the highest existing
`topics/NN-*` and use N+1) regardless of where the topic would "ideally" sit in a
pedagogical sequence. The 01-15 numbering is a real, meaningful teaching order (roughly
foundational → applied, per `OVERVIEW.md`'s five-cluster structure) with no gaps and no
`N.5`-style insertion convention — inserting mid-sequence means renaming every subsequent
file and updating every place that references a topic by number (README's Topic Spine,
`gap-based-path.md`, `interview-checkpoints.md`, `OVERVIEW.md` if it references topics by
number anywhere). That cascade is real cost, not paranoia — only take it on if the user
explicitly wants correct pedagogical placement, and tell them what it touches before doing
it.

## 3. Single-technique entry (rare, no established format)

`templates/method-card.md` exists (One-Sentence Definition → Use When → Avoid When →
Inputs/Outputs → Assumptions → Strengths → Weaknesses → Related Methods → Interview
Explanation) but a repo-wide search turns up **zero actual uses of it** — it's aspirational,
not proven. There's also no `notes/methods/`-style directory anywhere for it to live in.

If a user genuinely wants single-technique granularity (narrower than a whole topic, e.g.
one specific algorithm or paper rather than a subject area), the lowest-risk choice is
still a subsection inside the most relevant existing topic file, written in that file's
voice — not a stand-alone method-card file whose location and cross-linking convention
would have to be invented from scratch. If the user insists on the method-card format
specifically, use it, but flag clearly that this establishes a new convention rather than
following an existing one, and ask where they want it to live.

## What NOT to do

Don't default to "always make a new topic file" just because it's the most visible option —
the survey that produced this skill found real evidence the repo's own maintainer treats
topic files as a meaningful, curated spine (15 files, terse, no padding) rather than a
dumping ground. A new file for everything would dilute exactly what makes this repo useful
as a fast reference.
