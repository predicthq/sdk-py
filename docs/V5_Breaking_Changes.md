# V5 breaking changes details

V5 removes the following fields from the Beam correlation results response;
* features
* phq_impact_sum
* phq_spend_sum
* phq_attendance_sum
* phq_rank_count

It is recommended to query features directly from [Features API](https://docs.predicthq.com/api/features/get-features)
