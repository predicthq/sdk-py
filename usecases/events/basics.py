from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = 'abc123'

phq = Client(access_token=ACCESS_TOKEN)


# The search() method returns an EventResultSet which allows you to iterate
# over the first page of Event objects (10 events by default)
for event in phq.events.search():
    print(event.to_dict())


# You can access the Event object attributes directly.
# Event fields and their description are available at
# https://docs.predicthq.com/resources/events/#fields.
for event in phq.events.search():
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))


# You can add parameters to filter your search further.
# The following example searches for the 'Katy Perry' events (full text search)
# with rank level of 4 or 5 (rank >= 60) in the concerts category.
# The full list of parameters is available at
# https://docs.predicthq.com/resources/events/#search-events
for event in phq.events.search(q='Katy Perry', rank_level=[4, 5], category='concerts'):
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))
