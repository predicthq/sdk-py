from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = "abc123"

phq = Client(access_token=ACCESS_TOKEN)


# The events endpoint supports two types of search by location:
# - by latitude and longitude coordinates (location.origin)
# - by geoname place ID (location.place_id, see places endpoint for more details about geoname place ID)


# The `location.origin` parameter allows you to search for broadcasts
# happening in the county of the provided geopoint
# (a latitude and longitude coordinate string in the form {latitude},{longitude}).
# https://docs.predicthq.com/resources/broadcasts/#param-location.origin
for broadcast in phq.broadcasts.search(location__origin="45.5051,-122.6750"):
    print(
        broadcast.event.title,
        broadcast.phq_viewership,
        broadcast.location.places[0].place_id,
    )


# You can also specify a geoname place ID or a list of place IDs.
# The `location.place_id` suffix includes broadcasts being children
# or parent of the specified place ID.
# For the broadcasts happening in the US, the default location level
# is the county level. If you specify a city place ID, you'll get all
# the broadcasts for this city's county.
# https://docs.predicthq.com/resources/events/#param-place
for broadcast in phq.broadcasts.search(location__place_id="5746545"):
    print(
        broadcast.event.title,
        broadcast.phq_viewership,
        broadcast.location.country,
        broadcast.location.places[0].place_id,
    )
