import unittest

from predicthq.endpoints.v1.accounts.schemas import Account
from tests import with_mock_client, with_mock_responses, with_client


class AccountsTest(unittest.TestCase):

    @with_mock_client()
    def test_self_params(self, client):
        client.accounts.self()
        client.request.assert_called_once_with('get', '/v1/accounts/self/')

    @with_client()
    @with_mock_responses()
    def test_self(self, client, responses):
        account = client.accounts.self()
        assert isinstance(account, Account)
