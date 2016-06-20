# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function
import csv
import os

import unittest

from predicthq.endpoints.v1.signals.schemas import SignalResultSet, Signal, SavedSignal
from predicthq.exceptions import ValidationError
from tests import with_client, with_mock_client, with_mock_responses, load_fixture


class SignalsTest(unittest.TestCase):

    @with_mock_client()
    def test_search_params(self, client):
        client.signals.search(sort=["-created_at", "updated_at"])
        client.request.assert_called_once_with('get', '/v1/signals/', params={'sort': '-created_at,updated_at'})

    @with_mock_client()
    def test_search_for_account(self, client):
        client.signals.for_account('account-id').search()
        client.request.assert_called_once_with('get', '/v1/accounts/account-id/signals/', params={})

    @with_mock_client(request_returns={"id": "signal-id", "name": "Test", "dimensions": [], "country": "NZ"})
    def test_get_params(self, client):
        client.signals.get(id="signal-id")
        client.request.assert_called_once_with('get', '/v1/signals/signal-id/')

        with self.assertRaises(ValidationError):
            client.signals.get(id=None)

    @with_mock_client(request_returns={"id": "signal-id", "name": "Test", "dimensions": [{"name": "dimension", "type": "category"}], "country": "NZ"})
    def test_create_params(self, client):
        client.signals.create(name="Test", dimensions=[{"name": "dimension", "type": "category"}], country="NZ")
        client.request.assert_called_once_with('post', '/v1/signals/', json={'country':'NZ', 'name':'Test', 'dimensions': [{'type':'category', 'name':'dimension'}]})

    @with_mock_client(request_returns={"id": "signal-id", "name": "Test", "dimensions": [{"name": "dimension", "type": "category"}], "country": "NZ"})
    def test_update_params(self, client):
        client.signals.update(id="signal-id", name="Test", dimensions=[{"name": "dimension", "type": "category"}], country="NZ")
        client.request.assert_called_once_with('put', '/v1/signals/signal-id/', json={'country':'NZ', 'dimensions': [{'type':'category', 'name':'dimension'}], 'name':'Test'})

        with self.assertRaises(ValidationError):
            client.signals.update(name="Test", dimensions=[{"name": "dimension", "type": "category"}], country="NZ")

    @with_mock_client()
    def test_delete_params(self, client):
        client.signals.delete(id="signal-id")
        client.request.assert_called_once_with('delete','/v1/signals/signal-id/')

        with self.assertRaises(ValidationError):
            client.signals.delete(id=None)

    @with_client()
    @with_mock_responses()
    def test_search(self, client, responses):
        result = client.signals.search()
        self.assertIsInstance(result, SignalResultSet)
        self.assertEqual(result.count, len(list(result.iter_all())))
        self.assertEqual(1, len(responses.calls))

    @with_client()
    @with_mock_responses()
    def test_get(self, client, responses):
        result = client.signals.get(id="zVNLr8tHvWQw")
        self.assertIsInstance(result, Signal)
        self.assertIsInstance(result, SavedSignal)

    @with_client()
    @with_mock_responses()
    def test_create(self, client, responses):
        result = client.signals.create(name="Test", country="NZ", dimensions=[{"name": "city", "type": "category"}, {"name": "revenue", "type": "number"}])
        self.assertIsInstance(result, Signal)
        self.assertIsInstance(result, SavedSignal)
        self.assertIsNotNone(result.id)

    @with_client()
    @with_mock_responses()
    def test_create(self, client, responses):
        result = client.signals.create(id="", name="Test 1", country="NZ", dimensions=[{"name": "city", "type": "category"}, {"name": "revenue", "type": "number"}])
        self.assertIsInstance(result, Signal)
        self.assertIsInstance(result, SavedSignal)
        self.assertIsNotNone(result.id)

    @with_client()
    @with_mock_responses()
    def test_create_via_signal(self, client, responses):
        signal = Signal()
        signal.name = "Test"
        signal.country = "NZ"
        signal.add_dimension("city", "category")
        signal.add_dimension("revenue", "number")
        result = signal.save(client.signals)
        self.assertIsInstance(result, Signal)
        self.assertIsInstance(result, SavedSignal)
        self.assertIsNotNone(result.id)

    @with_client()
    @with_mock_responses()
    def test_update(self, client, responses):
        result = client.signals.update(id="zVNLr8tHvWQw", name="Test 1", country="NZ", dimensions=[{"name": "city", "type": "category"}, {"name": "revenue", "type": "number"}])
        self.assertIsInstance(result, Signal)
        self.assertIsInstance(result, SavedSignal)
        self.assertIsNotNone(result.id)

    @with_client()
    @with_mock_responses()
    def test_update_via_signal(self, client, responses):
        signal = client.signals.get(id="zVNLr8tHvWQw")
        signal.remove_dimension("city")
        signal.add_dimension("cancelled_at", "date")
        result = signal.save()
        self.assertIsInstance(result, Signal)
        self.assertIsInstance(result, SavedSignal)

    @with_client()
    @with_mock_responses()
    def test_delete(self, client, responses):
        result = client.signals.delete(id="zVNLr8tHvWQw")
        self.assertIsNone(result)

    @with_client()
    @with_mock_responses()
    def test_delete_via_signal(self, client, responses):
        signal = client.signals.get(id="zVNLr8tHvWQw")
        result = signal.delete()
        self.assertIsNone(result)

    @with_client()
    @with_mock_responses()
    def test_delete(self, client, responses):
        result = client.signals.delete(id="zVNLr8tHvWQw")
        self.assertIsNone(result)

    @with_client()
    @with_mock_responses()
    def test_sink(self, client, responses):
        signal = client.signals.get(id="zVNLr8tHvWQw")
        signal.sink(load_fixture("data_points"), chunk_size=2)
        self.assertEqual(3, len(responses.calls))
        for i in range(1, 3):
            self.assertEqual(responses.calls[i].request.headers['Content-Type'], "application/x-ldjson")
            self.assertEqual(len(responses.calls[i].request.body.split("\n")), 2)
        # @todo: add tests for custom signal dimensions

    @with_client()
    @with_mock_responses()
    def test_summary(self, client, responses):
        signal = client.signals.get(id="zVNLr8tHvWQw")
        summary = signal.summary()
        self.assertEqual(summary.date.count, 2729)
        self.assertEqual(summary.initiated.count, 2729)
        self.assertEqual(summary.completed.count, 2729)
        self.assertListEqual(summary.location.bbox, [153.02342, -27.46846, 153.02342, -27.46846])
        # @todo: add tests for custom signal dimensions

    @with_client()
    @with_mock_responses()
    def test_analysis(self, client, responses):
        signal = client.signals.get(id="zVNLr8tHvWQw")
        analysis = signal.analysis()
        self.assertEqual(analysis.count, 365)
        # @todo: add tests for custom signal dimensions
