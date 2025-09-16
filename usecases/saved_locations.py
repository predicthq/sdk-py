from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = "abc123"

phq = Client(access_token=ACCESS_TOKEN)


# You can search saved-locations in a very similar way as for events.
# https://docs.predicthq.com/api/saved-locations/search-saved-locations
for savedLocation in phq.saved_locations.search():
    print(savedLocation.location_id, savedLocation.create_dt, savedLocation.status)

for savedLocation in phq.saved_locations.search(labels=["venue"]):
    print(savedLocation.location_id, savedLocation.create_dt, savedLocation.status)

# Retrieve via query string search, and sort
result = phq.saved_locations.get(q="London", sort="-created")
print(result.location_id, result.create_dt, result.status, result.geojson)


# You can also create a new saved-location by providing a name and a geojson polygon
polygon_geojson = {
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [-87.94056213135401, 42.2319776767614],
                [-89.50381034693073, 41.273515480388085],
                [-86.81789419577427, 41.42279055968166],
                [-87.94056213135401, 42.2319776767614],
            ]
        ],
    },
}
phq.saved_locations.create(name="location_name_here", geojson=polygon_geojson)


# ... or a geojson point with a radius
point_geojson = {
    "type": "Feature",
    "properties": {"radius": 2.23, "radius_unit": "mi"},
    "geometry": {"type": "Point", "coordinates": [-115.1728484, 36.1147065]},
}
phq.saved_locations.create(name="new_created_location_3", geojson=point_geojson)


# You can replace location data, given its location_id
phq.saved_locations.replace_location_data(
    location_id="location_id_here",
    name="location_name_udpated",
    geojson=polygon_geojson,
)


# Retrieve a certain location by its location_id
result = phq.saved_locations.get(location_id="location_id_here")
print(result.location_id, result.create_dt, result.status, result.geojson)


# You can search for events within a certain saved-location by providing its location_id
for event in phq.saved_locations.search_event_result_set(
        location_id="some_location_id_here",
        date_range_type="next_90d",
        category="concerts,community",
        limit=10,
    ):
    print(event.title, event.start.strftime("%Y-%m-%d"), event.category)



# You can also refresh the insights for a certain saved-location by providing its location_id
phq.saved_locations.refresh_location_insights(location_id="location_id_here")


# You can delete a certain saved-location by providing its location_id
result = phq.saved_locations.delete_location(location_id="location_id_here")


# You can enable sharing for a certain saved-location by providing its location_id
phq.saved_locations.sharing_enable(location_id="location_id_here")
