"""TODO: <Algorithm Name> — Plotly figure builders."""
from __future__ import annotations

import plotly.graph_objects as go

from common.theme import base_layout  # or base_layout_3d for a 3-D figure

# Redeclare the shared categorical palette locally (existing convention — see
# references/conventions.md for why this isn't just imported from common.theme).
_PALETTE = [
    "#6366f1", "#14b8a6", "#f59e0b", "#f43f5e", "#0ea5e9",
    "#8b5cf6", "#84cc16", "#fb923c", "#06b6d4", "#ec4899",
]


def make_static_figure(snapshot, **kwargs) -> go.Figure:
    """Renders exactly one Snapshot — what the app page calls on every playback step."""
    # TODO: build traces from `snapshot`'s fields
    fig = go.Figure()
    fig.update_layout(
        base_layout(
            None,  # title=None: the page's own progress bar already shows the frame label
            xaxis=dict(title="TODO"),
            yaxis=dict(title="TODO"),
        )
    )
    return fig


# TODO: add build_figure(snapshots, ...) for an animated multi-frame version ONLY if it
# adds real value beyond manual step-by-step playback (most existing pages don't use their
# animated variant from the app page at all — see references/conventions.md).
