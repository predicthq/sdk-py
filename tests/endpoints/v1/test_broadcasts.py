import unittest

from predicthq.endpoints.v1.broadcasts.schemas import BroadcastResultSet
from tests import load_fixture, with_mock_client, with_mock_responses, with_client


class BroadcastsTest(unittest.TestCase):
    @with_mock_client(request_returns=load_fixture("requests_responses/broadcasts_test/test_empty_search"))
    def test_search_params_underscores(self, client):
        client.broadcasts.search(
            broadcast_id="broadcast_id",
            location__origin="34.05223,-118.24368",
            location__place_id="place_id",
            phq_viewership__gte=1,
            phq_viewership__lte=10,
            start__gte="2020-10-01",
            start__lt="2020-10-15",
            start__tz="Pacific/Auckland",
            updated__gte="2020-11-01",
            updated__lt="2020-11-30",
            updated__tz="Pacific/Auckland",
            first_seen__gte="2020-10-10",
            first_seen__lt="2020-10-20",
            first_seen__tz="Pacific/Auckland",
            record_status=["active", "deleted"],
            broadcast_status=["scheduled", "predicted", "cancelled"],
            event__event_id="event_id",
            event__category="sports",
            event__label=["sport", "nfl"],
        )

        client.request.assert_called_once_with(
            "get",
            "/v1/broadcasts/",
            params={
                "broadcast_id": "broadcast_id",
                "location.origin": "34.05223,-118.24368",
                "location.place_id": "place_id",
                "phq_viewership.gte": 1,
                "phq_viewership.lte": 10,
                "start.gte": "2020-10-01",
                "start.lt": "2020-10-15",
                "start.tz": "Pacific/Auckland",
                "updated.gte": "2020-11-01",
                "updated.lt": "2020-11-30",
                "updated.tz": "Pacific/Auckland",
                "first_seen.gte": "2020-10-10",
                "first_seen.lt": "2020-10-20",
                "first_seen.tz": "Pacific/Auckland",
                "record_status": "active,deleted",
                "broadcast_status": "scheduled,predicted,cancelled",
                "event.event_id": "event_id",
                "event.category": "sports",
                "event.label": "sport,nfl",
            },
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/broadcasts_test/test_empty_search"))
    def test_search_params_underscores_without_ssl_verification(self, client):
        client.broadcasts.search(
            broadcast_id="broadcast_id",
            config__verify_ssl=False,
        )

        client.request.assert_called_once_with(
            "get",
            "/v1/broadcasts/",
            params={"broadcast_id": "broadcast_id"},
            verify=False,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/broadcasts_test/test_empty_search"))
    def test_search_params_dicts(self, client):
        client.broadcasts.search(
            broadcast_id="broadcast_id",
            location={"origin": "34.05223,-118.24368", "place_id": "place_id"},
            phq_viewership={"gte": 1, "lte": 10},
            start={"gte": "2020-10-01", "lt": "2020-10-15", "tz": "Pacific/Auckland"},
            updated={"gte": "2020-11-01", "lt": "2020-11-30", "tz": "Pacific/Auckland"},
            first_seen={"gte": "2020-10-10", "lt": "2020-10-20", "tz": "Pacific/Auckland"},
            record_status=["active", "deleted"],
            broadcast_status=["scheduled", "predicted", "cancelled"],
            event={"event_id": "event_id", "category": "sports", "label": ["sport", "nfl"]},
        )

        client.request.assert_called_once_with(
            "get",
            "/v1/broadcasts/",
            params={
                "broadcast_id": "broadcast_id",
                "location.origin": "34.05223,-118.24368",
                "location.place_id": "place_id",
                "phq_viewership.gte": 1,
                "phq_viewership.lte": 10,
                "start.gte": "2020-10-01",
                "start.lt": "2020-10-15",
                "start.tz": "Pacific/Auckland",
                "updated.gte": "2020-11-01",
                "updated.lt": "2020-11-30",
                "updated.tz": "Pacific/Auckland",
                "first_seen.gte": "2020-10-10",
                "first_seen.lt": "2020-10-20",
                "first_seen.tz": "Pacific/Auckland",
                "record_status": "active,deleted",
                "broadcast_status": "scheduled,predicted,cancelled",
                "event.event_id": "event_id",
                "event.category": "sports",
                "event.label": "sport,nfl",
            },
            verify=True,
        )

    @with_mock_client(request_returns=load_fixture("requests_responses/broadcasts_test/test_empty_search"))
    def test_search_params_dicts_without_ssl_verification(self, client):
        client.broadcasts.search(
            broadcast_id="broadcast_id",
            config={"verify_ssl": False},
        )

        client.request.assert_called_once_with(
            "get",
            "/v1/broadcasts/",
            params={"broadcast_id": "broadcast_id"},
            verify=False,
        )

    @with_client()
    @with_mock_responses()
    def test_search(self, client, responses):
        result = client.broadcasts.search(broadcast_id="PmJUAWRQLsKkg9MGTQU2JA")
        assert isinstance(result, BroadcastResultSet)
        assert result.count == len(list(result.iter_all()))
        assert len(responses.calls) == 1
