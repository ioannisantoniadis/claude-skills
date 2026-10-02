#!/usr/bin/env python3
"""Compare regenerated figures in a git checkout against the committed versions.

Usage (inside the scratch clone, after running the figure scripts):
    python compare_figures.py <clone> [--threshold 0.05]

For every image git reports as modified, prints its size before and after and the share of
pixels that changed by more than the threshold (when sizes match). Needs numpy and matplotlib,
which any figure environment has, so run it with that environment's Python.

Read the output as a triage list, not a verdict. Tight-bbox shifts of a pixel or two, and font
or library-version differences, change bytes but not content. Look at any image whose changed
share is large, or whose size changed by more than a few pixels, before calling it a finding.
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

import matplotlib.image as mpimg
import numpy as np

RASTER = {".png", ".jpg", ".jpeg"}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("clone")
    ap.add_argument("--threshold", type=float, default=0.05)
    args = ap.parse_args()
    root = Path(args.clone).resolve()
    changed = subprocess.run(["git", "-C", root, "diff", "--name-only"], capture_output=True,
                             text=True, check=True).stdout.split()
    images = [c for c in changed if Path(c).suffix.lower() in RASTER]
    if not images:
        print("No committed raster images changed: regenerated figures are byte-identical.")
        return
    print("| Image | Committed size | Regenerated size | Changed pixels |\n|---|---|---|---|")
    with tempfile.TemporaryDirectory() as tmp:
        for rel in sorted(images):
            old = Path(tmp) / Path(rel).name
            old.write_bytes(subprocess.run(["git", "-C", root, "show", f"HEAD:{rel}"],
                                           capture_output=True, check=True).stdout)
            a, b = mpimg.imread(root / rel), mpimg.imread(old)
            size = lambda x: f"{x.shape[1]}×{x.shape[0]}"  # noqa: E731
            if a.shape != b.shape:
                note = "size differs: look at both"
            else:
                d = np.abs(a[..., :3].astype(float) - b[..., :3].astype(float)).max(-1)
                note = f"{(d > args.threshold).mean() * 100:.2f}%"
            print(f"| `{rel}` | {size(b)} | {size(a)} | {note} |")
    print("\nRestore the committed images afterwards: git checkout -- <paths>", file=sys.stderr)


if __name__ == "__main__":
    main()
