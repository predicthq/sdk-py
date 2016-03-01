# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

import unittest
from datetime import datetime

from tests import with_mock_client, with_mock_responses, with_client

from predicthq.endpoints.v1.events.schemas import EventResultSet, CalendarResultSet


class EventsTest(unittest.TestCase):

    @with_mock_client()
    def test_search_params(self, client):
        client.events.search(id="id", q="query", rank_level=[4,5], rank__gt=85, country=["NZ", "AU"],
             within__radius="2km", within__longitude=-71.0432, within__latitude=42.346,
             label=["label1", "label2"], category="category",
             start__gte="2016-03-01", start__lt=datetime(2016, 4, 1), start__tz="Pacific/Auckland",)

        client.request.assert_called_once_with('get', '/v1/events', params={
            'id': 'id', 'rank.gt': 85, 'rank_level': '4,5', 'category': 'category', 'country': 'NZ,AU',
            'within': '2km@42.346,-71.0432', 'label': 'label1,label2', 'q': 'query',
            'start.lt': '2016-04-01T00:00:00.000000', 'start.gte': '2016-03-01T00:00:00.000000', 'start.tz': 'Pacific/Auckland'})

    @with_mock_client(request_returns={"count": 12})
    def test_count_params(self, client):
        client.events.count(id="id", q="query", rank_level=[4,5], rank__gt=85, country=["NZ", "AU"],
             within__radius="2km", within__longitude=-71.0432, within__latitude=42.346,
             label=["label1", "label2"], category="category",
             start__gte="2016-03-01", start__lt=datetime(2016, 4, 1), start__tz="Pacific/Auckland",)

        client.request.assert_called_once_with('get', '/v1/events/count/', params={
            'id': 'id', 'rank.gt': 85, 'rank_level': '4,5', 'category': 'category', 'country': 'NZ,AU',
            'within': '2km@42.346,-71.0432', 'label': 'label1,label2', 'q': 'query',
            'start.lt': '2016-04-01T00:00:00.000000', 'start.gte': '2016-03-01T00:00:00.000000', 'start.tz': 'Pacific/Auckland'})

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
        result = client.events.count(q="Foo Fighters", country="AU", limit=10)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 12)

    @with_client()
    @with_mock_responses()
    def test_calendar(self, client, responses):
        result = client.events.calendar(start__gte="2015-12-24", start__lte="2015-12-26", country="NZ", top_events__limit=1, top_events__sort=["rank"])
        self.assertIsInstance(result, CalendarResultSet)
        self.assertEqual(result.count, 60)
        self.assertEqual(3, len(list(result.iter_all())))
        self.assertEqual(1, len(responses.calls))
