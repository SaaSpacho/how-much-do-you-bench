# Normalize token-usage exports

A few teammates exported their AI coding-tool usage in three different formats,
and I want them all in one shape so I can total them up.

`samples/` has one export from each tool: a Claude/Gemini-style JSON, a Cursor
CSV, and a CLI table.

`normalize_usage.py` has the function to implement and the exact record shape
it has to return.

How we read each vendor's columns, and what an internal usage report is
supposed to look like, is written down in the team wiki under `docs/` rather
than repeated here.
