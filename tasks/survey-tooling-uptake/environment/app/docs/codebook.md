# Codebook

## Structure of the export

Row 1 is the question code, row 2 is the question text as the respondent saw
it, and the data starts at row 3. Both header rows are part of the file.

`UID` identifies a respondent, `PID` the panel they came from,
`Respondent_Status` their disposition, and `StartDate` / `EndDate` bracket the
interview.

## Single-select questions

Stored as the answer text, not a code. `Q1` is revenue band and `Q4` is
industry.

## Multi-select grids

One column per option, suffixed `_1` ... `_n`. A cell holds the option text
when the respondent selected it and is empty when they did not. The option's
own label is the tail of the question text in row 2, after the last " - ".

Grids ending `_TEXT` hold free-text "other, please specify" answers and are not
options.

`Q7` is the tooling grid, 10 options.
