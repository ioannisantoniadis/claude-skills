"""TODO: <Algorithm Name> — Streamlit page.

Never add st.set_page_config(...) or the global CSS injection here — both belong
only in Home.py. See references/gotchas.md.
"""
from __future__ import annotations

import time

import streamlit as st

from common.ui import about_section, params_rail
from TODO_algo.algorithm import run  # TODO: real package name and function name
from TODO_algo.data import PRESET_KEYS, PRESET_NAMES, make_dataset
from TODO_algo.visualize import make_static_figure

NS = "TODO_algo"  # short, unique per page


def _k(name: str) -> str:
    return f"{NS}__{name}"


st.title("TODO: <Algorithm Display Name> — Step-by-step Visualiser")
caption_slot = st.empty()  # filled in after params are known, below

col_params, col_main = st.columns([1, 3])

with params_rail(col_params, "Data"):
    preset = st.selectbox(
        "Preset",
        options=PRESET_KEYS,
        format_func=lambda k: PRESET_NAMES[k],
        key=_k("preset"),
    )
    seed = st.number_input("Seed", value=0, step=1, key=_k("seed"))

with params_rail(col_params, "Parameters"):
    # TODO: algorithm-specific sliders/selects, every one with key=_k("...")
    regenerate = st.button("🔄 Re-generate", use_container_width=True, key=_k("regen"))

with col_params:
    with st.expander("How this algorithm works", expanded=False):
        st.markdown("""TODO: short explanation.""")

# Every value that should trigger a recompute goes in this tuple.
_param_key = (preset, int(seed))  # TODO: add the other parameter values


def _run() -> None:
    dataset = make_dataset(preset, seed=int(seed))  # TODO: pass real params
    st.session_state[_k("snapshots")] = run(dataset)  # TODO: real call signature
    st.session_state[_k("step_idx")] = 0
    st.session_state[_k("playing")] = False


if (
    _k("snapshots") not in st.session_state
    or regenerate
    or st.session_state.get(_k("_param_key")) != _param_key
):
    _run()
    st.session_state[_k("_param_key")] = _param_key

snapshots = st.session_state[_k("snapshots")]
caption_slot.caption(f"TODO: summary line using {preset}, etc.")

with col_main:
    about_section(
        "TODO: one paragraph on why this algorithm matters.",
        ["TODO: reference 1", "TODO: reference 2"],
    )

    with st.container(border=True):
        m1, m2, m3, m4 = st.columns(4)
        # TODO: st.metric(...) x3-4 reflecting the current snapshot's meaningful numbers

    @st.fragment
    def _playback() -> None:
        n_steps = len(snapshots)
        step_idx = min(st.session_state.get(_k("step_idx"), 0), n_steps - 1)
        playing = st.session_state.get(_k("playing"), False)
        snap = snapshots[step_idx]

        with st.container(border=True):
            speed = st.select_slider(
                "Playback speed",
                options=["0.5×", "1×", "2×", "4×"],
                value="1×",
                label_visibility="collapsed",
                key=_k("speed"),
            )
            delay = {"0.5×": 0.6, "1×": 0.3, "2×": 0.15, "4×": 0.075}[speed]

            col_prev, col_play, col_pause, col_next, _col_spacer = st.columns(
                [1, 1.2, 1.2, 1, 3]
            )
            if col_prev.button("◀ Prev", use_container_width=True, key=_k("prev")):
                st.session_state[_k("step_idx")] = max(step_idx - 1, 0)
                st.session_state[_k("playing")] = False
                st.rerun(scope="fragment")
            if col_play.button("▶ Play", use_container_width=True, key=_k("play")):
                st.session_state[_k("playing")] = True
                st.rerun(scope="fragment")
            if col_pause.button("⏸ Pause", use_container_width=True, key=_k("pause")):
                st.session_state[_k("playing")] = False
                st.rerun(scope="fragment")
            if col_next.button("Next ▶", use_container_width=True, key=_k("next")):
                st.session_state[_k("step_idx")] = min(step_idx + 1, n_steps - 1)
                st.session_state[_k("playing")] = False
                st.rerun(scope="fragment")

            st.progress(
                step_idx / max(n_steps - 1, 1),
                text=f"Frame {step_idx + 1} / {n_steps} — {snap.title}",
            )

        fig = make_static_figure(snap)
        with st.container(border=True):
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
                key=_k("chart"),
            )

        # TODO: phase-specific st.info/st.success box, if the algorithm has phases

        with st.expander("📖 Reading the chart"):
            st.markdown("""TODO""")

        # Auto-advance — MUST be the last statement in this fragment.
        if playing:
            if step_idx < n_steps - 1:
                time.sleep(delay)
                st.session_state[_k("step_idx")] = step_idx + 1
                st.rerun(scope="fragment")
            else:
                st.session_state[_k("playing")] = False
                st.rerun(scope="fragment")

    _playback()
