"""Grade compare() and plot_compare().

The numbers are graded exactly, against expectations computed here from the
job directories rather than read from the submission. The chart is graded on
what can be checked without guessing at a design: a real PNG, big enough to
read, and not a blank canvas. Two pairs of runs are used, the one shipped in
/app and one generated at grade time from a different seed.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, "/app")

ROLLOUT = re.compile(r"^[^_]+__(.+)__[^_]+$")
SKIP = {"smoke"}


def rewards(run_dir: Path) -> dict:
    """Exercise name -> reward, for the rollouts that recorded one."""
    out = {}
    for d in run_dir.iterdir():
        if not d.is_dir():
            continue
        m = ROLLOUT.match(d.name)
        if not m or m.group(1) in SKIP:
            continue
        reward = d / "verifier" / "reward.txt"
        out[m.group(1)] = float(reward.read_text()) if reward.exists() else None
    return out


def expected(before: Path, after: Path) -> dict:
    b, a = rewards(before), rewards(after)
    names = sorted(set(b) | set(a))
    both = [n for n in names if b.get(n) is not None and a.get(n) is not None]
    return {
        "exercises": [
            {"name": n, "before": b.get(n), "after": a.get(n)} for n in names
        ],
        "regressions": sorted(n for n in both if a[n] < b[n]),
        "fixed": sorted(n for n in both if a[n] > b[n]),
        "n_exercises": len(names),
    }


def check_numbers(label: str, jobs: Path) -> dict | None:
    from compare_runs import compare

    want = expected(jobs / "before", jobs / "after")
    try:
        got = compare(str(jobs / "before"), str(jobs / "after"))
    except Exception as exc:  # noqa: BLE001 - report, do not crash the grader
        print(f"FAIL {label}: compare() raised {exc!r}")
        return None
    if not isinstance(got, dict):
        print(f"FAIL {label}: compare() returned {type(got).__name__}, expected a dict")
        return None

    ok = True
    for key in ("n_exercises", "regressions", "fixed"):
        mine = got.get(key)
        if isinstance(mine, (list, tuple)):
            mine = list(mine)
        if mine != want[key]:
            print(f"FAIL {label}: {key} is {mine!r}, expected {want[key]!r}")
            ok = False

    rows = [dict(e) for e in got.get("exercises", []) if isinstance(e, dict)]
    trimmed = [{k: e.get(k) for k in ("name", "before", "after")} for e in rows]
    if trimmed != want["exercises"]:
        print(f"FAIL {label}: exercises do not match")
        print(f"  expected {want['exercises']}")
        print(f"  got      {trimmed}")
        ok = False

    if ok:
        print(f"PASS {label}: {want['n_exercises']} exercises, "
              f"{len(want['regressions'])} regressions, {len(want['fixed'])} fixed")
    return got if ok else None


def check_plot(label: str, summary: dict, out: Path) -> bool:
    from compare_runs import plot_compare

    try:
        plot_compare(summary, str(out))
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL {label}: plot_compare() raised {exc!r}")
        return False
    if not out.exists():
        print(f"FAIL {label}: no file at {out}")
        return False
    if out.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
        print(f"FAIL {label}: {out.name} is not a PNG")
        return False

    img = mpimg.imread(str(out))
    if min(img.shape[:2]) < 200:
        print(f"FAIL {label}: {img.shape[1]}x{img.shape[0]} is too small to read")
        return False
    # A chart has ink on it. A blank canvas is one colour, and an axes frame
    # with no bars is only a few more.
    if len(np.unique(img.reshape(-1, img.shape[2]), axis=0)) < 20:
        print(f"FAIL {label}: the chart is blank")
        return False
    print(f"PASS {label}: {img.shape[1]}x{img.shape[0]} PNG")
    return True


def grade(label: str, jobs: Path, out: Path) -> bool:
    summary = check_numbers(label, jobs)
    if summary is None:
        return False
    return check_plot(f"{label} chart", summary, out)


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        results = [grade("shipped runs", Path("/app/sample_jobs"), tmp / "a.png")]
        heldout = tmp / "heldout"
        subprocess.run(
            [sys.executable, "/opt/gen_jobs.py", "907", str(heldout)], check=True
        )
        results.append(grade("held-out runs", heldout, tmp / "b.png"))
    sys.exit(0 if all(results) else 1)
