from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://developer.predicthq.com/guides/quickstart/
ACCESS_TOKEN = 'abc123'

phq = Client(access_token=ACCESS_TOKEN)


# The PredictHQ API offers two ways to filter by rank.

# You can either filter by rank value
# https://developer.predicthq.com/resources/events/#param-rank
for event in phq.events.search(rank={'gte': 60, 'lt': 80}):
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))


# or filter by rank level
# https://developer.predicthq.com/resources/events/#param-rank_level
# 1 - Minor (rank between 0 and 20)
# 2 - Moderate (rank between 21 and 40)
# 3 - Important (rank between 41 and 60)
# 4 - Significant (rank between 61 and 80)
# 5 - Major (rank between 81 and 100)
# rank_level accepts either a single value or a list of values
for event in phq.events.search(rank_level=[4]):
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))
