from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = "abc123"

phq = Client(access_token=ACCESS_TOKEN)


# Get the impact area as a polygon for a given location and industry.
# Supported industries: "parking", "restaurants", "retail", "accommodation",
# "cpg", "tourism", "marketing", "transportation", "other"
result = phq.impact_area.search(location__origin="45.5051,-122.6750", industry="accommodation")
print(result.geojson.geometry.type)
print(result.geojson.geometry.coordinates)
print(result.location.model_dump(exclude_none=True))
print(result.warnings)


# Get the impact area as a radius instead of a polygon
result = phq.impact_area.search(location__origin="45.5051,-122.6750", industry="retail", area_type="radius")
print(result.geojson.properties.radius, result.geojson.properties.radius_unit)
print(result.geojson.geometry.coordinates)


# Get the impact area as a radius with a specific unit (m, km, ft, mi)
result = phq.impact_area.search(
    location__origin="45.5051,-122.6750", industry="restaurants", area_type="radius", radius_unit="km"
)
print(result.geojson.properties.radius, result.geojson.properties.radius_unit)
