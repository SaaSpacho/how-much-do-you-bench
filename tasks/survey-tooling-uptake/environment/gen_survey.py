"""Generate a Qualtrics-shaped export for the sample survey task.

Two header rows, a multi-select grid, an "other, please specify" free-text
column, and the panel/timing quirks the docs describe. Deterministic given the
seed, so the grader can make a second export the answer cannot be memorised on.

Usage: python gen_survey.py <seed> <out.csv>
"""
import csv
import sys
from datetime import datetime, timedelta
from random import Random

OPTIONS = [
    "Cloud data warehouse",
    "Data lakehouse",
    "Orchestration (Airflow or similar)",
    "Transformation tool (dbt or similar)",
    "Streaming platform",
    "Data catalog",
    "Data quality monitoring",
    "Reverse ETL",
    "Feature store",
    "Other (please specify)",
]
# Chance each option is selected, before the whole-grid effects below.
RATES = [0.72, 0.41, 0.55, 0.48, 0.27, 0.31, 0.36, 0.14, 0.11, 0.08]

REVENUE = ["EUR 1-10M", "EUR 10-50M", "EUR 50-250M", "More than EUR 250M"]
INDUSTRY = ["Manufacturing", "Retail", "Financial services", "Public sector",
            "Life Sciences", "Electric Power"]
OTHER_TEXT = ["homegrown scheduler", "spreadsheets, honestly", "SAP BW",
              "in-house metadata service"]

Q7_TEXT = "Which of the following are in production in your organization today?"
FIELDWORK_OPEN = datetime(2025, 2, 4, 9, 0)


def rows(seed: int, n: int = 500):
    rng = Random(seed)
    for i in range(n):
        pid = 4 if i < n // 8 else rng.choice([1, 1, 1, 2, 3])
        start = FIELDWORK_OPEN + timedelta(
            days=rng.randrange(0 if pid == 4 else 7, 17), minutes=rng.randrange(0, 600)
        )
        if pid == 4:
            start -= timedelta(days=14)
        minutes = rng.randrange(4, 10) if rng.random() < 0.15 else rng.randrange(10, 41)

        picks = [rng.random() < r for r in RATES]
        if rng.random() < 0.03:
            picks = [True] * len(OPTIONS)
        elif not any(picks):
            picks[0] = True

        grid = [opt if p else "" for opt, p in zip(OPTIONS, picks)]
        yield [
            start.strftime("%-m/%-d/%y %H:%M"),
            (start + timedelta(minutes=minutes)).strftime("%-m/%-d/%y %H:%M"),
            f"R{seed}{i:04d}",
            str(pid),
            "Complete",
            rng.choice(REVENUE),
            rng.choice(INDUSTRY),
            *grid,
            rng.choice(OTHER_TEXT) if picks[-1] else "",
        ]


def write(seed: int, path: str) -> None:
    codes = ["StartDate", "EndDate", "UID", "PID", "Respondent_Status", "Q1", "Q4"]
    codes += [f"Q7_{i}" for i in range(1, len(OPTIONS) + 1)] + ["Q7_10_TEXT"]
    labels = ["Start Date", "End Date", "Respondent ID", "Panel ID",
              "Respondent Status",
              "What was your organization's annual revenue in the last fiscal year?",
              "In which industry does your organization operate?"]
    labels += [f"{Q7_TEXT} - {opt}" for opt in OPTIONS]
    labels += [f"{Q7_TEXT} - Other (please specify) - Text"]

    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(codes)
        w.writerow(labels)
        w.writerows(rows(seed))


if __name__ == "__main__":
    write(int(sys.argv[1]), sys.argv[2])
