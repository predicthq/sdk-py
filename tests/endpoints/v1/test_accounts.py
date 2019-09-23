# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

import unittest

from tests import with_mock_client, with_mock_responses, with_client

from predicthq.endpoints.v1.accounts.schemas import Account


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
