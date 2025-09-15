from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = "abc123"

phq = Client(access_token=ACCESS_TOKEN)


# You can search places in a very similar way as for events.
# The full list of parameters is available at
# https://docs.predicthq.com/resources/places/#search-places
# and the fields availables can be found at
# https://docs.predicthq.com/resources/places/#fields
for place in phq.places.search(q="New York", country="US"):
    print(place.id, place.name, place.type, place.location)


# You can inspect a single Place object by using the ?id query parameter
ny_state = phq.places.search(id="5128638").results[0]
print(ny_state.id, ny_state.name, ny_state.type, ny_state.location)
