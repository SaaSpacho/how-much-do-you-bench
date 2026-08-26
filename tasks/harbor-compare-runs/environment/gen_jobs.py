"""Generate a pair of Harbor job directories for the sample task.

Real shape, small: one directory per rollout named
`<language>__<exercise>__<suffix>`, `verifier/reward.txt` inside, plus the
things a job directory carries that are not rollouts. Deterministic given the
seed, so the grader can build a second pair the answer cannot be memorised on.

Usage: python gen_jobs.py <seed> <out_dir>
"""
import json
import shutil
import sys
from pathlib import Path
from random import Random

EXERCISES = [
    "affine-cipher", "book-store", "bowling", "forth", "matrix",
    "pov", "rest-api", "zebra-puzzle",
]
SUFFIX = "abcdefghijklmnopqrstuvwxyz0123456789"


def rollout(root: Path, name: str, rng: Random, reward, missing=False) -> None:
    suffix = "".join(rng.choice(SUFFIX) for _ in range(6))
    d = root / f"python__{name}__{suffix}"
    (d / "verifier").mkdir(parents=True)
    (d / "attempt.json").write_text(json.dumps({"attempt": 1}) + "\n")
    if not missing:
        (d / "verifier" / "reward.txt").write_text(f"{reward}\n")


def write(seed: int, out: str) -> None:
    rng = Random(seed)
    root = Path(out)
    if root.exists():
        shutil.rmtree(root)

    # Which exercises each run passes. A few move in each direction, and one
    # rollout in the second run dies before writing its reward.
    before = {ex: (1.0 if rng.random() < 0.5 else 0.0) for ex in EXERCISES}
    after = dict(before)
    for ex in rng.sample(EXERCISES, 3):
        after[ex] = 0.0 if before[ex] else 1.0
    died = rng.choice(EXERCISES)

    for run, rewards in (("before", before), ("after", after)):
        d = root / run
        d.mkdir(parents=True)
        for ex, reward in rewards.items():
            rollout(d, ex, rng, reward, missing=(run == "after" and ex == died))
        # A canary rollout, which is not part of the benchmark.
        rollout(d, "smoke", rng, 1.0)
        # Things in a job directory that are not rollouts.
        (d / "result.json").write_text(json.dumps({"job": run}) + "\n")
        (d / "job.log").write_text("started\nfinished\n")
        (d / "_runner_tmp").mkdir()
        (d / "_runner_tmp" / "notes.txt").write_text("scratch\n")


if __name__ == "__main__":
    write(int(sys.argv[1]), sys.argv[2])
