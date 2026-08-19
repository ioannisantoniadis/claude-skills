# algorithm-visualizer

A [Claude Code](https://claude.com/claude-code) skill that adds a new algorithm to an
existing Streamlit + Plotly "algorithm visualizers" portfolio repo — a multipage app of
from-scratch NumPy implementations, each paired with an interactive step-by-step
walkthrough — following that repo's exact established convention instead of re-deriving it
per addition.

## What it does

Given an algorithm and a description of what's worth stepping through, it:

- Designs the right `Snapshot` shape (sparse/event-based vs. dense/per-step, based on
  whether the algorithm has discrete phases or is a uniform iterative loop)
- Implements a from-scratch NumPy core, numerically verified before moving on
- Builds matching synthetic dataset/environment generators
- Builds Plotly figures using the shared theme (palette, fonts, card layout)
- Builds the Streamlit page itself — playback controls, session-state namespacing,
  `st.fragment`-scoped autoplay — matching every other page in the app pixel-for-pixel
- Registers it in the app's navigation catalogue
- Actually runs the app and clicks through the new page looking for the class of bugs this
  kind of app tends to produce (duplicate element IDs, unclamped frame-index crashes, state
  leaking between pages)

**It never commits or pushes.** The target repo auto-deploys to a public site on every push
to `main`, so this skill always leaves its changes as uncommitted working-tree edits for
review.

## Design notes

Built by extracting the actual conventions from a real 20-algorithm portfolio repo — its
`common/theme.py` and `common/ui.py` helper APIs, its `Home.py` catalogue-registration
pattern, and two genuinely different `Snapshot` precedents (an event-based clustering
algorithm and a dense-per-step RL loop) — documented in `skills/algorithm-visualizer/references/`
so new additions read as a continuation of the pattern, not a bolt-on.

## Install

```
/plugin marketplace add ioannisantoniadis/claude-skills
/plugin install algorithm-visualizer@claude-skills
```
