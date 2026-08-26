# Data quality

Panel data is bought, and some of what arrives is not worth analysing. Two
checks are run on every wave before anyone reports a number, and both remove
respondents rather than flagging them.

## Speeders

Median completion for this instrument is around eighteen minutes and the
questionnaire cannot be answered honestly in much less. Anyone who finished in
**under ten minutes** is treated as a speeder and dropped.

There is no duration column in the export: it is `EndDate` minus `StartDate`.
Both are in the panel provider's format, `M/D/YY HH:MM`, and are minute
resolution, so the difference is whole minutes.

## Straight-lining

A respondent who ticks every option in a multi-select grid has told you nothing
about which of them matter. Where the grid offers 10 options and someone
selects all 10, the response is dropped rather than partially used.

Selecting most options is fine and is not straight-lining; the check is for
selecting all of them.

## What we do not do

We do not impute missing answers, and we do not drop a respondent for leaving a
single question blank.
