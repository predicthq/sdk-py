import unittest

import pytest

from predicthq.endpoints import schemas
from predicthq.endpoints.v1.places.schemas import PlaceResultSet
from tests import with_mock_client, with_mock_responses, with_client


class PlacesTest(unittest.TestCase):
    @with_mock_client()
    def test_search_params(self, client):
        client.places.search(country=["NZ", "AU"])
        client.request.assert_called_once_with(
            "get", "/v1/places/",
            params={"country": "NZ,AU"},
            verify=True,
        )

    @with_mock_client()
    def test_search_params_without_ssl_verification(self, client):
        client.places.search(country=["NZ", "AU"], config={"verify_ssl": False})
        client.request.assert_called_once_with(
            "get", "/v1/places/",
            params={"country": "NZ,AU"},
            verify=False,
        )

    @with_client()
    @with_mock_responses()
    def test_search(self, client, responses):
        result = client.places.search(country=["NZ", "AU"])
        assert isinstance(result, PlaceResultSet)
        assert result.count == len(list(result.iter_all()))
        assert len(responses.calls) == 1
