---
name: learning-repo-build
description: Build, or upgrade, a learning repository that teaches a technical subject from first principles (a Quarto book with computed figures, a notes collection, interactive algorithm demos, or a research write-up) to a rigorous standard. It researches primary sources before writing anything and logs them, builds a small ground-truth testbed where the right answer is computable exactly, tests that check the claims numerically, one script per figure from real computation with every image inspected, single-source-of-truth tables, a notation appendix, CI and a clean render, and a decision log. Use it whenever the user wants to write a technical book, tutorial series, explainer repo, "lab", course notes or visualization app for learning, or to fix, upgrade or remediate one after an audit, even if they don't say "learning repo".
---

# Learning-repo build

A learning repo is worth reading only if the reader can trust it without checking. Everything in
this workflow serves that: **research before writing, compute instead of illustrating, test
the claims rather than just the code, and look at every output.** The standard is the shared
rubric in `references/rubric.md` (the same one `learning-repo-audit` scores against). Read it
first. Practical detail, templates and known pitfalls are in `references/playbook.md`. Read the
relevant section when you reach each step.

## Two modes

- **New build**: from a topic or a spec. Follow the phases below in order.
- **Upgrade**: from an audit report (`learning-repo-audit`) or the user's list of problems. Read
  the report, confirm the fix list and its order with the user (blockers first), then apply the
  same phases to just the affected parts. Re-run the mechanical checks at the end and report
  each finding as fixed, skipped (with the reason) or disputed (with evidence).

## Standing rules

These hold throughout, and apply to the user's own spec too:

1. **Never write technical content from memory.** Equations, defaults, hyperparameters, reported
   results, dates and author lists come from the primary source, opened and read. Record each
   source in `research-log.md`: URL, what was checked, what couldn't be verified. Models are
   most wrong about recent work and specific numbers, and those are exactly what readers copy.
2. **Follow the evidence.** If research shows the spec (or the user, or an earlier chapter) is
   wrong, don't silently follow it and don't silently deviate. Note the discrepancy in the
   research log, follow the evidence, and tell the user.
3. **Every figure is a real computation.** One script per figure, committed, producing a
   committed image. If a picture is schematic, label it as schematic. Before writing a figure
   script, you should be able to finish the sentence "this figure makes visible that …". Put that
   sentence in the script's docstring.
4. **Look at everything you produce.** Open every image after generating it, and read the rendered
   page. Label collisions, wrong axes and misleading scales are only caught by looking.
5. **Claims match measurements.** Quote numbers from a fresh run. Scope generalizations to what
   was measured. If an effect appears on only some seeds, say so and show the spread.
6. **Ask only for decisions that are genuinely the user's** (scope, audience, thesis, what to
   cut). Make everything else yourself, and record the reasoning in `ROADMAP.md`.
7. **Don't commit or push unless asked.** `git init` is fine.

## Phase 1: scope, then stop for approval

1. **Read the neighbors.** Read the user's sibling repos on adjacent topics, so notation,
   conventions and scope boundaries line up and topics owned elsewhere get a link rather than a
   rewrite.
2. **Pin down the thesis and the reader.** State the thesis in a few sentences: the one argument
   the repo makes. Name the reader and what they already know. A catalogue of facts isn't a thesis.
3. **Do an initial research pass** over the core sources (see *Research* in the playbook), logged
   as you go.
4. **Scaffold the project docs.**
   - `README.md`
   - `CONVENTIONS.md`: chapter template, recurring devices, evidence levels, figure rules
   - `ROADMAP.md`: plan, status, decision log
   - `research-log.md`
   - `CLAUDE.md`
   - a notation appendix
   - build config, CI (lint, tests), docs deploy
   - stubs for every page

   Templates are in the playbook.
5. **Build the ground-truth testbed** before any content that depends on it. Choose the smallest
   setting in which the truth is computable *exactly* (enumeration, closed form, a tiny state
   space), so every method can be measured against the right answer rather than eyeballed. Write
   tests that check the repo's central derivations against it.
6. **Make the signature figure first**: the one picture the thesis rests on. If it doesn't come out
   clearly, the framing needs rethinking, and it's cheaper to find that out now.
7. **Stop and report**: what was built, what the signature figure showed (including surprises),
   the decisions you need from the user, and anything in the spec that research contradicted.

## Phase 2: write, one unit at a time

Before you start each chapter, page or app:

1. **Research it first.** Read the primary sources and search for later work that corrects or
   disputes them. Log everything.
2. **Implement and test.** Implement what the unit needs, with tests that check its claims
   numerically.
3. **Generate figures.** Generate its figures with real computation, look at each one, and
   iterate. Check robustness: re-run the key result with other seeds or settings when the claim
   is about typical behavior.
4. **Write it** to the template in `CONVENTIONS.md`:
   - motivate (what problem, and which earlier limitation)
   - state assumptions, with what breaks if each fails
   - derive, then box the result
   - interpret: what does optimizing or using it *actually* produce?
   - failure modes, with a figure
   - connections to 2–4 neighboring units, saying why each is related

   Label every empirical claim as mathematical fact, replicated finding, or recent or contested.
   Date anything frontier.
5. **Check it against the rubric** before moving on:
   - every symbol is in the notation appendix;
   - every cross-reference resolves;
   - every quoted number matches the latest run;
   - lint and tests pass, and the render has no warnings.

   Mark the unit done in `ROADMAP.md`, with anything notable in the log.

When all units are done, write the synthesis (map, decision guide, summary tables), generated from
data rather than retyped where possible. Then run a full self-audit: the mechanical checks
script from `learning-repo-audit` (at `../learning-repo-audit/scripts/mechanical_checks.py`, or
wherever that skill is installed), plus a re-read of the rubric. Fix what it finds, then report.

## Finishing

Report to the user:
- what was built;
- the test, render and CI status;
- every discrepancy where evidence overrode the spec;
- the claims that could not be verified;
- the decisions still open.

Offer, don't perform: commit, push, create the GitHub repo, enable Pages, update the profile
README. Each waits for the user's go-ahead.
