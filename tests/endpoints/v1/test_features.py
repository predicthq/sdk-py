import unittest

from predicthq.endpoints.v1.features.schemas import FeatureResultSet
from tests import with_mock_client, with_mock_responses, with_client


class FeaturesTest(unittest.TestCase):

    @with_mock_client()
    def test_request_params_dicts(self, client):
        client.features.obtain_features(
            active={
                "gte": "2017-12-31",
                "lte": "2018-01-02"
            },
            location={
                "place_id": [4671654]
            },
            phq_rank_public_holidays=True
        )

        client.request.assert_called_once_with(
            'post', '/v1/features/',
            json={"active": {"gte": "2017-12-31", "lte": "2018-01-02"}, "location": {"place_id": ["4671654"]},
                  "phq_rank_public_holidays": True}
        )

    @with_client()
    @with_mock_responses()
    def test_obtain_features(self, client, responses):
        result = client.features.obtain_features(active={
                "gte": "2017-12-31",
                "lte": "2018-01-02"
            },
            location={
                "place_id": [4671654]
            },
            phq_rank_public_holidays=True)
        assert isinstance(result, FeatureResultSet)
