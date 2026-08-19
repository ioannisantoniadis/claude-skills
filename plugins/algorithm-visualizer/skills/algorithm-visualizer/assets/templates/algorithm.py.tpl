"""TODO: <Algorithm Name> — from-scratch NumPy implementation.

TODO: one-paragraph docstring explaining what this algorithm does and, if the
Snapshot design is sparse/event-based rather than dense/per-step, WHY — see
references/snapshot-patterns.md for the two precedents this choice is based on.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np


@dataclass
class Snapshot:
    """TODO: one field per piece of state needed to redraw the chart at this instant.

    Every existing algorithm's Snapshot includes:
    - a `phase: Literal[...]` field if the algorithm has discrete phases
    - full copies (not views) of any mutable array — snapshots must be independent
    - a `title` property below, building the human-readable per-frame caption
    """

    # TODO: state fields
    phase: Literal["TODO"]  # TODO: real phase names, or delete if no discrete phases

    @property
    def title(self) -> str:
        """Human-readable caption for this frame — feeds the playback progress bar."""
        # TODO
        raise NotImplementedError


def run(
    # TODO: real parameters
    seed: int = 0,
) -> list[Snapshot]:
    """Run the algorithm, returning one Snapshot per step (sparse or dense — see
    references/snapshot-patterns.md for which shape fits this algorithm).
    """
    rng = np.random.default_rng(seed)
    snapshots: list[Snapshot] = []

    # TODO: the actual from-scratch algorithm loop.
    # Append a Snapshot at each meaningful step/event. Use .copy() on any mutable
    # array stored in the snapshot.

    return snapshots


# TODO: before wiring this into apps/<algo>.py, verify correctness — a finite-difference
# gradient check, a closed-form comparison, or a reference implementation's output on a
# small fixed input. Delete this comment once actually verified, not just written.
