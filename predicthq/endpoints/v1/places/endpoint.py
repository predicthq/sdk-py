from predicthq.endpoints.base import BaseEndpoint
from predicthq.endpoints.decorators import accepts, returns
from .schemas import PlaceResultSet


class PlacesEndpoint(BaseEndpoint):
    @accepts()
    @returns(PlaceResultSet)
    def search(self, **params):
        verify_ssl = params.pop("config.verify_ssl", True)
        return self.client.get(
            self.build_url("v1", "places"),
            params=params,
            verify=verify_ssl,
        )
