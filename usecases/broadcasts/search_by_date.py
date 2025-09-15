from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = "abc123"

phq = Client(access_token=ACCESS_TOKEN)


# We can use the `start.*`` parameters to filter broadcasts by time.
# For the time range in our example, we will use `start.gte=2020-11-01`
# and `start.lte=2020-11-30`.
# Using `start.tz=America/Los_Angeles` will treat the parameter’s start dates
# and times in the America/Los_Angeles time zone, otherwise the parameter
# dates and times will be treated as UTC.
# https://docs.predicthq.com/resources/broadcasts/#param-start
for broadcast in phq.broadcasts.search(
    start__gte="2020-11-01",
    start__lte="2020-11-30",
    start__tz="America/Los_Angeles",
    location__place_id=["5368381", "5391832"],
):
    print(
        broadcast.event.title,
        broadcast.phq_viewership,
        broadcast.location.country,
        broadcast.location.places[0].place_id,
    )


# If you want to fetch the recently updated broadcasts, you can use
# the `updated` parameter with a greater than or equal value.
# By default, the `updated` timezone is UTC but you can
# change this using the `updated.tz` parameter.
# https://docs.predicthq.com/resources/events/#param-updated
for event in phq.events.search(
    updated={"gte": "2019-09-24", "tz": "America/Los_Angeles"}
):
    print(event.rank, event.category, event.title, event.updated)
