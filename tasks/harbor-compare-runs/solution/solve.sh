#!/bin/bash
# Line the runs up on the exercise name, because the suffix changes every run.
# Skip what is not a rollout and skip the canary. A rollout that wrote no
# reward.txt has no result: it is None, it is not a zero, and it cannot be a
# regression. Agg before pyplot, because there is no display here.
set -euo pipefail

cat > /app/compare_runs.py <<'PY'
"""Compare two Harbor runs of the same benchmark, and chart them."""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROLLOUT = re.compile(r"^[^_]+__(.+)__[^_]+$")
SKIP = {"smoke"}


def _rewards(run_dir) -> dict:
    out = {}
    for d in Path(run_dir).iterdir():
        if not d.is_dir():
            continue
        m = ROLLOUT.match(d.name)
        if not m or m.group(1) in SKIP:
            continue
        reward = d / "verifier" / "reward.txt"
        out[m.group(1)] = float(reward.read_text()) if reward.exists() else None
    return out


def compare(before_dir, after_dir) -> dict:
    before, after = _rewards(before_dir), _rewards(after_dir)
    names = sorted(set(before) | set(after))
    both = [n for n in names
            if before.get(n) is not None and after.get(n) is not None]
    return {
        "exercises": [
            {"name": n, "before": before.get(n), "after": after.get(n)}
            for n in names
        ],
        "regressions": sorted(n for n in both if after[n] < before[n]),
        "fixed": sorted(n for n in both if after[n] > before[n]),
        "n_exercises": len(names),
    }


def plot_compare(summary, output_path) -> None:
    charted = [e for e in summary["exercises"]
               if e["before"] is not None and e["after"] is not None]
    names = [e["name"] for e in charted]
    x = range(len(charted))
    width = 0.4

    fig, ax = plt.subplots(figsize=(max(6, len(charted)), 4))
    ax.bar([i - width / 2 for i in x], [e["before"] for e in charted],
           width, label="before")
    ax.bar([i + width / 2 for i in x], [e["after"] for e in charted],
           width, label="after")
    ax.set_xticks(list(x))
    ax.set_xticklabels(names, rotation=45, ha="right")
    ax.set_ylabel("reward")
    ax.set_title("Before and after, by exercise")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
PY
