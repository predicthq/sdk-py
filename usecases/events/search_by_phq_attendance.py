from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = "abc123"

phq = Client(access_token=ACCESS_TOKEN)


# One of PredictHQ's data-enriching features is to provide predicted attendance
# numbers events. This is a paid feature and is extremely useful for demand
# intelligence and prediction. Predicted attendance is available as
# phq_attendance.

# You can filter by phq_attendance when searching.
# See https://docs.predicthq.com/resources/events/#param-phq_attendance
for event in phq.events.search(phq_attendance={"gte": 5000}):
    print(
        event.phq_attendance,
        event.category,
        event.title,
        event.start.strftime("%Y-%m-%d"),
    )
    # The phq_attendance field will only contain a value if there is a predicted
    # attendance for the event and if your subscription includes the feature in
    # your API plan.
