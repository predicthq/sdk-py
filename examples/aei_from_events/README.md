# Aggregate Event Impact (AEI) from Events

Event data queried from our events endpoint comes in the following form: one row corresponds to a single event. However, in the context of building forecasting models, the most natural way to incorporate information about events is to (first) include data about estimated attendance.

The set of functions simplify the transformation of record level event data into features aggregated by event category.

## Grouping Categories

For an overview of how different types of events are classified, see our [page](https://www.predicthq.com/intelligence/data-enrichment/event-categories) about how we categorize!

## Calculating Impact vs. Summing PHQ Attendance

[`phq_attendance`](https://support.predicthq.com/what-is-phq-attendance) is the _overall_ estimated attendance for an event. So now matter if an event with a `phq_attendance` of 10,000 takes place over the course of 1 day or 1 month, the event will show the same value in both cases. To properly model this information on a daily, calendarized basis, we must split the overall attendance figure into equal chunks over the duration of its start and end dates.

## AEI by Event Category and Log Transforms

Determining the daily `impact` (the proportionate, summed `phq attendance` across all events occurring on a specific day) allows a data scientist to incorporate a value representative of the estimated number of people attending (or affected) by events that day to a machine learning model.

Given the (typically) exponential distribution observed in predicted attendance, we recommend to log transform each of the `impact` figures that are computed. While this typically muddies the interpretation of the value being provided to a forecasting algorithm, this process (especially for linear regressors) tends to improve forecasting performance.

## Additional Packages

This assumes the local usage of `pandas>=0.20.0`.
