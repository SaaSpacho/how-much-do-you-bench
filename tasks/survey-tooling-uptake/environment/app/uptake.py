"""Count which tools organizations run in production.

`uptake(csv_path)` returns

    {"base": <number of respondents the count is over>,
     "counts": [(option_label, count), ...]}

with one entry per option of the tooling grid, sorted by count descending and
ties broken by option label A to Z. The numbers are the ones the research team
would publish.

`uptake` is graded on other exports in this format as well as on the one in
`/app`, so it has to read the file rather than return what you found in it.
"""
from __future__ import annotations


def uptake(csv_path) -> dict:
    raise NotImplementedError
