from predicthq.endpoints.base import BaseEndpoint
from predicthq.endpoints.decorators import returns
from .schemas import Account


class AccountsEndpoint(BaseEndpoint):

    @returns(Account)
    def self(self):
        return self.client.get(self.build_url('v1', 'accounts/self'))
