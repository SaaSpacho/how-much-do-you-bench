# Billing FAQ

### Why does the Cursor export say `Included` in the cost column?

Because that request came out of the seat's monthly allowance rather than
usage-based pricing. There is no marginal charge for it. **`Included` is a cost
of 0.00** -- it is not missing data, and it is not something to skip the row
over: the tokens were still spent and still count toward the day's usage.

The same goes for a blank cost cell, which is what the export writes when a
request is refunded.

### Why is our invoice higher than the total in these exports?

Seat licences. The exports only cover usage.

### Can we get this per person?

Not from these files. Ask in #platform-tooling.

*Last reviewed 2026-04-18.*
