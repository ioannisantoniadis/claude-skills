# Snapshot Pattern Reference

Two real, meaningfully different precedents for how `Snapshot` is shaped, to calibrate the
design decision in Step 2. Use these as evidence, not as the only two valid shapes — the
right shape follows from what the algorithm actually does.

## Sparse / event-based: `dbscan` (clustering)

```python
@dataclass
class Snapshot:
    points: np.ndarray
    labels: np.ndarray          # -2 unvisited, -1 noise, 0..K cluster id
    roles: np.ndarray           # UNVISITED / CORE / BORDER / NOISE
    active_point: int | None
    neighbors: np.ndarray | None
    eps: float
    phase: Literal["init", "examine", "expand", "done"]
    cluster_id: int
    @property
    def n_clusters(self) -> int: ...
    @property
    def title(self) -> str: ...
```

Snapshots are appended only at meaningful *events* inside the scan/BFS loop — right after
finding a core point (`phase="examine"`), right after BFS finishes expanding a cluster
(`phase="expand"`) — not once per point. Total count: roughly 6-20 for a typical run. This
is a deliberate choice (documented in the module docstring): one-snapshot-per-point would
be too fine-grained to be a meaningful "step" for a learner to reason about.

**Use this shape when**: the algorithm has discrete phases or makes discrete decisions
(cluster assignment, tree/graph construction, combinatorial search) where each "step" is
naturally an event, not a uniform iteration.

## Dense / per-step: `qlearning` (reinforcement learning)

```python
@dataclass
class Snapshot:
    grid: GridWorld                 # constant across snapshots
    algorithm: Literal["qlearning", "sarsa"]
    episode: int
    step_in_episode: int
    global_step: int
    phase: Literal["init", "explore", "exploit"]
    state: Cell | None
    action: int | None
    actual_action: int | None
    next_state: Cell | None
    reward: float | None
    done: bool
    epsilon: float
    q_table: np.ndarray             # (rows, cols, 4) COPY after this step's update
    td_error: float | None
    episode_return: float = 0.0
    episode_length: int = 0
    @property
    def slipped(self) -> bool: ...
    @property
    def title(self) -> str: ...
```

One `Snapshot` per environment step, appended inside
`for ep in range(1, n_episodes+1): for t in range(1, max_steps+1): ...` — right after the
Q-table update. This produces hundreds to thousands of frames for a realistic run.
`qlearning/visualize.py` compensates with `MAX_ANIMATED_FRAMES = 200` subsampling for the
*animated* figure variant (the manual-playback app page doesn't need this — it only
renders the current frame, not all of them at once).

**Use this shape when**: the algorithm is a numerical optimization loop or RL training
process where every iteration is comparably meaningful and there's no natural "event" to
single out.

## What's common to both

- A `phase: Literal[...]` field whenever the algorithm has any notion of discrete stages.
- A `title` `@property` building the human-readable per-frame caption — this feeds the
  playback progress bar's text, not a chart title (chart title is `None`, see
  `references/conventions.md`).
- Full copies (`.copy()`/`deepcopy`) of any mutable array/object stored in the snapshot, so
  each frame is independent and safe to scrub backward/forward through.

## Data shape follows the same split

`dbscan/data.py` generates point clouds: `(X: np.ndarray[N,2], true_labels: np.ndarray[N])`
from 6 named synthetic shape generators, normalized to a fixed range, dispatched through
`make_dataset(shape, n_points, n_clusters, seed)`.

`qlearning/data.py` generates an environment, not points: a `GridWorld` `@dataclass`
(`kind`, `reward`, `terminal`, `respawn` arrays, `start`, `rows`, `cols`, `name`), with
named presets (`make_classic()`, `make_cliff(...)`, `make_random_hazards(...)`) dispatched
through `make_grid(preset, rows, cols, seed)`.

Match whichever shape fits the new algorithm's actual input — point-cloud algorithms want
the `dbscan` shape, environment/graph/sequential algorithms want something closer to the
`qlearning` shape.
