from predicthq.endpoints.base import BaseEndpoint
from predicthq.endpoints.decorators import accepts, returns
from .schemas import SearchParams, PlaceResultSet


class PlacesEndpoint(BaseEndpoint):
    @accepts(SearchParams)
    @returns(PlaceResultSet)
    def search(self, verify_ssl, **params):
        return self.client.get(
            self.build_url("v1", "places"),
            params=params,
            verify=verify_ssl,
        )
