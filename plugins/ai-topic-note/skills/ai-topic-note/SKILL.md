---
name: ai-topic-note
description: Add a new topic (or extend an existing one) to the existing ~/GitHub/modern-ai-systems-and-methods personal AI/ML knowledge base, in its established terse-reference-prose style. Use whenever the user wants to "add a topic to my AI notes", "write up <ML/AI concept>" for that repo, learned something new and wants to capture it, or mentions extending "modern-ai-systems-and-methods". This modifies an EXISTING repo (not a new one) and never commits or pushes on its own — the user reviews and commits when ready.
---

# AI Topic Note Adder

Adds a new topic — or a new subsection within an existing one — to
`~/GitHub/modern-ai-systems-and-methods`, the user's personal, evolving AI/ML reference
spine. This skill extends that one existing repo; it does not create a new repo, and unlike
`interview-prep-repo` this is not research-and-citation-driven — the repo's own voice is
dense, declarative, synthesized understanding with **no inline citations** (verified: zero
`(2019)`-style or `et al.` references anywhere in `topics/*.md`). External sources live
separately in `references/books.md` / `references/courses.md` as curated reading lists, not
woven into the prose.

## Why granularity matters more than content here

This repo is not research-backed the way the interview-prep repos are — the hard part isn't
finding sources, it's deciding **where a new idea belongs** in an already-coherent
15-topic spine before writing a word. Read `references/granularity-guide.md` now — it
covers the decision that most determines whether this addition strengthens the spine or
just bolts a file onto the end of it.

## Step 1 — Gather input and classify it

Confirm `~/GitHub/modern-ai-systems-and-methods` exists (ask if not — it may have moved).

Required: the topic or concept to add, and roughly how much the user already understands it
— genuinely new territory, or something they know but haven't written up yet. This matters
because two of the repo's files (`gap-based-path.md`, `interview-checkpoints.md`) are
explicitly scoped to the owner's *actual knowledge gaps*, not the full 15-topic spine — see
`references/bookkeeping.md` for exactly which topics they currently cover and don't.

## Step 2 — Decide where it goes

Read `references/granularity-guide.md` and pick one of three shapes:

1. **New top-level `topics/NN-*.md` file** — only for a genuinely distinct subject area not
   covered by any existing topic. Default to appending as the next number (currently `16`)
   regardless of where it would "ideally" sit pedagogically — inserting mid-sequence forces
   a renumbering cascade across every cross-referencing file (README's Topic Spine,
   `gap-based-path.md`, `interview-checkpoints.md`, any inbound `OVERVIEW.md` edges). Only
   do that cascade if the user explicitly asks for correct pedagogical placement, and warn
   them what it touches before doing it.
2. **New subsection inside an existing `topics/NN-*.md` file** — the default for anything
   that extends or specializes a subject already covered. Cheapest option: no renumbering,
   no mandatory cross-file bookkeeping. Prefer this unless the topic clearly doesn't fit
   under any existing file's scope.
3. **A single-technique entry narrower than a full topic** — genuinely uncharted territory
   in this repo: `templates/method-card.md` exists but has never actually been used anywhere
   (verified via repo-wide search). Don't treat it as a proven format. If the user
   specifically wants this granularity, the lowest-risk choice is a new subsection inside
   the most relevant existing topic file, written in the same voice as the rest of that
   file — not a stand-alone method-card file with no precedent for where it would even live.

## Step 3 — Write in the established voice

Read `references/voice-and-structure.md` for the real structural pattern (every existing
topic file opens with `## Core Idea` and closes with `## Interview Check`; everything
between is bespoke per topic, not a fixed template) and calibration excerpts for tone.

Match length to precedent: existing topic files run 38-70 lines total. Don't pad a thin
topic to look more complete, and don't undershoot a genuinely broad one — let the actual
depth of the subject decide, the same "don't pad" principle as the interview-prep skills'
topic counts.

No inline citations. If a specific book or course was the actual source for this addition
and isn't already in `references/books.md` / `references/courses.md`, offer to add it there
under the right category — that's the one place external sources belong in this repo.

## Step 4 — Update the mandatory bookkeeping

Add a row to `README.md`'s **Topic Spine** table (`| <Area name> | \`topics/NN-*.md\` |`).
This is the one index that's consistently kept current — always update it, even for a new
subsection (only if that subsection is significant enough to warrant its own spine mention;
most subsections don't need a separate row).

## Step 5 — Update the conditional bookkeeping

Read `references/bookkeeping.md` for exactly what each of these covers and whether this
addition falls in scope — don't touch files that don't apply:

- **`learning-map.md`** — add to the relevant existing numbered problem-type section, or
  flag if a genuinely new section seems warranted (rare — there are 10 already, spanning
  the field broadly).
- **`glossary.md`** — append any new terms this topic introduces, matching the existing
  flat `- Term: one-sentence definition.` format. This file is currently thin/behind the 15
  topics — don't feel obligated to backfill unrelated gaps, just don't add to the debt.
- **`gap-based-path.md`** and **`interview-checkpoints.md`** — only touch these if Step 1
  established this is a genuine knowledge gap for the owner, matching the scope those files
  already cover. If the topic is in the "already mastered" set, leave both alone.
- **`OVERVIEW.md`** — the most labor-intensive: adding a real subsection under the right
  problem-framing cluster in the Mermaid `flowchart LR`, plus labeled edges to genuinely
  related existing nodes (the edge labels name the *shared concept*, not just "related to").
  This is optional, higher-effort bookkeeping — ask whether to do it now or leave it as a
  follow-up, rather than assuming.

## Step 6 — Hand off without committing

**Do not run `git add`, `git commit`, or `git push`.** Leave the new/edited files as
uncommitted working-tree changes and summarize exactly what was touched (new topic file or
subsection, which index files were updated and which were deliberately left alone and why)
so the user can review the diff and commit when they're ready.

## Quality bar

- Get the granularity decision right before writing — a good topic in the wrong place (a
  new top-level file that should've been a subsection, or vice versa) is worse than a
  slightly-imperfect topic in the right place.
- Voice matches: terse, declarative, `## Core Idea` → `## Interview Check` bookends, no
  inline citations, no padding to hit a length target.
- Never touch files outside what Steps 4-5 actually call for — this repo's own bookkeeping
  is already inconsistent (a thin glossary, checkpoint files scoped to a subset of topics);
  don't "fix" that scope creep as a side effect of adding one topic.
- Never commit or push.
