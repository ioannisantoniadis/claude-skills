---
name: white-paper
description: Turn a rough idea into a researched, well-argued white paper. Keeps the author's input verbatim, researches the current state, prior art and the evidence against the idea, writes to a structured template (thesis, argument, assumptions, factors, scenarios, impact, path, counterarguments, next steps), then reviews and revises it. Use it whenever someone wants to develop, flesh out, write up, stress-test or "properly structure" an idea, thesis, business concept, research direction, policy proposal or project idea, for example "turn this into a white paper", "make this idea robust", or "write this up so I can explore it later", even if they don't say "white paper". Not for summarising an existing paper, short blog posts, or technical design docs for code in a repo.
---

# White paper

Turns the core of an idea (a few paragraphs, bullet points, a voice-note transcript, sometimes with
criteria) into a white paper that argues its case honestly. The idea stays the author's. You
strengthen it; you don't swap it for a different one.

## Before you start: does the repo already have a convention?

Look for an `AGENTS.md`, `CLAUDE.md`, `TEMPLATE.md` or an existing folder of papers in the working
directory. If the repo defines its own template, folder layout, front matter or review format (an
"idea garden", for example), **follow the repo's version**. It overrides everything below, because
the repo's scripts and indexes depend on it. Use this skill's defaults only where the repo says
nothing.

Default layout, when there's no convention:

```
<date>-<slug>/          slug: 3–6 lowercase words from the title
  README.md             the paper (from assets/template.md)
  seed.md               the author's input, verbatim
  review.md             review rounds, newest last
```

Put it where the user says. Otherwise put it in the current directory, and say where.

## Workflow

1. **Save the seed.** Write the author's input exactly as given to `seed.md` under
   `# Seed — <date>`. Later input goes into the same file under `## Addendum — <date>`, and earlier
   text is never changed. The seed is the reference for "did the paper keep the author's idea?", so
   it has to be untouched.
2. **Understand it.** Pull out the core claim, the author's criteria and constraints, and the
   *kind*: `thesis`, `venture`, `product`, `research`, `policy` or `project`. If the claim can be
   read two ways that would produce two different papers, ask the author (at most three questions).
   Otherwise pick the most plausible reading and state it in the review.
3. **Research.** Read `references/research-and-style.md` first. In short: current state, prior art,
   and especially evidence *against* the idea; primary sources; a date on every claim about "today";
   no invented citations (mark anything you couldn't verify `[unverified]`). Keep it proportionate:
   a dozen or two well-chosen sources beats sixty skimmed ones, and every fetched page stays in
   context.
4. **Draft.** Fill in `assets/template.md` as `README.md`. Fill every section; if one doesn't apply,
   say why in one line instead of deleting it. Add the optional sections for the idea's kind (listed
   at the bottom of the template). Keep the author's thesis, their strongest lines and their voice.
   When the evidence contradicts the thesis, the paper says so under Counterarguments. Never quietly
   flip the thesis.
5. **Review.** If the `skeptical-review` skill is available, use it on the draft and write its
   output to `review.md` as `## Round 1`. Otherwise write that review yourself, as a hostile but fair
   referee: scores, ranked issues, what's strong, and decisions for the author.
6. **Revise.** Fix every issue that doesn't need the author's judgement, bump the version, and add a
   revision-history row. Leave the rest as *Decisions for the author* in the review.
7. **Report back** in a few lines: what the paper now argues, the three most important issues, and
   the decisions the author needs to make. Don't commit or push unless asked.

**Length.** A full paper is 3,000–6,000 words. If the user wants a quick look, or is going to judge
many ideas, write a *brief* of 1,500–2,500 words: keep every section, but make each one short.

## Growing an existing paper

When the author comes back with answers or new thoughts, append them to `seed.md` as an addendum,
revise the paper, add `## Round N` to `review.md`, bump `version` and `updated`, and add a
revision-history row. Treat the author's answers to earlier *Decisions* as settled.

## What makes these papers good

The template exists to force the moves weak idea documents skip: a one-sentence falsifiable thesis,
named load-bearing assumptions with what would break them, the strongest objection answered or
conceded, and signposts that would show the idea is wrong. Treat those sections as the point of the
paper, not as boxes to tick. A narrow claim that survives is worth more than a grand one that
doesn't, and an honest "the evidence cuts against this" is a successful outcome.
