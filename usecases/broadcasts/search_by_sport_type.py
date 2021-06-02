from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = 'abc123'

phq = Client(access_token=ACCESS_TOKEN)


# The `scheduled` `broadcast_status` is for these broadcasts where we know the date,
# time and location of a TV broadcast based on TV schedule information.
# These are broadcasts for the seven top US leagues: NFL, NBA, NHL, MLB, MLS, D1 NCAA Basketball,
# and D1 NCAA Football.
# Broadcasts for sports other than the seven leagues have a `broadcast_status`
# of `predicted` since we predict their televised time and location (county).
# https://docs.predicthq.com/resources/broadcasts/#param-broadcast_status
for broadcast in phq.broadcasts.search(broadcast_status=['scheduled', 'predicted']):
    print(broadcast.event.title, broadcast.phq_viewership, broadcast.broadcast_status)


# The Broadcasts API also supports the `event.label` parameter which can be used to
# find broadcasts for specific sport types. Please note that all labels are lowercase.
# https://docs.predicthq.com/resources/broadcasts/#param-event.label
for broadcast in phq.broadcasts.search(event__label='nba'):
    print(broadcast.event.title, broadcast.phq_viewership, broadcast.event.labels)
