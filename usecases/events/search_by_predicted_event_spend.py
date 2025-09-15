from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = "abc123"

phq = Client(access_token=ACCESS_TOKEN)


# Predicted event spend is available as predicted_event_spend,
# predicted_event_spend_industry__accommodation,
# predicted_event_spend_industry__hospitality and
# predicted_event_spend_industry__transportation.

# You can filter by predicted_event_spend when searching.
# See https://docs.predicthq.com/resources/events/#param-predicted_event_spend
for event in phq.events.search(
    predicted_event_spend={"gte": 5000, "lte": 10000}, sort="predicted_event_spend"
):
    print(
        event.predicted_event_spend,
        event.category,
        event.title,
        event.start.strftime("%Y-%m-%d"),
    )
    # The predicted_event_spend field will only contain a value if there is a predicted event
    # spend for the event and if your subscription includes the feature in your API plan.


# You can filter by predicted_event_spend_industry__accommodation when searching.
# See https://docs.predicthq.com/resources/events/#param-predicted_event_spend
for event in phq.events.search(
    predicted_event_spend_industry__accommodation={"gte": 5000, "lte": 10000},
    sort="-predicted_event_spend_industry.accommodation",
):
    print(
        event.predicted_event_spend_industries.accommodation,
        event.category,
        event.title,
        event.start.strftime("%Y-%m-%d"),
    )
    # The predicted_event_spend field will only contain a value if there is a predicted event
    # spend for the event and if your subscription includes the feature in your API plan.


# You can filter by predicted_event_spend_industry_hospitality when searching.
# See https://docs.predicthq.com/resources/events/#param-predicted_event_spend
for event in phq.events.search(
    predicted_event_spend_industry__hospitality={"gte": 5000, "lte": 10000},
    sort="predicted_event_spend_industry.hospitality",
):
    print(
        event.predicted_event_spend_industries.hospitality,
        event.category,
        event.title,
        event.start.strftime("%Y-%m-%d"),
    )
    # The predicted_event_spend field will only contain a value if there is a predicted event
    # spend for the event and if your subscription includes the feature in your API plan.


# You can filter by predicted_event_spend_industry_transportation when searching.
# See https://docs.predicthq.com/resources/events/#param-predicted_event_spend
for event in phq.events.search(
    predicted_event_spend_industry__transportation={"gte": 5000, "lte": 10000},
    sort="predicted_event_spend_industry.transportation",
):
    print(
        event.predicted_event_spend_industries.transportation,
        event.category,
        event.title,
        event.start.strftime("%Y-%m-%d"),
    )
    # The predicted_event_spend field will only contain a value if there is a predicted event
    # spend for the event and if your subscription includes the feature in your API plan.
