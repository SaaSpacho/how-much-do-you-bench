# Export column reference

## Claude / Gemini JSON (`daily[]`)

| Field                  | Meaning                                              |
| ---------------------- | ---------------------------------------------------- |
| `period`               | The usage day, already `YYYY-MM-DD`.                  |
| `inputTokens`          | Prompt tokens, cache reads excluded.                  |
| `outputTokens`         | Completion tokens.                                    |
| `cacheReadTokens`      | Tokens served from an existing prompt cache.          |
| `cacheCreationTokens`  | Tokens written *into* the cache. See below.           |
| `totalCost`            | Already in USD.                                       |
| `modelsUsed`           | Informational. We do not break spend down by model.   |

**Cache creation is not one of our reported figures.** It is priced
differently per vendor and only one of the three exports reports it at all, so
a number that included it would not be comparable across teams. Carry input,
output and cache *read*; drop cache creation.

## Cursor CSV

Cursor ships two input columns and they are not interchangeable:

- `Input (w/ Cache Write)` -- prompt tokens *plus* the tokens written into the
  cache on that request.
- `Input (w/o Cache Write)` -- prompt tokens only.

Use `Input (w/o Cache Write)`. The other one double-counts cache creation, which
per the rule above we do not report. This trips up everyone who writes the
importer from the column order rather than the header.

`Date` is a full ISO timestamp, not a date. One row is one request, not one day.

## CLI table

A box-drawing table pasted out of a terminal, `│`-delimited. Columns in order:
Date, Agent, Models, Input, Output, Cache Create, Cache Read, Total Tokens,
Cost (USD). Counts carry thousands separators and the cost cell carries a `$`.

*Last reviewed 2026-05-02.*
