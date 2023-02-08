from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = 'abc123'

phq = Client(access_token=ACCESS_TOKEN)


suggested_radius = phq.radius.search(location__origin="45.5051,-122.6750")
print(suggested_radius)


suggested_radius = phq.radius.search(location__origin="45.5051,-122.6750", radius_unit="mi", industry="retail")
print(suggested_radius)
