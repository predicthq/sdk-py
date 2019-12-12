import unittest

import pytest
import six

from predicthq.endpoints.oauth2.schemas import AccessToken
from predicthq.exceptions import ValidationError
from tests import with_mock_client, load_fixture, with_mock_responses, with_client


class OAuth2Test(unittest.TestCase):

    @with_mock_client(request_returns=load_fixture('access_token'))
    def test_get_token_params(self, client):
        token = client.oauth2.get_token(client_id='client_id', client_secret='client_secret', scope=['account', 'events'])
        client.request.assert_called_once_with('post', '/oauth2/token/', auth=('client_id', 'client_secret'), data={'scope': 'account events', 'grant_type': 'client_credentials'})
        assert isinstance(token, AccessToken)
        assert token.to_primitive() == client.request.return_value

        with pytest.raises(ValidationError):
            client.oauth2.get_token(client_id=None)

        with pytest.raises(ValidationError):
            client.oauth2.get_token(invalid_arg=None)

    @with_mock_client()
    def test_revoke_token_params(self, client):
        result = client.oauth2.revoke_token(client_id='client_id', client_secret='client_secret', token='token123')
        client.request.assert_called_once_with('post', '/oauth2/revoke/', auth=('client_id', 'client_secret'), data={'token': 'token123', 'token_type_hint': 'access_token'})
        assert result is None

        with pytest.raises(ValidationError):
            client.oauth2.revoke_token(token=None)

        with pytest.raises(ValidationError):
            client.oauth2.revoke_token(invalid_arg=None)

    @with_client()
    @with_mock_responses()
    def test_get_token(self, client, responses):
        token = client.oauth2.get_token(client_id='client_id', client_secret='client_secret', scope=['account', 'events'])
        assert isinstance(token, AccessToken)
        assert token.access_token == "token123"
        assert token.token_type == "Bearer"
        assert token.scope == ['account', 'events']
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['Content-Type'] == 'application/x-www-form-urlencoded'
        assert responses.calls[0].request.headers['Authorization'] == 'Basic Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ='
        assert dict(six.moves.urllib.parse.parse_qsl(responses.calls[0].request.body)) == {'scope': 'account events', 'grant_type': 'client_credentials'}

    @with_client()
    @with_mock_responses()
    def test_revoke_token(self, client, responses):
        result = client.oauth2.revoke_token(client_id='client_id', client_secret='client_secret', token='token123')
        assert result is None
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['Content-Type'] == 'application/x-www-form-urlencoded'
        assert responses.calls[0].request.headers['Authorization'] == 'Basic Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ='
        assert dict(six.moves.urllib.parse.parse_qsl(responses.calls[0].request.body)) == {'token_type_hint': 'access_token', 'token': 'token123'}
