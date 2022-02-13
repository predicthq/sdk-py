from predicthq.endpoints.base import UserBaseEndpoint
from predicthq.endpoints.decorators import accepts, returns
from .schemas import BroadcastResultSet, SearchParams


class BroadcastsEndpoint(UserBaseEndpoint):
    @accepts(SearchParams)
    @returns(BroadcastResultSet)
    def search(self, verify_ssl, **params):
        return self.client.get(
            self.build_url("v1", "broadcasts"),
            params=params,
            verify=verify_ssl,
        )
