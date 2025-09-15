from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = "abc123"

phq = Client(access_token=ACCESS_TOKEN)


# The search() method returns an EventResultSet which allows you to iterate
# over the first page of Broadcast objects (10 results by default)
for broadcast in phq.broadcasts.search():
    print(broadcast.model_dump(exclude_none=True))


# You can access the Broadcast object attributes directly.
# Broadcast fields and their description are available at
# https://docs.predicthq.com/resources/broadcasts/#broadcast-fields.
for broadcast in phq.broadcasts.search():
    print(
        broadcast.event.title,
        broadcast.phq_viewership,
        broadcast.event.category,
        broadcast.dates.start.strftime("%Y-%m-%d"),
    )


# You can add parameters to filter your search further.
# The following example searches for the broadcasts
# with PHQ viewership gte 100 and with event (the physical event the broadcast links to) label 'nfl'.
# The full list of parameters is available at
# https://docs.predicthq.com/resources/broadcasts/#search-broadcasts
for broadcast in phq.broadcasts.search(phq_viewership__gte=100, event__label="nfl"):
    print(
        broadcast.event.title,
        broadcast.phq_viewership,
        broadcast.event.labels,
        broadcast.dates.start.strftime("%Y-%m-%d"),
    )


# Please note that for dot ('.') separated parameters in the API,
# you can use one of the two following formats in the Python SDK:
# - double underscores: phq.broadcasts.search(location__origin='45.5051,-122.6750')
# - dictionary: phq.broadcasts.search(location={'origin': '45.5051,-122.6750'})
for broadcast in phq.broadcasts.search(location={"origin": "45.5051,-122.6750"}):
    print(
        broadcast.event.title,
        broadcast.phq_viewership,
        broadcast.location.places[0].place_id,
    )


# Please note that you can use comma separated string parameters in the API
# when you need to specify multiple options. This translates to Python lists
# parameters in the Python SDK.
for broadcast in phq.broadcasts.search(location__place_id=["5742126", "5799783"]):
    print(
        broadcast.event.title,
        broadcast.phq_viewership,
        broadcast.location.country,
        broadcast.location.places[0].place_id,
    )
