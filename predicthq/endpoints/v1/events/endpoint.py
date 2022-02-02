from predicthq.endpoints.base import UserBaseEndpoint
from predicthq.endpoints.decorators import accepts, returns
from .schemas import (
    SearchParams,
    EventResultSet,
    CountResultSet,
    CalendarParams,
    CalendarResultSet,
    ImpactParams,
    ImpactResultSet,
)


class EventsEndpoint(UserBaseEndpoint):
    @accepts(SearchParams)
    @returns(EventResultSet)
    def search(self, verify_ssl, **params):
        return self.client.get(
            self.build_url("v1", "events"),
            params=params,
            verify=verify_ssl,
        )

    @accepts(SearchParams)
    @returns(CountResultSet)
    def count(self, verify_ssl, **params):
        return self.client.get(
            self.build_url("v1", "events/count"),
            params=params,
            verify=verify_ssl,
        )

    @accepts(CalendarParams)
    @returns(CalendarResultSet)
    def calendar(self, verify_ssl, **params):
        return self.client.get(
            self.build_url("v1", "events/calendar"),
            params=params,
            verify=verify_ssl,
        )

    @accepts(ImpactParams)
    @returns(ImpactResultSet)
    def impact(self, verify_ssl, **params):
        return self.client.get(
            self.build_url("v1", "events/impact"),
            params=params,
            verify=verify_ssl,
        )
