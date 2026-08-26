# Charts

Charts go straight into the report, so they are saved as PNG and nothing else.

A comparison chart shows both runs per exercise: one bar for before and one
for after, side by side, with the exercise names along the x axis.

Exercises with no result in one of the runs are not charted. There is nothing
to draw for them and a gap in the axis prompts the same question every time.

## Headless

These run on a build agent with no display. matplotlib picks an interactive
backend when it can find one and fails when it cannot, so the report scripts
select the Agg backend before importing pyplot.
