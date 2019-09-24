from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://developer.predicthq.com/guides/quickstart/
ACCESS_TOKEN = 'abc123'

phq = Client(access_token=ACCESS_TOKEN)


# events and places endpoints use the same approach for search pagination.


# By default the search() method only returns the first
# page of results, which contains at most 10 events.
# It's because the default values for the offset and limit parameters
# are respectively 0 and 10.
for event in phq.events.search():
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))


# You can modify this behaviour by specifying an offset and/or a limit.
# The following example skips the first 10 results (offset=10)
# and limits the results to 5 items (limit=5).
for event in phq.events.search(offset=10, limit=5):
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))

# You can chain the iter_all() generator to iterate over all your events.
# Please note that the following method call might iterate over millions
# of records.
for event in phq.events.search().iter_all():
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))
