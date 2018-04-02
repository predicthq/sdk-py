# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

import unittest
from datetime import datetime

from tests import with_mock_client, with_mock_responses, with_client

from predicthq.endpoints.v1.events.schemas import EventResultSet, CalendarResultSet, Count


class EventsTest(unittest.TestCase):

    @with_mock_client()
    def test_search_params_underscores(self, client):
        client.events.search(id="id", q="query", country=["NZ", "AU"],
             rank_level=[4,5], rank__gt=85,  local_rank_level=[4,5], local_rank__gt=85,
             within__radius="2km", within__longitude=-71.0432, within__latitude=42.346,
             label=["label1", "label2"], category="category", state='deleted',
             start_around__origin='2016-03-05', start_around__scale='5d',
             place__scope=["place1", "place2"], place__exact=["place3"],
             start__gte="2016-03-01", start__lt=datetime(2016, 4, 1), start__tz="Pacific/Auckland",
             end__gte="2016-05-01", end__lt=datetime(2016, 6, 1), end__tz="Pacific/Auckland",
             active__gte="2016-03-01", active__lt=datetime(2016, 4, 1), active__tz="Pacific/Auckland",
             updated__gte="2016-03-01", updated__lt=datetime(2016, 4, 1), updated__tz="Pacific/Auckland",
             signal__id="zVNLr8tHvWQw", signal__explain=datetime(2016, 4, 1))

        client.request.assert_called_once_with('get', '/v1/events/', params={
            'id': 'id', 'category': 'category', 'state': 'deleted', 'country': 'NZ,AU',
            'rank.gt': 85, 'rank_level': '4,5', 'local_rank.gt': 85, 'local_rank_level': '4,5',
            'within': '2km@42.346,-71.0432', 'label': 'label1,label2', 'q': 'query',
            'start_around.origin': '2016-03-05', 'start_around.scale': '5d',
            'place.scope': 'place1,place2', 'place.exact': 'place3',
            'start.lt': '2016-04-01T00:00:00.000000', 'start.gte': '2016-03-01T00:00:00.000000', 'start.tz': 'Pacific/Auckland',
            'end.lt': '2016-06-01T00:00:00.000000', 'end.gte': '2016-05-01T00:00:00.000000', 'end.tz': 'Pacific/Auckland',
            'active.lt': '2016-04-01T00:00:00.000000', 'active.gte': '2016-03-01T00:00:00.000000', 'active.tz': 'Pacific/Auckland',
            'updated.lt': '2016-04-01T00:00:00.000000', 'updated.gte': '2016-03-01T00:00:00.000000', 'updated.tz': 'Pacific/Auckland',
            'signal.id': 'zVNLr8tHvWQw', 'signal.explain': '2016-04-01'})

    @with_mock_client()
    def test_search_params_dicts(self, client):
        client.events.search(id="id", q="query", rank_level=[4,5], rank={"gt": 85}, country=["NZ", "AU"],
             within={"radius": "2km", "longitude": -71.0432, "latitude": 42.346},
             label=["label1", "label2"], category="category", state='deleted',
             place={"scope": ["place1", "place2"], "exact": "place3"},
             location_around={'origin': '40.730610,-73.935242', 'scale': '2km', 'offset': '0.5km'},
             start={"gte": "2016-03-01", "lt": datetime(2016, 4, 1), "tz": "Pacific/Auckland"},
             end={"gte": "2016-05-01", "lt": datetime(2016, 6, 1), "tz": "Pacific/Auckland"},
             active={"gte": "2016-03-01", "lt": datetime(2016, 4, 1), "tz": "Pacific/Auckland"},
             updated={"gte": "2016-03-01", "lt": datetime(2016, 4, 1), "tz": "Pacific/Auckland"},
             signal={"id": "zVNLr8tHvWQw", "explain": datetime(2016, 4, 1)})

        client.request.assert_called_once_with('get', '/v1/events/', params={
            'id': 'id', 'rank.gt': 85, 'rank_level': '4,5', 'category': 'category', 'state': 'deleted', 'country': 'NZ,AU',
            'within': '2km@42.346,-71.0432', 'label': 'label1,label2', 'q': 'query',
            'place.scope': 'place1,place2', 'place.exact': 'place3',
            'location_around.origin': '40.730610,-73.935242', 'location_around.scale': '2km', 'location_around.offset': '0.5km',
            'start.lt': '2016-04-01T00:00:00.000000', 'start.gte': '2016-03-01T00:00:00.000000', 'start.tz': 'Pacific/Auckland',
            'end.lt': '2016-06-01T00:00:00.000000', 'end.gte': '2016-05-01T00:00:00.000000', 'end.tz': 'Pacific/Auckland',
            'active.lt': '2016-04-01T00:00:00.000000', 'active.gte': '2016-03-01T00:00:00.000000', 'active.tz': 'Pacific/Auckland',
            'updated.lt': '2016-04-01T00:00:00.000000', 'updated.gte': '2016-03-01T00:00:00.000000', 'updated.tz': 'Pacific/Auckland',
            'signal.id': 'zVNLr8tHvWQw', 'signal.explain': '2016-04-01'})

    @with_mock_client()
    def test_search_for_account(self, client):
        client.events.for_account('account-id').search(q="query")
        client.request.assert_called_once_with('get', '/v1/accounts/account-id/events/', params={'q': 'query'})

    @with_client()
    @with_mock_responses()
    def test_search(self, client, responses):
        result = client.events.search(q="Foo Fighters", country="AU", limit=10)
        self.assertIsInstance(result, EventResultSet)
        self.assertEqual(result.count, len(list(result.iter_all())))
        self.assertEqual(2, len(responses.calls))

    @with_client()
    @with_mock_responses()
    def test_count(self, client, responses):
        result = client.events.count(active__gte="2015-01-01", active__lte="2015-12-31", within="50km@-27.470784,153.030124")
        self.assertIsInstance(result, Count)
        self.assertEqual(result.count, 2501)

    @with_client()
    @with_mock_responses()
    def test_calendar(self, client, responses):
        result = client.events.calendar(active__gte="2015-12-24", active__lte="2015-12-26", country="NZ", top_events__limit=1, top_events__sort=["rank"], active__tz="Pacific/Auckland")
        self.assertIsInstance(result, CalendarResultSet)
        self.assertEqual(result.count, 60)
        self.assertEqual(3, len(list(result.iter_all())))
        self.assertEqual(1, len(responses.calls))
