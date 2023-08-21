import unittest

from predicthq.endpoints.v1.accounts.schemas import Account
from tests import load_fixture, with_mock_client, with_mock_responses, with_client


class AccountsTest(unittest.TestCase):
    @with_mock_client(
        request_returns=load_fixture("requests_responses/accounts_test/test_self")[0]["body"]
    )
    def test_self_params(self, client):
        client.accounts.self()
        client.request.assert_called_once_with("get", "/v1/accounts/self/")

    @with_client()
    @with_mock_responses()
    def test_self(self, client, responses):
        account = client.accounts.self()
        assert isinstance(account, Account)
