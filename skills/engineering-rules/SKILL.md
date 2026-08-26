---
name: engineering-rules
description: >
  Universal engineering discipline for every task, in every language: read
  the project's documentation before touching code, verify changes by
  actually running checks rather than reasoning about them, cap iteration
  on a failing fix, preserve existing interfaces exactly, and match
  surrounding code style. Apply this at the start of every task and again
  right before declaring it done — it does not depend on the task's domain
  or language.
metadata:
  type: workflow
---

# Engineering rules

Apply these to every task, regardless of language or problem.

## Read the docs first

Before tackling ANY task, use the `docs` skill to read ALL the
documentation in the project's docs folder. The rules that decide whether
an answer is right often live there, not in the code.

## Verify before finishing

Never declare done from reasoning alone — write a script covering normal
cases, boundaries, and error paths, run it, and compare actual vs. expected
output. A test run reporting zero collected/executed tests is a failure
signal, not success; if no suite exists, write checks from the task's own
examples.

## Iteration budget: 3 runs max

Run your checks at most 3 times total for the whole task. If still failing
after the 3rd, stop: apply your best correction, note what's still wrong,
and finish. Don't keep re-editing the same file past 3 attempts hoping it
works.

## Preserve the interface

Keep names, signatures, parameter names, defaults, imports, and return
types exactly as given. Match specified output text, error messages, and
formats exactly.

## Code quality

Match the surrounding style over cleverness. Raise specific exceptions
rather than swallowing errors. Clean up scratch files before finishing.
