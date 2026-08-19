"""TODO: <Algorithm Name> — synthetic dataset / environment generators."""
from __future__ import annotations

import numpy as np

# TODO: named presets — existing algorithms use 3-6. Keys are internal identifiers,
# names are what the selectbox displays.
PRESET_KEYS: list[str] = ["TODO"]
PRESET_NAMES: dict[str, str] = {"TODO": "TODO Display Name"}


def make_TODO_preset(*, seed: int = 0) -> object:
    """TODO: one generator function per preset, or one parameterized generator —
    match whichever existing algorithms in the same category use.

    Point-cloud algorithms (see dbscan): return (X: np.ndarray[N, dims], labels).
    Environment/graph algorithms (see qlearning's GridWorld): return a small
    dataclass describing the environment.
    """
    rng = np.random.default_rng(seed)
    raise NotImplementedError


def make_dataset(preset: str, *, seed: int = 0, **kwargs) -> object:
    """Dispatcher — the app page calls this, not the individual generators directly."""
    # TODO: dispatch to the right make_*_preset function
    raise NotImplementedError
