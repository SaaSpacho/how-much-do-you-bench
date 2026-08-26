"""Compare two Harbor runs of the same benchmark, and chart them.

`compare(before_dir, after_dir)` returns

    {
        "exercises": [
            {"name": ..., "before": <float or None>, "after": <float or None>},
            ...                  # one per exercise, sorted by name
        ],
        "regressions": [...],    # exercise names that scored worse, sorted
        "fixed": [...],          # exercise names that scored better, sorted
        "n_exercises": ...,      # how many exercises the runs cover
    }

`plot_compare(summary, output_path)` saves a PNG at `output_path` charting the
two runs against each other, as `docs/charts.md` describes them.

`sample_jobs/` has a pair of runs to work against, and `docs/` is what we have
worked out about reading Harbor's output. Both functions are graded on other
runs as well as on that pair, so they have to read the directories rather than
return what you found in them.
"""
from __future__ import annotations


def compare(before_dir, after_dir) -> dict:
    raise NotImplementedError


def plot_compare(summary, output_path) -> None:
    raise NotImplementedError
