#!/bin/bash
# The four rules that are in docs/ and not in the data: panel 4 is the pilot and
# is out of every published figure, anyone under ten minutes is a speeder, a
# respondent who ticked all ten options is straight-lining, and _TEXT is a
# free-text answer rather than an option. Counts are unweighted, so the base is
# just how many respondents survived those cuts.
set -euo pipefail

cat > /app/uptake.py <<'PY'
"""Count which tools organizations run in production."""
from __future__ import annotations

import csv
from datetime import datetime

FMT = "%m/%d/%y %H:%M"


def uptake(csv_path) -> dict:
    with open(csv_path, newline="") as fh:
        codes, labels, *data = list(csv.reader(fh))

    grid = [i for i, c in enumerate(codes)
            if c.startswith("Q7_") and not c.endswith("_TEXT")]
    counts = {labels[i].rsplit(" - ", 1)[1]: 0 for i in grid}
    base = 0

    for row in data:
        rec = dict(zip(codes, row))
        if rec["PID"] == "4":
            continue
        minutes = (datetime.strptime(rec["EndDate"], FMT)
                   - datetime.strptime(rec["StartDate"], FMT)).total_seconds() / 60
        if minutes < 10:
            continue
        picked = [row[i] for i in grid if row[i].strip()]
        if len(picked) == len(grid):
            continue
        base += 1
        for option in picked:
            counts[option] += 1

    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return {"base": base, "counts": ranked}
PY
