"""Grade uptake() against expected counts computed here, independently.

Two exports are checked: the one shipped in /app, and one generated at grade
time from a different seed, so an answer that returns what it read in the file
it was given fails.
"""
import csv
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, "/app")

FMT = "%m/%d/%y %H:%M"
PILOT = "4"
SPEEDER_MINUTES = 10


def expected(path: str) -> dict:
    with open(path, newline="") as fh:
        codes, labels, *data = list(csv.reader(fh))
    grid = [
        i
        for i, c in enumerate(codes)
        if c.startswith("Q7_") and not c.endswith("_TEXT")
    ]
    options = [labels[i].rsplit(" - ", 1)[1] for i in grid]
    counts = dict.fromkeys(options, 0)
    base = 0

    for row in data:
        rec = dict(zip(codes, row))
        if rec["PID"] == PILOT:
            continue
        minutes = (
            datetime.strptime(rec["EndDate"], FMT)
            - datetime.strptime(rec["StartDate"], FMT)
        ).total_seconds() / 60
        if minutes < SPEEDER_MINUTES:
            continue
        picked = [row[i] for i in grid if row[i].strip()]
        if len(picked) == len(grid):
            continue
        base += 1
        for opt in picked:
            counts[opt] += 1

    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return {"base": base, "counts": ranked}


def compare(label: str, path: str) -> bool:
    from uptake import uptake

    want = expected(path)
    try:
        got = uptake(path)
    except Exception as exc:  # noqa: BLE001 - report, do not crash the grader
        print(f"FAIL {label}: uptake() raised {exc!r}")
        return False

    ok = True
    if not isinstance(got, dict):
        print(f"FAIL {label}: expected a dict, got {type(got).__name__}")
        return False
    if got.get("base") != want["base"]:
        print(f"FAIL {label}: base is {got.get('base')}, expected {want['base']}")
        ok = False

    counts = [tuple(c) for c in got.get("counts", [])]
    if counts != want["counts"]:
        print(f"FAIL {label}: counts do not match")
        print(f"  expected {want['counts']}")
        print(f"  got      {counts}")
        ok = False
    if ok:
        print(f"PASS {label}: base {want['base']}, {len(want['counts'])} options")
    return ok


if __name__ == "__main__":
    results = [compare("shipped export", "/app/quant_tooling.csv")]
    with tempfile.TemporaryDirectory() as tmp:
        heldout = str(Path(tmp) / "quant_heldout.csv")
        subprocess.run(
            [sys.executable, "/opt/gen_survey.py", "907", heldout], check=True
        )
        results.append(compare("held-out export", heldout))
    sys.exit(0 if all(results) else 1)
