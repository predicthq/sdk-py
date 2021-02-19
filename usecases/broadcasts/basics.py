from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = 'abc123'

phq = Client(access_token=ACCESS_TOKEN)


# The search() method returns an EventResultSet which allows you to iterate
# over the first page of Broadcast objects (10 results by default)
for broadcast in phq.broadcasts.search():
    print(broadcast.to_dict())


# You can access the Broadcast object attributes directly.
# Broadcast fields and their description are available at
# https://docs.predicthq.com/resources/broadcasts/#broadcast-fields.
for broadcast in phq.broadcasts.search():
    print(broadcast.event.title, broadcast.phq_viewership, broadcast.event.category, broadcast.dates.start.strftime('%Y-%m-%d'))


# You can add parameters to filter your search further.
# The following example searches for the broadcasts
# with PHQ viewership gte 100 and with event (the physical event the broadcast links to) label 'nfl'.
# The full list of parameters is available at
# https://docs.predicthq.com/resources/broadcasts/#search-broadcasts
for broadcast in phq.broadcasts.search(phq_viewership__gte=100, event__label='nfl'):
    print(broadcast.event.title, broadcast.phq_viewership, broadcast.event.labels, broadcast.dates.start.strftime('%Y-%m-%d'))
