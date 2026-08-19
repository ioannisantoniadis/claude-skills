# Conventions Reference

Exact API and structure conventions from `~/GitHub/algorithm-visualizers`, as they exist
today. If any of this drifts from the real repo, the repo is the source of truth — re-check
`common/theme.py`, `common/ui.py`, and `Home.py` directly rather than trusting this file
blindly if something doesn't match.

## The 8 categories (exact strings, order = nav order)

`"Clustering"`, `"Dimensionality reduction"`, `"Classification & ensembles"`,
`"Deep learning building blocks"`, `"Generative & self-supervised models"`,
`"Graph algorithms"`, `"Probabilistic methods, state estimation & signal processing"`,
`"Reinforcement learning"`.

## `common/theme.py`

- `PALETTE: list[str]` — 10-color categorical palette, identical to
  `.streamlit/config.toml`'s `chartCategoricalColors`:
  `["#6366f1", "#14b8a6", "#f59e0b", "#f43f5e", "#0ea5e9", "#8b5cf6", "#84cc16", "#fb923c", "#06b6d4", "#ec4899"]`
- `FONT_FAMILY = "Inter, -apple-system, Segoe UI, sans-serif"`
- `cluster_colours(n: int) -> list[str]` — cycles `PALETTE` to produce `n` colors.
- `axis_style() -> dict` — shared 2-D axis dict (light gridlines `#eef0f4`, no zeroline,
  thin `#e4e4e7` axis line).
- `base_layout(title=None, *, height=560, xaxis=None, yaxis=None, showlegend=True, margin=None) -> go.Layout`
  — the primary helper. Merges `xaxis`/`yaxis` over `axis_style()`, positions a horizontal
  legend below the plot, `plot_bgcolor="#fbfbfd"`, `paper_bgcolor="rgba(0,0,0,0)"`. Pass
  `title=None` when the page's own progress bar already shows the frame label.
- `base_layout_3d(title=None, *, height=560, scene=None, showlegend=True, margin=None) -> go.Layout`
  — 3-D counterpart.
- `apply_theme(fig, title=None, *, height=560, showlegend=True, margin=None) -> go.Figure` —
  for figures already built via `make_subplots`; mutates and returns `fig`.

Every existing `<algo>/visualize.py` redeclares its own local `_PALETTE` copy of the same
10 hex values rather than importing `theme.PALETTE` — match this unless there's a specific
reason to import directly.

## `common/ui.py`

- Design tokens: `SPACE_XS/SM/MD/LG/XL = "8px"/"12px"/"16px"/"24px"/"32px"`,
  `MAX_CONTENT_WIDTH = "1500px"`.
- `CATEGORY_ACCENTS: dict[str, str]` — one accent hex per category name (must match
  `Home.py`'s `CATALOGUE` keys verbatim), `DEFAULT_ACCENT = "#6366f1"` fallback.
- `category_accent(category: str) -> str`.
- `global_css() -> str` — injected once, **only from `Home.py`**.
- `params_rail(col, title: str = "Configuration")` — `@contextmanager`, renders a label +
  bordered card in `col`:
  ```python
  col_params, col_main = st.columns([1, 3])
  with params_rail(col_params, "Data"):
      shape_name = st.selectbox(..., key=_k("shape"))
  ```
- `badge_row(items: list[tuple[str, str]]) -> None` — pill badges for short categorical
  values, as an alternative to `st.metric`.
- `about_section(why_it_matters: str, references: list[str]) -> None` — renders an
  `st.expander("📚 About this algorithm", expanded=False)`. Call this first inside the main
  column, before the metrics container.

## `Home.py` — `CATALOGUE` and navigation

```python
CATALOGUE = {
    "Clustering": [
        ("apps/kmeans.py", "K-Means", "Manual centroid placement, E/M step-through"),
        ("apps/dbscan.py", "DBSCAN", "Density clustering — core / border / noise points"),
        ...
    ],
    ...
}
```

Adding an algorithm = appending one `(module_path, title, one_line_blurb)` tuple to the
right category's list. `st.navigation` and the home-page card grid both derive from
`CATALOGUE` automatically:

```python
home_page = st.Page(_home_page, title="Home", default=True, url_path="home")
PAGES_BY_PATH: dict[str, st.Page] = {}
nav: dict[str, list[st.Page]] = {"Overview": [home_page]}
for category, items in CATALOGUE.items():
    section_pages = []
    for path, title, _blurb in items:
        p = st.Page(path, title=title)
        PAGES_BY_PATH[path] = p
        section_pages.append(p)
    nav[category] = section_pages
pg = st.navigation(nav)
pg.run()
```

No `.streamlit/pages.toml`, no separate sitemap — `CATALOGUE` is the single registration
point. `apps/` has no `__init__.py` (pages are referenced by path string, not imported as a
package).

## `.streamlit/config.toml` (exact values)

```toml
[theme]
base = "light"
primaryColor = "#6366f1"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8f8fb"
textColor = "#18181b"
borderColor = "#e4e4e7"
baseRadius = "medium"
font = "Inter:https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
chartCategoricalColors = ["#6366f1", "#14b8a6", "#f59e0b", "#f43f5e", "#0ea5e9", "#8b5cf6", "#84cc16", "#fb923c", "#06b6d4", "#ec4899"]

[theme.sidebar]
backgroundColor = "#f8f8fb"
borderColor = "#e4e4e7"

[client]
toolbarMode = "minimal"
```

Never edit this file to fit one new algorithm — it's shared theme, and any per-page color
need should be handled in that page's `visualize.py` instead (see the RL precedent's
hand-picked semantic terrain colors in `references/snapshot-patterns.md`).

## `apps/<algo>.py` page skeleton (condensed — see `assets/templates/app_page.py.tpl` for
the full copyable version)

```python
NS = "dbscan"
def _k(name: str) -> str:
    return f"{NS}__{name}"

st.title("DBSCAN — Step-by-step Visualiser")
caption_slot = st.empty()

col_params, col_main = st.columns([1, 3])
with params_rail(col_params, "Data"):
    ...  # selectbox/slider widgets, all key=_k(...)
with params_rail(col_params, "Algorithm parameters"):
    ...
    regenerate = st.button("🔄 Re-generate", use_container_width=True, key=_k("regen"))

_param_key = (...)  # tuple of every widget value that should trigger a recompute
def _run() -> None:
    st.session_state[_k("snapshots")] = run_algorithm(...)
    st.session_state[_k("step_idx")] = 0
    st.session_state[_k("playing")] = False
if _k("snapshots") not in st.session_state or regenerate or st.session_state.get(_k("_param_key")) != _param_key:
    _run()
    st.session_state[_k("_param_key")] = _param_key

snapshots = st.session_state[_k("snapshots")]
caption_slot.caption(f"...")

with col_main:
    about_section("...", [...])
    with st.container(border=True):
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("...", ...)

    @st.fragment
    def _playback() -> None:
        step_idx = ...  # clamped to [0, len(snapshots)-1]
        playing = st.session_state.get(_k("playing"), False)
        with st.container(border=True):
            speed = st.select_slider("Playback speed", options=["0.5×","1×","2×","4×"], value="1×", key=_k("speed"))
            # Prev / Play / Pause / Next buttons -> mutate session_state -> st.rerun(scope="fragment")
            st.progress(step_idx / max(len(snapshots) - 1, 1), text=f"Frame {step_idx+1} / {len(snapshots)} — {snap.title}")

        fig = make_static_figure(snap, ...)
        with st.container(border=True):
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key=_k("chart"))

        # phase-specific st.info/st.success box
        with st.expander("📖 Reading the chart"):
            st.markdown("""...""")

        if playing:
            if step_idx < len(snapshots) - 1:
                time.sleep(DELAY)
                st.session_state[_k("step_idx")] = step_idx + 1
                st.rerun(scope="fragment")
            else:
                st.session_state[_k("playing")] = False
                st.rerun(scope="fragment")

    _playback()
```
