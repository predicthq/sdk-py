from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = 'abc123'

phq = Client(access_token=ACCESS_TOKEN)


# The PredictHQ Aggregate Event Impact endpoint can be used to find the correlation between your demand and the events data.
# We always aggregate on the date but you can use different impact_rank values to specify how we calculate the impact.
# You will need a Premium Plan to access this endpoint and Aviation Rank subscription for Aviation Rank impact.

# You can either aggregate on PHQ Rank by passing impact_rank param as 'rank'.
# https://docs.predicthq.com/resources/events/#param-impact-rank
for impact_day in phq.events.impact(active__gte='2015-12-24', active__lte='2015-12-26', impact_rank='rank'):
    print(impact_day.date, impact_day.impact, impact_day.rank_levels, impact_day.rank_levels_impact, impact_day.categories, impact_day.categories_impact)


# or aggregate on Aviation Rank by passing impact_rank param as 'aviation_rank'.
# https://docs.predicthq.com/resources/events/#param-impact-rank
for impact_day in phq.events.impact(active__gte='2015-12-24', active__lte='2015-12-26', impact_rank='aviation_rank'):
    print(impact_day.date, impact_day.impact, impact_day.aviation_rank_levels, impact_day.aviation_rank_levels_impact, impact_day.categories, impact_day.categories_impact)
