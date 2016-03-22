# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

import unittest

from predicthq.endpoints import schemas
from tests import with_mock_client, with_mock_responses, with_client

from predicthq.endpoints.v1.places.schemas import PlaceResultSet


class PlacesTest(unittest.TestCase):

    @with_mock_client()
    def test_search_params(self, client):
        client.places.search(country=["NZ", "AU"])
        client.request.assert_called_once_with('get', '/v1/places/', params={'country': 'NZ,AU'})

    @with_mock_client()
    def test_invalide_search_params(self, client):
        with self.assertRaises(schemas.SchematicsValidationError):
            client.places.search()

    @with_client()
    @with_mock_responses()
    def test_search(self, client, responses):
        result = client.places.search(country=["NZ", "AU"])
        self.assertIsInstance(result, PlaceResultSet)
        self.assertEqual(result.count, len(list(result.iter_all())))
        self.assertEqual(1, len(responses.calls))
