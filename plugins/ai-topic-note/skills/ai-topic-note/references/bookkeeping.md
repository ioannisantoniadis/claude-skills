# Bookkeeping Reference

What each index file is for, its exact format, and whether a new topic actually needs to
touch it. Always re-check the live file before editing — this describes the pattern, the
repo is the source of truth for current content.

## `README.md` — Topic Spine (mandatory for a new top-level topic)

A two-column table: `| <Area name, Title Case> | \`topics/NN-*.md\` |`. Always add a row
here for a new top-level topic file. Not required for a new subsection inside an existing
file.

## `learning-map.md` (conditional)

10 numbered problem-type sections (e.g. "1. Prediction From Labeled Data", "5. Making
Decisions"), each with a "Core methods" bullet list and a "Use when:" line. **No file-path
links at all** — it's a conceptual index organized by problem type, not by topic file. Add
the new topic's core idea as a bullet under whichever existing numbered section it best
fits; only propose a new numbered section if the topic genuinely doesn't fit any of the 10
existing problem types (rare — they're broad).

## `glossary.md` (conditional, keep additions minimal)

Flat, alphabetized, one line per term: `- Term: one-sentence definition.` Currently only
~14 terms — thinner than the 15 topic files would suggest, i.e. already behind. Add genuinely
new terms this addition introduces; don't take this as license to backfill unrelated
existing gaps as a side effect.

## `gap-based-path.md` and `interview-checkpoints.md` (conditional — check scope first)

Both are scoped to the owner's **actual knowledge gaps**, not the full spine. As of the
last check, both cover roughly topics 4-7, 9-10, 12-15 and deliberately skip 1-3, 8, 11
(areas the owner already considers mastered). Re-verify this scope against the live files
rather than trusting these numbers blindly — the point is: **check whether the new topic
falls in the "gap" set or the "mastered" set before touching either file.** If it's in the
mastered set, leave both alone; forcing an entry into a file that's deliberately scoped to
gaps would misrepresent what the owner actually needs to study.

- `gap-based-path.md`: reading order broken into phases, each listing specific
  `topics/NN-*.md` files, things to be able to explain, and practice prompts. A new
  in-scope topic gets added to the phase that makes sense given its dependencies.
- `interview-checkpoints.md`: per-branch bullet lists of interview-style questions,
  organized by branch name (not filepath). A new in-scope topic gets a new bullet list
  under its branch (or a new branch heading if it doesn't fit an existing one).

## `OVERVIEW.md` (optional, highest-effort — ask before doing)

A prose "why things relate" document built around a Mermaid `flowchart LR` with named
`subgraph` clusters (e.g. `Predict`, `Prob`) containing short-ID nodes
(`SL["Supervised Learning<br/>labels -> prediction"]`) and labeled edges naming the shared
concept that makes the connection real (`SL -->|losses, likelihoods,<br/>calibration,
priors| PM`, not just an unlabeled arrow). Adding a topic here means: picking or creating
the right cluster, adding a node with a short ID + one-line subtitle, and adding genuinely
meaningful labeled edges to related existing nodes (read a few real edges in the live file
first to calibrate what "genuinely meaningful" looks like — they name concrete shared
concepts, not vague "related to" links). This is real design work, not mechanical
bookkeeping — always ask whether to do it now or leave it as a follow-up rather than doing
it by default.
