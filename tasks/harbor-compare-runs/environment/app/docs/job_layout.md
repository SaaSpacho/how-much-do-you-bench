# Job directory layout

A job directory holds one sub-directory per rollout, plus a `result.json` that
Harbor writes at the end.

A rollout directory is named `<language>__<exercise>__<suffix>`, where the
suffix is random per rollout. `python__bowling__99zzyy` is the `bowling`
exercise; the suffix carries no meaning and is not part of the exercise name.
The same exercise gets a different suffix in every run, so two runs are lined
up on the exercise name and never on the directory name.

Inside, `verifier/reward.txt` is the grade. Any file in a rollout can be
missing: the rollout may have died before writing it.

## What is not an exercise

Two things in a job directory are not rollouts and do not belong in a summary:

* anything that is not a directory -- `result.json`, `job.log`, `lock.json`;
* directories that do not follow the `<language>__<exercise>__<suffix>`
  pattern, which the runner uses for its own scratch space.

## Smoke rollouts

Our CI launches a canary rollout with every job to check the harness is alive.
It is named for the exercise `smoke` -- `python__smoke__<suffix>` -- and it is
not part of the benchmark. It always passes, and counting it inflates both the
exercise count and the success rate.

It is in the job directory because Harbor put it there. Skip it.
