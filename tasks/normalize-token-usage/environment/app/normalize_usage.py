"""Normalize heterogeneous token-usage exports into one schema.

`normalize_usage(path)` detects the format from the file, parses it, and
returns one record per day, sorted by date:

    {
        "date": "YYYY-MM-DD",
        "input_tokens": ...,
        "output_tokens": ...,
        "cache_read_tokens": ...,
        "cost_usd": ...,
        "source": ...,            # "claude-json" | "cursor-csv" | "cli-table"
    }

The wiki under `docs/` covers what each vendor's columns mean and the shape an
internal usage report takes.
"""
from __future__ import annotations

from pathlib import Path


def normalize_usage(path) -> list[dict]:
    raise NotImplementedError
