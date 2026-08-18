# Content Style Guide

Per-file-type structure and tone, calibrated against the user's existing repos. The voice
throughout is terse, bullet-heavy, second-person-imperative, and built for rehearsal — the
user reads these under time pressure or says them out loud. This is a deliberate choice;
don't drift toward generic AI-listicle prose.

## Topic notes (`topics/NN-*.md`)

Structure:
1. H1 title
2. **Why This Matters** — one short paragraph connecting the topic to what actually gets
   asked.
3. **Core Concepts** — bullets, not paragraphs.
4. Sub-sections with prose explanation as needed.
5. A tradeoff/metrics table.
6. A Mermaid diagram where a system or flow is involved.
7. **Interview Questions To Rehearse** — bullets.
8. **Interview Answer Template** — a literal spoken paragraph, in quotes, the user could say
   almost verbatim in an interview.

Calibration excerpt (from a recsys-ranking precedent repo's topic note):
> "I would separate retrieval, ranking, and reranking." Then define the objective: "For
> this surface, the utility is not just click; I would include long listen, save/follow,
> skip, and retention proxies."

That's the register to aim for in every "Interview Answer Template" — specific, structured,
sayable in one breath, not a wall of bullet points read verbatim.

## Case studies (`notes/case-studies/*.md`)

Numbered sections mirroring an actual interview flow: Clarify → Framing/Metrics →
Architecture (with a Mermaid diagram) → ... → **Trade-offs Summary** table → closing
**"Say This Out Loud"** monologue. This exact heading — "Say This Out Loud" — recurs
verbatim across multiple precedent repos. Use it as-is; it
signals "this is the thing to actually rehearse," not a stylistic flourish to replace.

## Paper / blog notes (`notes/papers/*.md`, `notes/blogs/*.md`)

Rigid template, always in this order:
1. Metadata (Authors / Year / Venue / Link / Tags)
2. One-Sentence Summary
3. Problem
4. Main Idea
5. Method Details
6. Evaluation
7. Production/Interview Relevance
8. Interview Takeaways
9. Open Questions

Citations are real — arXiv links, venue and year, real engineering-blog author/org names.
Never fabricate a citation or invent a source that wasn't actually read this run.

## Glossary (`glossary.md`)

Markdown tables, `Term | Definition`, grouped by category, one-sentence definitions meant
to be spoken aloud without re-reading.

## Templates (`templates/*.md`)

Literal fill-in-the-blank scaffolds — the same section headers as the filled-in versions
above, but with `TODO:` placeholders instead of content. These get copied verbatim into the
generated repo's own `templates/` folder so the user can keep adding notes after the prep
sprint is "done." `TODO:` placeholders belong only here — never in the generated content
itself.

## Code files (`src/*.py`)

Short, dependency-free (or `pytest`-only), heavily docstring-annotated, with an explicit
complexity note and a "Production:" line contrasting the toy implementation with what a
real system would use. Calibration excerpt (`rate_limiter.py`):
> Time per `allow()`: O(1). Space: O(1). Production: Redis cell-based limiter or
> proxy-level limits.

Tests are terse pytest functions, one per edge case, using fake/injectable clocks or
fixtures where relevant — written to be read aloud and explained in an interview, not just
to pass CI silently.

## `interview-brief.md`

The cram sheet. Include, where known:
- The actual interviewer's background if known (calibration excerpt,
  an analytics/data-viz precedent repo): "The interviewer is a Product Analytics Lead
  (analytics background: business analytics MSc, stats/maths, market-research and
  Tableau/SPSS/R experience)."
- Format specifics: round length, tool (CoderPad / whiteboard / HackerRank / take-home),
  number of rounds.
- A likelihood table of question types (e.g. "Very likely / Likely / Central" against
  question categories) — don't hedge everything as equally possible; take a real position
  based on what research actually surfaced.

## `deep-dive-priorities.md`

10-20 ranked items, each with **Terms / Why / Study / Practice** columns or sub-bullets,
grouped into **Highest / Medium / Lower** priority tiers. Include time-boxed cram paths
(1-hour, 4-hour, 1-day, 2-day) so the user can triage by however much time they actually
have left. Every "Why" line should trace to either the JD (quoted, not paraphrased) or to
something found in Step 4 research — never a generic justification.

## `interview-prompts.md`

5-8 full rehearsable scenarios, each with the scenario prompt plus likely follow-ups, and
one rapid-fire list of 8-15 short questions at the end for quick self-testing.

## `README.md`

Section order, consistent across all precedent repos:
1. H1 title (+ optional hero image in `assets/`, only if it's cheap to produce — never
   spend research/writing budget on this before the content itself is done)
2. Framing paragraph — interview context, company, round name/duration, a "not X, but Y"
   contrast (e.g. "not a coding test... a *how do you think with data* conversation")
3. **How To Use This Repo** — a numbered reading flow referencing specific files by name
4. **Topic Map** — a `Area | File` table
5. Repo-specific sections as relevant: **Starter Implementation** (code-backed only),
   **Case Studies** table, **Reference Indexes**
6. **Guiding Questions** — bulleted rhetorical self-test questions
7. **Related Prep Repos** table, if sibling `*-prep` repos exist in `~/GitHub` — `Repo |
   Use When` columns
8. **License** — one line, always last

## What to avoid

- Flashcard-style Q/A dumps with no surrounding structure — every file type above has a
  specific shape; don't collapse into generic bullet lists.
- Hedged, non-committal "it depends" framing where the research actually supports a
  specific position.
- Filler sections that don't map to one of the structures above.
