---
name: airflow
description: >
  Write and debug Airflow DAGs, especially data-aware scheduling with
  Assets. Use whenever a task involves creating or editing an Airflow DAG
  file, wiring up `schedule=`/`outlets=`/`inlets=`, or a DAG fails to parse
  with a DagBag import error. Airflow 3 renamed `Dataset` to `Asset` and
  the DAG constructor now validates `schedule` strictly — passing anything
  but assets/asset references/asset aliases in a schedule list raises a
  `ValueError` at parse time that takes down every DAG in that file, not
  just the broken one.
metadata:
  type: workflow
---

# Airflow DAGs (3.x)

## `Dataset` is gone — it's `Asset` now

Airflow 3 renamed the data-aware scheduling primitive from `Dataset` to
`Asset`. The old names (`airflow.Dataset`, `airflow.datasets.Dataset`) are
either removed or a shim that no longer satisfies the type checks the DAG
constructor runs — so code that imports `Dataset` and passes it into
`schedule=`, `outlets=`, or `inlets=` fails at parse time, not at runtime.

```python
# wrong (Airflow 2.x API, removed/incompatible in 3.x)
from airflow.datasets import Dataset
with DAG("build_marts", schedule=[Dataset("s3://bucket/orders")]) as dag:
    ...

# right (Airflow 3.x)
from airflow.sdk import Asset
with DAG("build_marts", schedule=[Asset("s3://bucket/orders")]) as dag:
    ...
```

Same swap for task-level `outlets=`/`inlets=`:

```python
@task(outlets=[Asset("s3://bucket/orders")])
def ingest_orders(): ...
```

## `schedule` validation is strict

`DAG(schedule=...)` accepts exactly one of:

- `None`
- a cron string or `timedelta`
- a `Timetable` instance (e.g. `AssetOrTimeSchedule` to combine a time
  schedule with asset triggers)
- a list whose elements are **only** `Asset`, `Asset.ref(...)`
  (`AssetRef`), or `AssetAlias` instances

Mixing types, or putting a `Dataset`, string, or anything else into that
list, raises exactly this at import time:

```
ValueError: All elements in 'schedule' should be either assets, asset
references, or asset aliases
```

This is a DagBag-level failure: the whole file fails to import, so every
DAG defined in it disappears from the UI/scheduler, not just the one with
the bad `schedule=`.

## Before finishing: grep for the old API

If a task or CI check complains about "deprecated dataset API" (or
similarly), it's checking for leftover `Dataset` usage. Before considering
a DAG file done, check every DAG file you touched:

```bash
grep -rn "\bDataset\b\|from airflow\.datasets import" dags/
```

Any hit should become `Asset` from `airflow.sdk`, including in:
- `schedule=` on the `DAG(...)` constructor or `@dag` decorator
- `outlets=`/`inlets=` on tasks
- any helper that builds a list of datasets to schedule off of

## Gotchas

- **A DagBag import error kills the whole file, not just one DAG.** If a
  file defines multiple DAGs and one has a bad `schedule=`, none of them
  will show up — always re-parse the whole file after editing
  (`airflow dags list-import-errors` or just re-run the parse check) rather
  than assuming an unrelated DAG in the same file is unaffected.
- **`Asset` is identity-by-URI.** Two `Asset("s3://bucket/orders")`
  instances in different files refer to the same asset for scheduling
  purposes — no need to share a Python object, just match the URI string
  exactly (including scheme/trailing slash).
- **Don't reach for `AssetAlias`/`AssetRef` unless cross-DAG indirection is
  actually needed.** A single producer/consumer pair should just share the
  same `Asset(uri)` literal; aliases add a layer of indirection only worth
  it when multiple DAGs need to resolve to a producer decided elsewhere.
