from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = 'abc123'

phq = Client(access_token=ACCESS_TOKEN)

# "impact_patterns" field shows impact for leading days (days before the event), lagging days (days after an event) and the days the event occurs.
# impact_patterns is an array of impact pattern objects. The same event can have different impact patterns for different industry verticals.

# You can access the Event object attributes directly.
# Event fields and their description are available at
# https://docs.predicthq.com/resources/events/#event-fields
params = {"category": "severe-weather"}

for event in phq.events.search(**params):
    print(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d'))

    if event.impact_patterns:

        for impact_pattern in event.impact_patterns:
            print(impact_pattern.vertical, impact_pattern.impact_type)

            for impact in impact_pattern.impacts:
                print(impact.date_local, impact.value, impact.position)
