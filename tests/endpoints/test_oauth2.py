import unittest
from urllib.parse import parse_qsl

from predicthq.endpoints.oauth2.schemas import AccessToken
from tests import with_mock_client, load_fixture, with_mock_responses, with_client


class OAuth2Test(unittest.TestCase):
    @with_mock_client(request_returns=load_fixture("access_token"))
    def test_get_token_params(self, client):
        token = client.oauth2.get_token(
            client_id="client_id",
            client_secret="client_secret",
            scope=["account", "events"],
        )
        client.request.assert_called_once_with(
            "post",
            "/oauth2/token/",
            auth=("client_id", "client_secret"),
            data={"scope": "account events", "grant_type": "client_credentials"},
            verify=True,
        )
        assert isinstance(token, AccessToken)
        token_dump = token.model_dump(exclude_none=True)
        token_dump["scope"] = " ".join(token.scope)
        assert token_dump == client.request.return_value

    @with_mock_client(request_returns=load_fixture("access_token"))
    def test_get_token_params_without_ssl_verification(self, client):
        client.oauth2.get_token(
            client_id="client_id",
            client_secret="client_secret",
            scope=["account", "events"],
            config__verify_ssl=False,
        )
        client.request.assert_called_once_with(
            "post",
            "/oauth2/token/",
            auth=("client_id", "client_secret"),
            data={"scope": "account events", "grant_type": "client_credentials"},
            verify=False,
        )

    @with_mock_client()
    def test_revoke_token_params(self, client):
        result = client.oauth2.revoke_token(client_id="client_id", client_secret="client_secret", token="token123")
        client.request.assert_called_once_with(
            "post",
            "/oauth2/revoke/",
            auth=("client_id", "client_secret"),
            data={"token": "token123", "token_type_hint": "access_token"},
            verify=True,
        )
        assert result is None

    @with_mock_client()
    def test_revoke_token_params_without_ssl_verification(self, client):
        client.oauth2.revoke_token(
            client_id="client_id",
            client_secret="client_secret",
            token="token123",
            config__verify_ssl=False,
        )
        client.request.assert_called_once_with(
            "post",
            "/oauth2/revoke/",
            auth=("client_id", "client_secret"),
            data={"token": "token123", "token_type_hint": "access_token"},
            verify=False,
        )

    @with_client()
    @with_mock_responses()
    def test_get_token(self, client, responses):
        token = client.oauth2.get_token(
            client_id="client_id",
            client_secret="client_secret",
            scope=["account", "events"],
        )
        assert isinstance(token, AccessToken)
        assert token.access_token == "token123"
        assert token.token_type == "Bearer"
        assert token.scope == ["account", "events"]
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers["Content-Type"] == "application/x-www-form-urlencoded"
        assert responses.calls[0].request.headers["Authorization"] == "Basic Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ="
        assert dict(parse_qsl(responses.calls[0].request.body)) == {
            "scope": "account events",
            "grant_type": "client_credentials",
        }

    @with_client()
    @with_mock_responses()
    def test_revoke_token(self, client, responses):
        result = client.oauth2.revoke_token(client_id="client_id", client_secret="client_secret", token="token123")
        assert result is None
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers["Content-Type"] == "application/x-www-form-urlencoded"
        assert responses.calls[0].request.headers["Authorization"] == "Basic Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ="
        assert dict(parse_qsl(responses.calls[0].request.body)) == {
            "token_type_hint": "access_token",
            "token": "token123",
        }

    def test_oauth2_endpoint_method_deprecation_warning(self):
        from predicthq.endpoints.oauth2.endpoint import OAuth2Endpoint
        import warnings

        expected_text = (
            "OAuth2 endpoints in the SDK are deprecated and will be removed in future releases. "
            "Use TokenAuth (API Access Token) with Client(..., access_token=...)."
        )

        endpoint = OAuth2Endpoint(client=None)

        # Test get_token
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                endpoint.get_token("id", "secret", "scope", "grant_type")
            except Exception:
                pass  # Ignore errors from None client
            assert any(
                issubclass(warning.category, FutureWarning) and expected_text in str(warning.message) for warning in w
            )

        # Test revoke_token
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                endpoint.revoke_token("id", "secret", "token", "hint")
            except Exception:
                pass  # Ignore errors from None client
            assert any(
                issubclass(warning.category, FutureWarning) and expected_text in str(warning.message) for warning in w
            )
