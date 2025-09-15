import unittest

from predicthq.endpoints.v1.events.schemas import EventResultSet
from tests import load_fixture, with_mock_client
from predicthq.endpoints.v1.saved_locations.schemas import (
    SavedLocation,
    SavedLocationResultSet,
    CreateSavedLocationResponse,
    PostSharingEnableResponse,
    SuggestedRadiusResponse,
    Location
)

class SavedLocationsTest(unittest.TestCase):
    @with_mock_client(
        request_returns=load_fixture("requests_responses/saved_locations_test/test_search")
    )
    def test_search(self, client):
        result = client.saved_locations.search()

        client.request.assert_called_once_with(
            "get",
            "/v1/saved-locations/",
            params={},
            verify=True,
        )

        assert isinstance(result, SavedLocationResultSet)


    @with_mock_client(
        request_returns=load_fixture("requests_responses/saved_locations_test/test_empty_search")
    )
    def test_search_params_underscores(self, client):
        client.saved_locations.search(
            updated__gt="2016-03-01",
            updated__gte="2016-03-01",
            updated__lt="2016-04-01",
            updated__lte="2016-04-01",
            q="query",
            location_id="yfQpe0p43Q5Clkqdei6n_g",
            location_code="4t855453234t5623",
            labels=["test", "retail"],
            user_id="hjqkKozgS8mm",
            subscription_valid_types=["events"],
        )

        client.request.assert_called_once_with(
            "get",
            "/v1/saved-locations/",
            params={
            "updated.gt":"2016-03-01",
            "updated.gte":"2016-03-01",
            "updated.lt":"2016-04-01",
            "updated.lte":"2016-04-01",
            "q":"query",
            "location_id":"yfQpe0p43Q5Clkqdei6n_g",
            "location_code":"4t855453234t5623",
            "labels":"test,retail",
            "user_id":"hjqkKozgS8mm",
            "subscription_valid_types":"events",
            },
            verify=True,
        )


    @with_mock_client(
        request_returns=load_fixture("requests_responses/saved_locations_test/test_empty_search")
    )
    def test_search_params_underscores(self, client):
        client.saved_locations.search(
            updated={
                "gt": "2016-03-01",
                "gte": "2016-03-01",
                "lt": "2016-04-01",
                "lte": "2016-04-01",
            },
            q="query",
            location_id="yfQpe0p43Q5Clkqdei6n_g",
            location_code="4t855453234t5623",
            labels=["test", "retail"],
            user_id="hjqkKozgS8mm",
            subscription_valid_types=["events"],
        )

        client.request.assert_called_once_with(
            "get",
            "/v1/saved-locations/",
            params={
            "updated.gt":"2016-03-01",
            "updated.gte":"2016-03-01",
            "updated.lt":"2016-04-01",
            "updated.lte":"2016-04-01",
            "q":"query",
            "location_id":"yfQpe0p43Q5Clkqdei6n_g",
            "location_code":"4t855453234t5623",
            "labels":"test,retail",
            "user_id":"hjqkKozgS8mm",
            "subscription_valid_types":"events",
            },
            verify=True,
        )


    @with_mock_client(
        request_returns=load_fixture("requests_responses/saved_locations_test/test_create")
    )
    def test_create(self, client):
        result = client.saved_locations.create(
            name="name",
            location_code="4t855453234t5623",
            description="saved location description",
            labels=["test", "retail"],
            geojson={
                "type": "Feature",
                "geometry": {
                  "coordinates": [
                    [
                      [-87.94056213135401, 42.2319776767614],
                      [-89.50381034693073, 41.273515480388085],
                      [-86.81789419577427, 41.42279055968166],
                      [-87.94056213135401, 42.2319776767614]
                    ]
                  ],
                  "type": "Polygon"
                }
              },
            place_ids=["5391959", "5391960"],
            formatted_address="formatted_address",
        )
        client.request.assert_called_once_with(
            "post",
            "/v1/saved-locations/",
            json={
                "name": "name",
                "geojson":{
                    "type": "Feature",
                    "geometry": {
                      "coordinates": [
                        [
                          [-87.94056213135401, 42.2319776767614],
                          [-89.50381034693073, 41.273515480388085],
                          [-86.81789419577427, 41.42279055968166],
                          [-87.94056213135401, 42.2319776767614]
                        ]
                      ],
                      "type": "Polygon"
                    }
                  },
                "location_code" : "4t855453234t5623",
                "description": "saved location description",
                "place_ids": ["5391959", "5391960"],
                "formatted_address": "formatted_address",
                "labels": ["test", "retail"],
            },
            verify=True,
        )
        assert isinstance(result, CreateSavedLocationResponse)


    @with_mock_client(request_returns="<html><body>OK</body></html>")
    def test_replace(self, client):
        client.saved_locations.replace_location_data(
            location_id="abc123",
            name="name",
            location_code="4t855453234t5623",
            description="saved location description",
            labels=["test", "retail"],
            geojson={
                "type": "Feature",
                "geometry": {
                    "coordinates": [
                        [
                            [-87.94056213135401, 42.2319776767614],
                            [-89.50381034693073, 41.273515480388085],
                            [-86.81789419577427, 41.42279055968166],
                            [-87.94056213135401, 42.2319776767614]
                        ]
                    ],
                    "type": "Polygon"
                }
            },
            place_ids=["5391959", "5391960"],
            formatted_address="formatted_address",
        )
        client.request.assert_called_once_with(
            "put",
            "/v1/saved-locations/abc123",
            json={
                "name": "name",
            "geojson":{
                "type": "Feature",
                "geometry": {
                  "coordinates": [
                    [
                      [-87.94056213135401, 42.2319776767614],
                      [-89.50381034693073, 41.273515480388085],
                      [-86.81789419577427, 41.42279055968166],
                      [-87.94056213135401, 42.2319776767614]
                    ]
                  ],
                  "type": "Polygon"
                }
              },
             "location_code" : "4t855453234t5623",
            "description": "saved location description",
            "place_ids": ["5391959", "5391960"],
            "formatted_address": "formatted_address",
            "labels": ["test", "retail"],
            },
            verify=True,
        )


    @with_mock_client()
    def test_delete_location(self, client):
        client.saved_locations.delete_location(location_id="abc123")

        client.request.assert_called_once_with(
            "delete",
            "/v1/saved-locations/abc123",
            params={},
            verify=True,
        )


    @with_mock_client()
    def test_refresh_location_insights(self, client):
        client.saved_locations.refresh_location_insights(location_id="abc123")

        client.request.assert_called_once_with(
            "post",
            "/v1/saved-locations/abc123/insights/refresh/",
            params={},
            verify=True,
        )


    @with_mock_client(request_returns={"share_url": "https://share.url/abc123"})
    def test_sharing_enable(self, client):
        client.saved_locations.sharing_enable(location_id="abc123")

        client.request.assert_called_once_with(
            "post",
            "/v1/saved-locations/abc123/sharing/enable",
            params={},
            verify=True,
        )


    @with_mock_client(request_returns=load_fixture("requests_responses/saved_locations_test/test_saved_location"))
    def test_get_location(self, client):
        result = client.saved_locations.get(location_id="some_location_id")

        client.request.assert_called_once_with(
            "get",
            "/v1/saved-locations/some_location_id",
            params={},
            verify=True,
        )
        assert isinstance(result, SavedLocation)


    @with_mock_client(
        request_returns=load_fixture("requests_responses/saved_locations_test/test_event_result_set")
    )
    def test_search_event_result_set(self, client):
        result = client.saved_locations.search_event_result_set(
            updated__gt="2016-03-01",
            updated__gte="2016-03-01",
            updated__lt="2016-04-01",
            updated__lte="2016-04-01",
            location_id="yfQpe0p43Q5Clkqdei6n_g",
        )

        assert isinstance(result, EventResultSet)


    @with_mock_client(
        request_returns=load_fixture("requests_responses/saved_locations_test/test_suggested_radius")
    )
    def test_suggested_radius(self, client):
        result = client.saved_locations.suggested_radius(
            location_origin="37.747767,-122.415202",
            industry="parking",
            radius_unit="km"
        )

        assert isinstance(result, SuggestedRadiusResponse)
