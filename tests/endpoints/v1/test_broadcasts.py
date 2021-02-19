import unittest

from predicthq.endpoints.v1.broadcasts.schemas import BroadcastResultSet
from tests import with_mock_client, with_mock_responses, with_client


class BroadcastsTest(unittest.TestCase):

    @with_mock_client()
    def test_search_params_underscores(self, client):
        client.broadcasts.search(
            broadcast_id='broadcast_id',
            location__origin='34.05223,-118.24368', location__place_id='place_id',
            phq_viewership__gte=1, phq_viewership__lte=10,
            start__gte='2020-10-01', start__lt='2020-10-15', start__tz='Pacific/Auckland',
            updated__gte='2020-11-01', updated__lt='2020-11-30', updated__tz='Pacific/Auckland',
            record_status=['active', 'deleted'], broadcast_status=['scheduled', 'cancelled'],
            event__event_id='event_id', event__category='sports', event__label=['sport', 'nfl']
        )

        client.request.assert_called_once_with(
            'get', '/v1/broadcasts/', params={
                'broadcast_id': 'broadcast_id',
                'location.origin': '34.05223,-118.24368', 'location.place_id': 'place_id',
                'phq_viewership.gte': 1, 'phq_viewership.lte': 10,
                'start.gte': '2020-10-01T00:00:00.000000', 'start.lt': '2020-10-15T23:59:59.999999', 'start.tz': 'Pacific/Auckland',
                'updated.gte': '2020-11-01T00:00:00.000000', 'updated.lt': '2020-11-30T23:59:59.999999', 'updated.tz': 'Pacific/Auckland',
                'record_status': 'active,deleted', 'broadcast_status': 'scheduled,cancelled',
                'event.event_id': 'event_id', 'event.category': 'sports', 'event.label': 'sport,nfl'
            }
        )

    @with_mock_client()
    def test_search_params_dicts(self, client):
        client.broadcasts.search(
            broadcast_id='broadcast_id',
            location={'origin': '34.05223,-118.24368', 'place_id': 'place_id'},
            phq_viewership={'gte': 1, 'lte': 10},
            start={'gte': '2020-10-01', 'lt': '2020-10-15', 'tz': 'Pacific/Auckland'},
            updated={'gte': '2020-11-01', 'lt': '2020-11-30', 'tz': 'Pacific/Auckland'},
            record_status=['active', 'deleted'], broadcast_status=['scheduled', 'cancelled'],
            event={'event_id': 'event_id', 'category': 'sports', 'label': ['sport', 'nfl']}
        )

        client.request.assert_called_once_with(
            'get', '/v1/broadcasts/', params={
                'broadcast_id': 'broadcast_id',
                'location.origin': '34.05223,-118.24368', 'location.place_id': 'place_id',
                'phq_viewership.gte': 1, 'phq_viewership.lte': 10,
                'start.gte': '2020-10-01T00:00:00.000000', 'start.lt': '2020-10-15T23:59:59.999999', 'start.tz': 'Pacific/Auckland',
                'updated.gte': '2020-11-01T00:00:00.000000', 'updated.lt': '2020-11-30T23:59:59.999999', 'updated.tz': 'Pacific/Auckland',
                'record_status': 'active,deleted', 'broadcast_status': 'scheduled,cancelled',
                'event.event_id': 'event_id', 'event.category': 'sports', 'event.label': 'sport,nfl'
            }
        )

    @with_client()
    @with_mock_responses()
    def test_search(self, client, responses):
        result = client.broadcasts.search(broadcast_id='PmJUAWRQLsKkg9MGTQU2JA')
        assert isinstance(result, BroadcastResultSet)
        assert result.count == len(list(result.iter_all()))
        assert len(responses.calls) == 1
