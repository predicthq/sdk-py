from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = "abc123"

phq = Client(access_token=ACCESS_TOKEN)


# To find broadcasts for an event, we can use the `event.event_id` parameter.
# For the US events, this parameter allows us to retrieve broadcast records
# for each county the game has viewership in. So, for a specific game televised nation-wide,
# the API would return over 3000 broadcast records with viewership per county.
# The following example is for the 2019 Super Bowl game.
# https://docs.predicthq.com/resources/broadcasts/#param-event.event_id
for broadcast in phq.broadcasts.search(event__event_id="ePQLUqbPnMn3mQhe35"):
    print(
        broadcast.event.title,
        broadcast.phq_viewership,
        broadcast.location.places[0].name,
    )
