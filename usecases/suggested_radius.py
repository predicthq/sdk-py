from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = 'abc123'

phq = Client(access_token=ACCESS_TOKEN)


# Get suggested radius for a given location and the industry of interest
# to be used when retrieving events. supported industries: "parking",
# "restaurants", "retail", "accommodation",
suggested_radius = phq.radius.search(location__origin="45.5051,-122.6750")
print(suggested_radius.radius, suggested_radius.radius_unit, suggested_radius.location.model_dump(exclude_none=True))


suggested_radius = phq.radius.search(location__origin="45.5051,-122.6750", radius_unit="mi", industry="retail")
print(suggested_radius.radius, suggested_radius.radius_unit, suggested_radius.location.model_dump(exclude_none=True))
