# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

import unittest
from datetime import datetime

from tests import with_mock_client, with_mock_responses, with_client

from predicthq.endpoints.v1.events.schemas import EventResultSet, CalendarResultSet, Count


class EventsTest(unittest.TestCase):

    @with_mock_client()
    def test_search_params(self, client):
        client.events.search(id="id", q="query", rank_level=[4,5], rank__gt=85, country=["NZ", "AU"],
             within__radius="2km", within__longitude=-71.0432, within__latitude=42.346,
             label=["label1", "label2"], category="category",
             place__scope=["place1", "place2"], place__exact=["place3"],
             start__gte="2016-03-01", start__lt=datetime(2016, 4, 1), start__tz="Pacific/Auckland",
             active__gte="2016-03-01", active__lt=datetime(2016, 4, 1), active__tz="Pacific/Auckland",
             signal__id='zVNLr8tHvWQw', signal__explain=datetime(2016, 4, 1))

        client.request.assert_called_once_with('get', '/v1/events/', params={
            'id': 'id', 'rank.gt': 85, 'rank_level': '4,5', 'category': 'category', 'country': 'NZ,AU',
            'within': '2km@42.346,-71.0432', 'label': 'label1,label2', 'q': 'query',
            'place.scope': 'place1,place2', 'place.exact': 'place3',
            'start.lt': '2016-04-01T00:00:00.000000', 'start.gte': '2016-03-01T00:00:00.000000', 'start.tz': 'Pacific/Auckland',
            'active.lt': '2016-04-01T00:00:00.000000', 'active.gte': '2016-03-01T00:00:00.000000', 'active.tz': 'Pacific/Auckland',
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
