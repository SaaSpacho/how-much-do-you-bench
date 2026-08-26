# Internal usage reporting conventions

Every usage report we publish, whatever the source, is **one record per
calendar day, ascending by date**.

Vendors disagree about granularity: the JSON export is already daily, the CLI
table is already daily, and the Cursor CSV is one row per request with a
timestamp. Where a source reports several rows for one day, total them into
that day's single record -- sum the token counts and sum the cost. Where a
source reports a timestamp, the day is the date part of it, as exported. We do
not convert timezones; every vendor exports in UTC and so do we.

Days with no usage are simply absent. Do not pad the range.

*Last reviewed 2026-05-02.*
