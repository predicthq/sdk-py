from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = "abc123"

phq = Client(access_token=ACCESS_TOKEN)


# Filtering by start and/or end date.
# By default our events start and end date are in UTC but
# you can use the tz suffix to filter by local datetime and
# get the response in local datetime too.
# https://docs.predicthq.com/resources/events/#param-start
# https://docs.predicthq.com/resources/events/#param-end
start = {
    "gte": "2018-12-24",
    "lte": "2018-12-26",
    "tz": "Pacific/Auckland",
}
for event in phq.events.search(start=start, country="NZ"):
    print(event.rank, event.category, event.title, event.start.strftime("%Y-%m-%d"))


# Our date range filters allow both date (YYYY-MM-DD) and datetime (YYYY-MM-DD hh:mm:ss) formats
# So if you need a more granular date filtering you can perform the following
# https://docs.predicthq.com/api/requests/#param-date-range
start = {
    "gte": "2018-12-24T14:00:00",
    "lte": "2018-12-26T08:00:00",
    "tz": "Pacific/Auckland",
}
for event in phq.events.search(start=start, country="NZ"):
    print(event.rank, event.category, event.title, event.start.strftime("%Y-%m-%d"))


# If you are unsure of the exact start date, you can use the fuzzy date search
# with start_around and/or end_around parameters.
# https://docs.predicthq.com/resources/events/#param-start-around
# https://docs.predicthq.com/resources/events/#param-end-around
# Please note that using start_around will influence the relevance.
for event in phq.events.search(start_around={"origin": "2018-12-24"}, country="NZ"):
    print(
        event.rank,
        event.category,
        event.title,
        event.start.strftime("%Y-%m-%d"),
        event.relevance,
    )


# If you want to fetch the recently updated events, you can use the `updated` parameter
# with a greater than or equal value.
# By default, the `updated` timezone is UTC but you can
# change this using the `updated.tz` parameter.
# https://docs.predicthq.com/resources/events/#param-updated
for event in phq.events.search(updated={"gte": "2019-09-24", "tz": "America/Los_Angeles"}):
    print(event.rank, event.category, event.title, event.updated)
