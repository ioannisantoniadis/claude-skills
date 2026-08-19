---
name: algorithm-visualizer
description: Add a new algorithm to the existing ~/GitHub/algorithm-visualizers Streamlit portfolio repo — a from-scratch NumPy implementation with step-by-step Plotly visualization, following that repo's exact established convention (Snapshot-per-step pattern, shared theme, session-state namespacing, playback controls). Use whenever the user wants to "add an algorithm visualizer", "visualize <algorithm> like the others in my portfolio", "add <X> to algorithm-visualizers", or wants a new interactive step-by-step demo of a classic ML/CS algorithm added to that specific repo. This modifies an EXISTING repo (not a new one) and never commits or pushes on its own.
---

# Algorithm Visualizer Adder

Adds one new algorithm to `~/GitHub/algorithm-visualizers` — a portfolio Streamlit
multipage app of ~20 classic ML/CS algorithms, each a from-scratch NumPy implementation
paired with an interactive step-by-step Plotly walkthrough. This skill extends that one
existing repo; it does not create a new repo.

The convention here is unusually well-documented already — the repo's own `CLAUDE.md`
records exactly how it came to exist and what broke during the original build (crashes
from unclamped frame-index state, duplicate-element-ID errors, a real algorithm bug found
via live testing). Read `references/gotchas.md` before touching CSS, navigation, or
session state — every item there was a real bug once.

## Step 1 — Confirm target and gather the algorithm spec

Verify `~/GitHub/algorithm-visualizers` exists; if not, ask the user (it may have moved).

Required: which algorithm, and what makes it worth stepping through — the sequence of
intermediate states a learner would want to see (e.g. "each E/M iteration", "each grid cell
visited during BFS", "each gradient-descent update"). If the user just names an algorithm
without describing what to visualize, propose a specific step sequence yourself and confirm
before implementing — this is the single decision that shapes everything downstream.

Also determine:
- **Category**: one of the 8 existing categories (see `references/conventions.md` for the
  exact list) or a genuinely new one. Read `Home.py`'s `CATALOGUE` dict to see current
  entries and pick based on where this algorithm actually fits.
- **Module name**: short snake_case, becomes `<algo>/` and `apps/<algo>.py`. Check it
  doesn't already exist (`grep '"apps/<algo>.py"' Home.py`).

## Step 2 — Design the Snapshot shape

Read `references/snapshot-patterns.md` now — it documents two real, meaningfully different
precedents (a sparse event-based clustering algorithm vs. a dense per-step RL loop) and
gives the decision rule for which shape fits a new algorithm:

- **Sparse/event-based** snapshots (record only meaningful state transitions — a handful to
  a few dozen total) for algorithms with discrete phases or combinatorial structure
  (clustering, graph search, tree building).
- **Dense/per-step** snapshots (one per iteration/episode-step, possibly hundreds) for
  numerical optimization loops or RL — pair with frame subsampling for the animated variant
  if the step count could realistically exceed ~200.

Every `Snapshot` needs, at minimum: enough state to redraw the chart at that instant, a
`phase: Literal[...]` field if the algorithm has discrete phases, and a `title` property
that builds the human-readable per-frame caption (this drives the progress-bar text, not a
repeated chart title).

## Step 3 — Implement `<algo>/algorithm.py`

From-scratch NumPy only — no scikit-learn, no PyTorch, no other ML framework in the core
algorithm (this is the repo's central portfolio claim; don't compromise it for convenience).

Verify numerical correctness before moving on — against a known closed-form result, a
finite-difference gradient check, or a reference implementation's output on a small fixed
input. This was step 1 of the original build process for every existing algorithm; skipping
it is how subtle bugs (the repo's `CLAUDE.md` cites a real one — a UMAP SGD update that only
touched one side of each edge) ship silently.

The main function returns `list[Snapshot]`, appending one `Snapshot(...)` per step per the
Step 2 design. Use `copy.deepcopy` or `.copy()` on any mutable array/object stored in a
snapshot — snapshots must be independent frames, not views into mutating state.

## Step 4 — Implement `<algo>/data.py`

One or more named synthetic dataset/environment generators (e.g. `make_blobs`,
`make_moons` for point clouds; a `GridWorld`-style dataclass for RL/graph environments).
Export a dispatcher (`make_dataset(name, ...)` or `make_grid(preset, ...)`) plus
`*_KEYS`/`*_NAMES` constants the Streamlit page uses to populate a selectbox. Match the
existing repos' pattern of 3-6 named presets rather than one fixed dataset — variety is
part of what makes the visualizer worth exploring more than once.

## Step 5 — Implement `<algo>/visualize.py`

Import `base_layout` (or `base_layout_3d` for 3-D) from `common.theme`. Redeclare a local
`_PALETTE` copy of the 10-color categorical palette (existing convention — see
`references/conventions.md` for the exact hex values) rather than importing it, unless the
figure needs semantically-meaningful colors (e.g. a heatmap where color encodes a domain
concept, not a category) — in that case hand-pick colors and say so in a comment, matching
how the RL precedent handles terrain-type colors.

Provide at least a `make_static_figure(snapshot, ...)` for manual step-by-step playback.
Add `build_figure(snapshots, ...)` for an animated multi-frame version only if it adds real
value beyond the manual playback the app page already provides. Pass `title=None` to
`base_layout` when the page's own progress bar already shows the frame label — don't
duplicate it as a chart title.

## Step 6 — Implement `<algo>/__init__.py`

Re-export the public API (`Snapshot`, the main algorithm function, the data generators and
their key/name constants) even though `apps/<algo>.py` will import from submodules
directly — this matches every existing algorithm package and keeps the API surface
consistent for anyone importing the package from outside `apps/`.

## Step 7 — Implement `apps/<algo>.py`

Read `references/conventions.md` now for the exact page skeleton (title → params rail →
about section → metrics container → `@st.fragment`-wrapped playback block → chart →
phase-specific info box → expander). Start from **the closest existing page in the same
category** (e.g. a new probabilistic/state-estimation algorithm should start from
`apps/kalman.py` or `apps/mcmc.py`, not from scratch), not just
`assets/templates/app_page.py.tpl` — the template is a correct floor that guarantees the
load-bearing mechanics below, but real categories have accumulated richer, more specific
conventions (comparison panels, extra legends, disabled-state handling) that only show up
by reading a real sibling. Use the template to check nothing load-bearing got lost when
adapting a sibling page, not as the primary source to build from. Load-bearing details,
either way:

- `NS = "<algo>"` then every single `st.session_state` key and every widget's `key=` goes
  through `_k(name) -> f"{NS}__{name}"`. No bare keys, ever — this is how two algorithm
  pages would end up silently sharing state in one Streamlit session.
- `st.set_page_config(...)` and the global CSS injection belong **only** in `Home.py`.
  Never add them here.
- The playback block (metrics, chart, controls) is wrapped in `@st.fragment` so autoplay's
  `st.rerun()` doesn't flicker the whole page. The auto-advance
  `time.sleep(DELAY); st.rerun(scope="fragment")` must be the **last statement** in that
  fragment function.
- `st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key=_k(...))`
  — the `displayModeBar` config lives at this call site, not inside `visualize.py`.
- Wrap `params_rail`, the metrics row, and the chart each in `st.container(border=True)`
  (imported from `common.ui`) for the card look every other page uses.
- Call `about_section(why_it_matters, references)` from `common.ui` as the first thing in
  the main column, before the metrics container.

## Step 8 — Register in `Home.py`

Add exactly one tuple to the chosen category's list in the `CATALOGUE` dict:
`("apps/<algo>.py", "<Display Title>", "<one-line blurb>")`. This is the **only** mandatory
registration point — `st.navigation` and the home-page card grid both derive from
`CATALOGUE` automatically, nothing else needs wiring.

If this genuinely needs a new category (not one of the existing 8), add the new key to
`CATALOGUE` and add a matching entry to `CATEGORY_ACCENTS` in `common/ui.py` — otherwise it
falls back to the default accent color, which is a visible (if minor) inconsistency.

Update the category table in `README.md` to add the new algorithm — it's meant to mirror
`CATALOGUE` and existing entries keep it in sync.

## Step 9 — Verify by actually running the app

Read `references/gotchas.md` before this step — several real bugs in this repo's history
only manifested inside the real running multipage app, not by reading a single file in
isolation.

Run `uv sync && uv run streamlit run Home.py` and click through the new page: step through
manually with Prev/Next, run Play through to completion, drag every slider to its min and
max, hit Re-generate/reset if the page has one, and navigate away and back. Watch for
crashes, `StreamlitDuplicateElementId` errors, and visual breakage. If browser automation
tools are available, drive this directly and report what you found; otherwise ask the user
to click through and report back before considering the algorithm done.

## Step 10 — Hand off without committing

**Do not run `git add`, `git commit`, or `git push`.** This repo auto-deploys to a public
Streamlit Community Cloud site on every push to `main` — that is a real, visible action
this skill must never take on its own. Leave the new files as uncommitted working-tree
changes and summarize what was added (files created, category, `CATALOGUE` entry) so the
user can review the diff, test it themselves, and commit/push when they're ready.

## Quality bar

- No scikit-learn/PyTorch/etc. in `<algo>/algorithm.py` — from-scratch NumPy is the whole
  point of this portfolio.
- Numerical correctness actually checked, not assumed.
- Every `st.session_state` key and widget `key=` goes through `_k(...)` — no exceptions.
- Match the existing visual language (indigo/teal palette, Inter font, bordered cards,
  `displayModeBar: False`) exactly — this is one visual product across ~20 pages, not 20
  independent ones.
- Never touch `Home.py`'s `st.set_page_config`/global-CSS lines or add them elsewhere.
- Never commit or push.
