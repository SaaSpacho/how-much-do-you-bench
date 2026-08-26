---
name: docs
description: >
  Read and apply the documentation in an app's docs/ folder (typically
  app/docs) before analyzing its data or working in its codebase. Use
  whenever a task involves a directory containing documentation
  markdown files describing a dataset, export, or system — README,
  methodology, data_quality, codebook, schema, FAQ, or similar. These
  docs typically hide the rules that make a number right or wrong:
  exclusions, cutoffs, definitions, and scope limits that are not visible
  in the raw data or code itself. Skipping even one file risks reporting
  a figure that silently contradicts the documented rules.
metadata:
  type: workflow
---

# Reading app docs

Documentation folders like `app/docs` are written piecemeal — "written when
someone asks and are not always tidied afterwards" is a typical disclaimer —
so the rules that matter can be in any file, including ones whose name looks
irrelevant to the task at hand. Treat every file as a candidate for a rule
that changes the answer.

## Procedure

1. **List every file in the docs directory before reading any of them.**
   Use the README or index file (if present) as a map, but don't stop
   there — it may not mention every file, and it may be stale.
2. **Read every file in full, not just the ones the README points at.**
   A short, oddly-named, or seemingly tangential file is exactly where an
   exclusion or edge case tends to live. Do not sample, skim headings only,
   or stop once you've found "enough."
3. **Extract rules that are invisible in the raw data/code**, typically:
   - **Exclusions** — rows, IDs, panels, time ranges, or entities to drop
     before computing anything (e.g. a pilot cohort, a disabled feature
     flag, a known-bad data source).
   - **Cutoffs / thresholds** — numeric definitions of a category (e.g.
     "under N minutes is a speeder", "more than X retries counts as
     failed").
   - **Encoding conventions** — how the raw format maps to meaning (column
     naming schemes, sentinel values, status codes, units).
   - **Scope limits** — a rule, weighting scheme, or transformation that
     applies to *only* one part of the system and must not leak elsewhere.
   - **Explicit non-behaviors** — what the docs say is deliberately *not*
     done (no imputation, no dedup, no retries), which rules out a
     "obvious" fix that would actually contradict policy.
4. **Reconcile conflicts and precedence.** If two files touch the same
   topic, prefer the more specific file over the README, and flag the
   conflict to the user rather than silently picking one.
5. **Carry the rules forward as constraints, not trivia.** Before producing
   any figure, query, or change, check it against every rule extracted in
   step 3 — most of them are the kind of thing that makes a result fail to
   reconcile with previously reported numbers if missed, without raising
   an error.

## Gotchas

- **A file being short is not a signal it's low-value.** Some of the
  highest-impact rules (a single exclusion, a single cutoff) fit in one
  paragraph.
- **Don't infer a rule's absence from silence in the code.** Docs commonly
  describe rules that the underlying data/export does not encode at all
  (e.g. a derived cutoff computed from two raw columns, or an exclusion
  that must be applied by ID because there's no flag for it).
- **Re-check the docs directory if it's referenced again later in a long
  task.** Long sessions can drift into treating remembered summaries as
  ground truth; re-reading is cheap compared to a wrong figure.
