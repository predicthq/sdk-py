import unittest

from predicthq.endpoints.v1.events.schemas import (
    EventResultSet, CalendarResultSet, CountResultSet, ImpactResultSet
)
from tests import with_mock_client, with_mock_responses, with_client


class EventsTest(unittest.TestCase):

    @with_mock_client()
    def test_search_params_underscores(self, client):
        client.events.search(
            id='id', q='query', country=['NZ', 'AU'],
            rank_level=[4, 5], rank__gt=85,  local_rank_level=[4, 5], local_rank__gt=85,
            within__radius='2km', within__longitude=-71.0432, within__latitude=42.346,
            label=['label1', 'label2'], category='category', state='deleted',
            start_around__origin='2016-03-05', start_around__scale='5d',
            place__scope=['place1', 'place2'], place__exact=['place3'],
            start__gte='2016-03-01', start__lt='2016-04-01', start__tz='Pacific/Auckland',
            end__gte='2016-05-01', end__lt='2016-06-01', end__tz='Pacific/Auckland',
            active__gte='2016-03-01', active__lt='2016-04-01', active__tz='Pacific/Auckland',
            updated__gte='2016-03-01', updated__lt='2016-04-01', updated__tz='Pacific/Auckland',
        )

        client.request.assert_called_once_with(
            'get', '/v1/events/', params={
                'id': 'id', 'q': 'query', 'country': 'NZ,AU',
                'rank_level': '4,5', 'rank.gt': 85, 'local_rank_level': '4,5', 'local_rank.gt': 85,
                'within': '2km@42.346,-71.0432',
                'label': 'label1,label2', 'category': 'category', 'state': 'deleted',
                'start_around.origin': '2016-03-05', 'start_around.scale': '5d',
                'place.scope': 'place1,place2', 'place.exact': 'place3',
                'start.gte': '2016-03-01T00:00:00.000000', 'start.lt': '2016-04-01T23:59:59.999999', 'start.tz': 'Pacific/Auckland',
                'end.gte': '2016-05-01T00:00:00.000000', 'end.lt': '2016-06-01T23:59:59.999999', 'end.tz': 'Pacific/Auckland',
                'active.gte': '2016-03-01T00:00:00.000000', 'active.lt': '2016-04-01T23:59:59.999999', 'active.tz': 'Pacific/Auckland',
                'updated.gte': '2016-03-01T00:00:00.000000', 'updated.lt': '2016-04-01T23:59:59.999999', 'updated.tz': 'Pacific/Auckland',
            }
        )

    @with_mock_client()
    def test_search_params_dicts(self, client):
        client.events.search(
            id='id', q='query', country=['NZ', 'AU'],
            rank_level=[4, 5], rank={'gt': 85},
            within={'radius': '2km', 'longitude': -71.0432, 'latitude': 42.346},
            label=['label1', 'label2'], category='category', state='deleted',
            place={'scope': ['place1', 'place2'], 'exact': 'place3'},
            location_around={'origin': '40.730610,-73.935242', 'scale': '2km', 'offset': '0.5km'},
            start={'gte': '2016-03-01', 'lt': '2016-04-01', 'tz': 'Pacific/Auckland'},
            end={'gte': '2016-05-01', 'lt': '2016-06-01', 'tz': 'Pacific/Auckland'},
            active={'gte': '2016-03-01', 'lt': '2016-04-01', 'tz': 'Pacific/Auckland'},
            updated={'gte': '2016-03-01', 'lt': '2016-04-01', 'tz': 'Pacific/Auckland'},
        )

        client.request.assert_called_once_with(
            'get', '/v1/events/', params={
                'id': 'id', 'q': 'query', 'country': 'NZ,AU',
                'rank_level': '4,5', 'rank.gt': 85,
                'within': '2km@42.346,-71.0432',
                'label': 'label1,label2', 'category': 'category', 'state': 'deleted',
                'place.scope': 'place1,place2', 'place.exact': 'place3',
                'location_around.origin': '40.730610,-73.935242', 'location_around.scale': '2km', 'location_around.offset': '0.5km',
                'start.gte': '2016-03-01T00:00:00.000000', 'start.lt': '2016-04-01T23:59:59.999999', 'start.tz': 'Pacific/Auckland',
                'end.gte': '2016-05-01T00:00:00.000000', 'end.lt': '2016-06-01T23:59:59.999999', 'end.tz': 'Pacific/Auckland',
                'active.gte': '2016-03-01T00:00:00.000000', 'active.lt': '2016-04-01T23:59:59.999999', 'active.tz': 'Pacific/Auckland',
                'updated.gte': '2016-03-01T00:00:00.000000', 'updated.lt': '2016-04-01T23:59:59.999999', 'updated.tz': 'Pacific/Auckland',
            }
        )

    @with_mock_client()
    def test_search_for_account(self, client):
        client.events.for_account('account-id').search(q='query')
        client.request.assert_called_once_with('get', '/v1/accounts/account-id/events/', params={'q': 'query'})

    @with_client()
    @with_mock_responses()
    def test_search(self, client, responses):
        result = client.events.search(q='Foo Fighters', country='AU', limit=10)
        assert isinstance(result, EventResultSet)
        assert result.count == len(list(result.iter_all()))
        assert len(responses.calls) == 2

    @with_client()
    @with_mock_responses()
    def test_count(self, client, responses):
        result = client.events.count(active__gte='2015-01-01', active__lte='2015-12-31', within='50km@-27.470784,153.030124')
        assert isinstance(result, CountResultSet)
        assert result.count == 2501

    @with_client()
    @with_mock_responses()
    def test_calendar(self, client, responses):
        result = client.events.calendar(active__gte='2015-12-24', active__lte='2015-12-26', country='NZ', top_events__limit=1, top_events__sort=['rank'], active__tz='Pacific/Auckland')
        assert isinstance(result, CalendarResultSet)
        assert result.count == 60
        assert len(list(result.iter_all())) == 3
        assert len(responses.calls) == 1

    @with_client()
    @with_mock_responses()
    def test_impact(self, client, responses):
        result = client.events.impact(active__gte="2015-12-24", active__lte="2015-12-26", country="NZ", impact_rank="rank", active__tz="Pacific/Auckland")
        assert isinstance(result, ImpactResultSet)
        assert result.count == 76
        assert len(list(result.iter_all())) == 3
        assert len(responses.calls) == 1
