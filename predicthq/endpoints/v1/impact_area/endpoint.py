from predicthq.endpoints.base import BaseEndpoint
from predicthq.endpoints.decorators import accepts, returns
from .schemas import ImpactAreaResultSet


class ImpactAreaEndpoint(BaseEndpoint):
    @accepts()
    @returns(ImpactAreaResultSet)
    def search(self, **params):
        verify_ssl = params.pop("config.verify_ssl", True)
        return self.client.get(
            self.build_url("v1", "impact-area"),
            params=params,
            verify=verify_ssl,
        )
