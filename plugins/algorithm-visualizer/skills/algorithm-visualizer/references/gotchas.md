# Gotchas Reference

Real bugs found in this repo's history, preserved so a new algorithm doesn't reintroduce
them. Source: the repo's own `CLAUDE.md`, condensed here for this skill's use.

- **Streamlit CSS specificity.** Streamlit's own emotion-generated styles carry strong
  specificity, sometimes attribute-selector-tied. If a CSS override doesn't visibly take
  effect, check computed styles directly rather than assuming the selector is wrong — you
  likely need `!important` and/or a more specific selector. This shouldn't come up for a
  new algorithm page (page-specific CSS is rare and discouraged — reuse `common/ui.py`'s
  existing classes instead of writing new CSS).
- **`:has()` for CSS scoping**, if any page-specific styling is ever truly necessary — so it
  can't bleed onto other pages' bordered containers. Prefer this over ad-hoc classes.
- **Widget-value reset on page navigation is a real, observed, *harmless* quirk.** Leaving a
  page and returning can reset some widgets to their script-default value — systemic to how
  `st.navigation` handles widget lifecycle, not a bug in any specific page. Don't spend time
  "fixing" this unless it starts actually breaking something (wrong data shown, a crash).
- **`st.set_page_config` and the global CSS block belong only in `Home.py`.** Adding either
  to `apps/<algo>.py` will error (page config can only be called once) or produce duplicate
  `<style>` tags. Never add them to a new page.
- **Test inside the real running multipage app**, not by reading `apps/<algo>.py` in
  isolation. Several historical bugs in this repo only manifested inside real navigation:
  stale state carried across pages, duplicate element IDs from two charts rendering on one
  page, unhandled crashes from unclamped frame-index state after a parameter change. Run
  `uv run streamlit run Home.py` and actually click through — see SKILL.md Step 9.
- **`StreamlitDuplicateElementId`** has broken a page's default load before. Every widget
  and every `st.plotly_chart` needs an explicit, namespaced `key=_k(...)` — this is the
  single most common cause.
- **A real algorithm bug this repo has actually shipped**: a UMAP SGD update that only
  touched one side of each edge. The lesson generalizes — verify numerical correctness
  against something independent (finite-difference check, closed-form result, reference
  implementation on a small fixed input) before trusting a from-scratch implementation, per
  SKILL.md Step 3. Visual plausibility in a demo is not the same as correctness.
- **Dead click-to-draw features from a Plotly `hoverinfo="skip"` footgun** have happened
  before — if a new page wants any click/hover interactivity beyond the standard playback
  controls, verify it actually fires in the running app, not just that the code looks right.
