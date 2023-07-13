from predicthq.endpoints.base import UserBaseEndpoint
from predicthq.endpoints.decorators import accepts, returns
from .schemas import (
    EventResultSet,
    CountResultSet,
    CalendarResultSet,
)


class EventsEndpoint(UserBaseEndpoint):
    @accepts()
    @returns(EventResultSet)
    def search(self, **params):
        verify_ssl = params.pop("config.verify_ssl", True)
        return self.client.get(
            self.build_url("v1", "events"),
            params=params,
            verify=verify_ssl,
        )

    @accepts()
    @returns(CountResultSet)
    def count(self, **params):
        verify_ssl = params.pop("config.verify_ssl", True)
        return self.client.get(
            self.build_url("v1", "events/count"),
            params=params,
            verify=verify_ssl,
        )

    @accepts()
    @returns(CalendarResultSet)
    def calendar(self, **params):
        verify_ssl = params.pop("config.verify_ssl", True)
        return self.client.get(
            self.build_url("v1", "events/calendar"),
            params=params,
            verify=verify_ssl,
        )
