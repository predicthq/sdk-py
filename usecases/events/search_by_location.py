from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = 'abc123'

phq = Client(access_token=ACCESS_TOKEN)


# The events endpoint supports three types of search by location:
# - by area
# - by fuzzy location search around
# - by geoname place ID (see places endpoint for more details)


# The within parameter allows you to search for events within
# a specified area. It expects a string in the form
# {radius}{unit}@{latitude},{longitude}
# where the radius unit can be one of: m, km, ft, mi.
# https://docs.predicthq.com/resources/events/#param-within
# Please note that the the within parameter uses the lat, lon order
# but the location field in the event response uses the lon, lat GeoJSON order.
for event in phq.events.search(within='10km@-36.844480,174.768368'):
    print(event.rank, event.category, event.title, event.location)


# The fuzzy location search around doesn't restrict search results
# to the specified latitude, longitude and offset.
# In most cases, you only need to use the `origin` key,
# e.g. {'origin': '{lat},{lon}'}
# Please not that this affects the relevance of your search results.
# https://docs.predicthq.com/resources/events/#param-loc-around
for event in phq.events.search(location_around={'origin': '-36.844480,174.768368'}):
    print(event.rank, event.category, event.title, event.location, event.relevance)


# Finally, you can specify a geoname place ID or a list of place IDs or
# airport codes (see https://docs.predicthq.com/csv/airport_codes.csv)
# The scope suffix (includes events having children or parent of the place ID)
# or the exact (only events with the specified place ID) suffixes can be used.
# https://docs.predicthq.com/resources/events/#param-place
for event in phq.events.search(place={'scope': '5128638'}):  # place ID
    print(event.rank, event.category, event.title, event.place_hierarchies)

for event in phq.events.search(place={'scope': 'SFO'}):  # airport code
    print(event.rank, event.category, event.title, event.place_hierarchies)
