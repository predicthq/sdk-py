import unittest

from predicthq.endpoints.v1.accounts.schemas import Account
from tests import load_fixture, with_mock_client, with_mock_responses, with_client


class AccountsTest(unittest.TestCase):
    @with_mock_client(request_returns=load_fixture("requests_responses/accounts_test/test_self")[0]["body"])
    def test_self_params(self, client):
        client.accounts.self()
        client.request.assert_called_once_with("get", "/v1/accounts/self/")

    @with_client()
    @with_mock_responses()
    def test_self(self, client, responses):
        account = client.accounts.self()
        assert isinstance(account, Account)

    class AccountsTest(unittest.TestCase):
        @with_mock_client(request_returns=load_fixture("requests_responses/accounts_test/test_self")[0]["body"])
        def test_self_params(self, client):
            client.accounts.self()
            client.request.assert_called_once_with("get", "/v1/accounts/self/")

        @with_client()
        @with_mock_responses()
        def test_self(self, client, responses):
            account = client.accounts.self()
            assert isinstance(account, Account)

    def test_accounts_endpoint_deprecation_warning(self):
        from predicthq.endpoints.v1.accounts.endpoint import AccountsEndpoint

        expected_text = (
            "The Accounts endpoint in the SDK is deprecated and will be removed in future releases. "
            "Account information can be managed via the PredictHQ dashboard."
        )
        import warnings

        endpoint = AccountsEndpoint(client=None)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                endpoint.self()
            except Exception:
                pass  # Ignore errors due to None client
            assert any(
                issubclass(warning.category, FutureWarning) and expected_text in str(warning.message) for warning in w
            )
