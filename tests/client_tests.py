# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function


import unittest

import predicthq
from predicthq import endpoints
from predicthq.endpoints.oauth2.schemas import AccessToken
from predicthq.exceptions import ClientError, ServerError

from tests import with_mock_responses, with_config, with_mock_client, load_fixture


class ClientTest(unittest.TestCase):

    def setUp(self):
        self.client = predicthq.Client()

    @with_config(ENDPOINT_URL="https://api.predicthq.com")
    def test_build_url(self):
        self.assertEqual(self.client.build_url('v1'), "https://api.predicthq.com/v1/")

    def test_endpoints_initialization(self):
        self.assertIsInstance(self.client.oauth2, endpoints.OAuth2Endpoint)
        self.assertIsInstance(self.client.accounts, endpoints.AccountsEndpoint)
        self.assertIsInstance(self.client.events, endpoints.EventsEndpoint)
        self.assertIsInstance(self.client.signals, endpoints.SignalsEndpoint)

    @with_mock_responses()
    def test_request(self, responses):
        self.client.logger.setLevel('DEBUG')

        self.assertDictEqual(self.client.get("/v1/"), responses.calls[0].response.json())

        self.assertIsNone(self.client.get("/no-content/"))

        self.assertIsNone(self.client.get("/invalid-json/"))

        with self.assertRaises(ClientError) as ctx:
            self.client.get("/not-found/")
            self.assertEqual(ctx.exception.message, responses.calls[3].response.json())

        with self.assertRaises(ServerError) as ctx:
            self.client.get("/server-error/")
            self.assertEqual(ctx.exception.message, responses.calls[4].response.json())

        # Test headers
        self.client.authenticate(client_id='client_id', client_secret='client_secret', scope=['account'])
        self.assertEqual(responses.calls[5].request.headers['Authorization'], 'Basic Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ=')
        self.assertEqual(responses.calls[5].request.headers['Content-Type'], 'application/x-www-form-urlencoded')

        self.client.accounts.self()
        self.assertEqual(responses.calls[6].request.headers['Authorization'], 'Bearer token123')
        self.assertEqual(responses.calls[6].request.headers['Accept'], 'application/json')

    @with_mock_client(request_returns={"result": "value"})
    def test_get(self, client):
        result = self.client.get('/get/', params={'q': 'query'})
        client.request.assert_called_once_with('get', '/get/', params={'q': 'query'})
        self.assertDictEqual(result, client.request.return_value)

    @with_mock_client(request_returns={"result": "value"})
    def test_post(self, client):
        result = self.client.post('/post/', data={'key': 'value'})
        client.request.assert_called_once_with('post', '/post/', data={'key': 'value'})
        self.assertDictEqual(result, client.request.return_value)

    @with_mock_client(request_returns={"result": "value"})
    def test_put(self, client):
        result = self.client.put('/put/', data={'key': 'value'})
        client.request.assert_called_once_with('put', '/put/', data={'key': 'value'})
        self.assertDictEqual(result, client.request.return_value)

    @with_mock_client(request_returns={"result": "value"})
    def test_patch(self, client):
        result = self.client.patch('/patch/', data={'key': 'value'})
        client.request.assert_called_once_with('patch', '/patch/', data={'key': 'value'})
        self.assertDictEqual(result, client.request.return_value)

    @with_mock_client()
    def test_delete(self, client):
        result = client.delete('/delete/')
        client.request.assert_called_once_with('delete', '/delete/')
        self.assertEqual(result, client.request.return_value)

    @with_mock_client(request_returns=load_fixture('access_token'))
    def test_authenticate(self, client):
        token = self.client.authenticate(client_id='client_id', client_secret='client_secret', scope=['account', 'events', 'signals'])
        client.request.assert_called_once_with('post', '/oauth2/token/', auth=('client_id', 'client_secret'), data={'scope': 'account events signals', 'grant_type': 'client_credentials'})

        self.assertIsInstance(token, AccessToken)
        self.assertDictEqual(token.to_primitive(), client.request.return_value)

        self.assertEqual(self.client.access_token, 'token123')

    def test_construct_with_access_token(self):
        client = predicthq.Client(access_token='token123')
        self.assertEqual(client.access_token, 'token123')

    @with_config(OAUTH2_ACCESS_TOKEN='token123')
    def test_construct_with_access_token_config(self):
        client = predicthq.Client()
        self.assertEqual(client.access_token, 'token123')
