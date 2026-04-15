import unittest

from predicthq.endpoints.v1.impact_area.schemas import (
    ImpactAreaResultSet,
    GeoJsonFeature,
    LocationResult,
    RadiusProperties,
    Point,
    Polygon,
)
from tests import load_fixture, with_mock_client


class ImpactAreaTest(unittest.TestCase):
    @with_mock_client(request_returns=load_fixture("requests_responses/impact_area_test/test_search_polygon"))
    def test_search_polygon_default(self, client):
        result = client.impact_area.search(
            location__origin="37.7749,-122.4194",
        )

        client.request.assert_called_once_with(
            "get",
            "/v1/impact-area/",
            params={
                "location.origin": "37.7749,-122.4194",
            },
            verify=True,
        )

        assert isinstance(result, ImpactAreaResultSet)
        assert isinstance(result.location, LocationResult)
        assert result.location.lat == "37.7749"
        assert result.location.lon == "-122.4194"
        assert isinstance(result.geojson, GeoJsonFeature)
        assert result.geojson.type == "Feature"
        assert isinstance(result.geojson.geometry, Polygon)
        assert result.geojson.geometry.type == "Polygon"
        assert result.geojson.properties is None
        assert result.warnings == []

    @with_mock_client(request_returns=load_fixture("requests_responses/impact_area_test/test_search_polygon"))
    def test_search_polygon_with_industry(self, client):
        client.impact_area.search(
            industry="accommodation",
            location__origin="37.7749,-122.4194",
            area_type="polygon",
        )

        client.request.assert_called_once_with(
            "get",
            "/v1/impact-area/",
            params={
                "industry": "accommodation",
                "location.origin": "37.7749,-122.4194",
                "area_type": "polygon",
            },
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/impact_area_test/test_search_radius"))
    def test_search_radius(self, client):
        result = client.impact_area.search(
            industry="retail",
            location__origin="37.7749,-122.4194",
            area_type="radius",
            radius_unit="m",
        )

        client.request.assert_called_once_with(
            "get",
            "/v1/impact-area/",
            params={
                "industry": "retail",
                "location.origin": "37.7749,-122.4194",
                "area_type": "radius",
                "radius_unit": "m",
            },
            verify=True,
        )

        assert isinstance(result, ImpactAreaResultSet)
        assert isinstance(result.geojson.geometry, Point)
        assert result.geojson.geometry.type == "Point"
        assert result.geojson.geometry.coordinates == [-122.4194, 37.7749]
        assert isinstance(result.geojson.properties, RadiusProperties)
        assert result.geojson.properties.radius == 1500.0
        assert result.geojson.properties.radius_unit == "m"

    @with_mock_client(request_returns=load_fixture("requests_responses/impact_area_test/test_search_radius"))
    def test_search_radius_unit_km(self, client):
        client.impact_area.search(
            location__origin="37.7749,-122.4194",
            area_type="radius",
            radius_unit="km",
        )

        client.request.assert_called_once_with(
            "get",
            "/v1/impact-area/",
            params={
                "location.origin": "37.7749,-122.4194",
                "area_type": "radius",
                "radius_unit": "km",
            },
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/impact_area_test/test_search_with_warnings"))
    def test_search_with_warnings(self, client):
        result = client.impact_area.search(
            industry="parking",
            location__origin="37.7749,-122.4194",
        )

        client.request.assert_called_once_with(
            "get",
            "/v1/impact-area/",
            params={
                "industry": "parking",
                "location.origin": "37.7749,-122.4194",
            },
            verify=True,
        )

        assert isinstance(result, ImpactAreaResultSet)
        assert len(result.warnings) == 1
        assert "fallback to radius" in result.warnings[0]
