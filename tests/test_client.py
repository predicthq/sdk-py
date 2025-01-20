import unittest
from unittest import mock

import pytest
import requests
import stamina

import predicthq
from predicthq import endpoints
from predicthq.endpoints.oauth2.schemas import AccessToken
from predicthq.exceptions import ClientError, RetriableError, ServerError
from tests import load_fixture, with_config, with_mock_client, with_mock_responses


class ClientTest(unittest.TestCase):
    def setUp(self):
        stamina.set_testing(True)
        self.client = predicthq.Client()

    def tearDown(self):
        stamina.set_testing(False)

    @with_config(ENDPOINT_URL="https://api.predicthq.com")
    def test_build_url(self):
        assert self.client.build_url("v1") == "https://api.predicthq.com/v1"

    def test_endpoints_initialization(self):
        assert isinstance(self.client.oauth2, endpoints.OAuth2Endpoint)
        assert isinstance(self.client.accounts, endpoints.AccountsEndpoint)
        assert isinstance(self.client.events, endpoints.EventsEndpoint)
        assert isinstance(self.client.places, endpoints.PlacesEndpoint)

    @with_mock_responses()
    def test_request(self, responses):
        self.client.logger.setLevel("DEBUG")

        assert self.client.get("/v1/") == responses.calls[0].response.json()

        assert self.client.get("/no-content/") is None

        assert self.client.get("/invalid-json/") is None

        with pytest.raises(ClientError) as excinfo:
            self.client.get("/not-found/")
        assert excinfo.value.args[0] == responses.calls[3].response.json()

        with pytest.raises(ServerError) as excinfo:
            self.client.get("/server-error/")
        assert excinfo.value.args[0] == responses.calls[4].response.json()

        with pytest.raises(ServerError) as excinfo:
            self.client.get("/no-json/")
        assert excinfo.value.args[0] == responses.calls[5].response.content

        # Test headers
        self.client.authenticate(client_id="client_id", client_secret="client_secret", scope=["account"])
        assert responses.calls[6].request.headers["Authorization"] == "Basic Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ="
        assert responses.calls[6].request.headers["Content-Type"] == "application/x-www-form-urlencoded"

        self.client.accounts.self()
        assert responses.calls[7].request.headers["Authorization"] == "Bearer token123"
        assert responses.calls[7].request.headers["Accept"] == "application/json"

    @with_mock_client(request_returns={"result": "value"})
    def test_get(self, client):
        result = self.client.get("/get/", params={"q": "query"})
        client.request.assert_called_once_with("get", "/get/", params={"q": "query"})
        assert result == client.request.return_value

    @with_mock_client(request_returns={"result": "value"})
    def test_post(self, client):
        result = self.client.post("/post/", data={"key": "value"})
        client.request.assert_called_once_with("post", "/post/", data={"key": "value"})
        assert result == client.request.return_value

    @with_mock_client(request_returns={"result": "value"})
    def test_put(self, client):
        result = self.client.put("/put/", data={"key": "value"})
        client.request.assert_called_once_with("put", "/put/", data={"key": "value"})
        assert result == client.request.return_value

    @with_mock_client(request_returns={"result": "value"})
    def test_patch(self, client):
        result = self.client.patch("/patch/", data={"key": "value"})
        client.request.assert_called_once_with("patch", "/patch/", data={"key": "value"})
        assert result == client.request.return_value

    @with_mock_client()
    def test_delete(self, client):
        result = client.delete("/delete/")
        client.request.assert_called_once_with("delete", "/delete/")
        assert result == client.request.return_value

    @with_mock_client(request_returns=load_fixture("access_token"))
    def test_authenticate(self, client):
        token = self.client.authenticate(
            client_id="client_id", client_secret="client_secret", scope=["account", "events"]
        )
        client.request.assert_called_once_with(
            "post",
            "/oauth2/token/",
            auth=("client_id", "client_secret"),
            data={"scope": "account events", "grant_type": "client_credentials"},
            verify=True,
        )

        assert isinstance(token, AccessToken)

        assert self.client.access_token == "token123"

    def test_construct_with_access_token(self):
        client = predicthq.Client(access_token="token123")
        assert client.access_token == "token123"

    @with_config(OAUTH2_ACCESS_TOKEN="token123")
    def test_construct_with_access_token_config(self):
        client = predicthq.Client()
        assert client.access_token == "token123"


# New tests are intentionally left out of the ClientTest class because pytest does not support
# parametrized fixtures inside unittest.TestCase classes as documented at
# https://docs.pytest.org/en/stable/how-to/unittest.html#pytest-features-in-unittest-testcase-subclasses
# We should gradually migrate all tests to pytest style and remove unittest.TestCase classes


@pytest.fixture
def client():
    return predicthq.Client()


@pytest.mark.parametrize("status_code", (429, 503, 504))
@mock.patch("predicthq.client.requests.request")
def test_retries(mock_request, client, status_code):
    stamina.set_testing(True, attempts=3)  # Disable stamina backoff waiting so the tests can run faster

    mock_request.return_value.status_code = status_code
    mock_request.return_value.raise_for_status.side_effect = requests.HTTPError

    with pytest.raises(RetriableError):
        client.get("/get/")

    # Check that the request was retried 3 times
    mock_request.assert_has_calls(
        [
            mock.call("get", client.build_url("/get/"), headers=client.get_headers({})),
            mock.call().raise_for_status(),
            mock.call().json(),
        ]
        * 3
    )

    stamina.set_testing(False)  # Enable stamina backoff waiting after the test is done
