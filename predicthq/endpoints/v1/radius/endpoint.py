from predicthq.endpoints.base import BaseEndpoint
from predicthq.endpoints.decorators import accepts, returns
from .schemas import SuggestedRadiusResultSet


class SuggestedRadiusEndpoint(BaseEndpoint):
    @accepts()
    @returns(SuggestedRadiusResultSet)
    def search(self, **params):
        verify_ssl = params.pop("config.verify_ssl", True)
        return self.client.get(
            self.build_url("v1", "suggested-radius"),
            params=params,
            verify=verify_ssl,
        )
