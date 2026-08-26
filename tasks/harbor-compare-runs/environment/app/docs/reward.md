# Reward

`verifier/reward.txt` holds one number: what the rollout scored. These runs are
pass or fail, so it is `1` or `0`, sometimes written as `1.0`. Read it as a
float and compare numerically.

## A missing reward is not a zero

A rollout whose verifier never ran writes no `reward.txt`. That is a rollout we
have no result for, and it is not the same thing as a rollout that scored 0.

Reporting it as a zero turns an infrastructure failure into a regression, which
is how we spent an afternoon looking for a bug in an exercise that was never
graded. Where a run has no result for an exercise, say so rather than picking a
number for it, and leave that exercise out of the regression and fixed lists --
there is nothing to compare it against.
