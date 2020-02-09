from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://developer.predicthq.com/guides/quickstart/
ACCESS_TOKEN = 'abc123'

phq = Client(access_token=ACCESS_TOKEN)


# The PredictHQ API offers two types of aggregation on events.

# You can either aggregate on PHQ Rank
# https://developer.predicthq.com/resources/events/#param-impact-rank
for event in phq.events.impact(active__gte="2015-12-24", active__lte="2015-12-26", impact_rank="rank"):
    print(event.rank_levels, event.rank_levels_impact, event.categories, event.categories_impact)


# or aggregate on Aviation Rank
# https://developer.predicthq.com/resources/events/#param-impact-rank
for event in phq.events.impact(active__gte="2015-12-24", active__lte="2015-12-26", impact_rank="aviation_rank"):
    print(event.aviation_rank_levels, event.aviation_rank_levels_impact, event.categories, event.categories_impact)
