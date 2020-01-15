from predicthq.endpoints.base import UserBaseEndpoint
from predicthq.endpoints.decorators import accepts, returns
from .schemas import (
    SearchParams, EventResultSet, CountResultSet, CalendarParams, CalendarResultSet,
    ImpactParams, ImpactResultSet
)


class EventsEndpoint(UserBaseEndpoint):

    @accepts(SearchParams)
    @returns(EventResultSet)
    def search(self, **params):
        return self.client.get(self.build_url('v1', 'events'), params=params)

    @accepts(SearchParams)
    @returns(CountResultSet)
    def count(self, **params):
        return self.client.get(self.build_url('v1', 'events/count'), params=params)

    @accepts(CalendarParams)
    @returns(CalendarResultSet)
    def calendar(self, **params):
        return self.client.get(self.build_url('v1', 'events/calendar'), params=params)

    @accepts(ImpactParams)
    @returns(ImpactResultSet)
    def impact(self, **params):
        return self.client.get(self.build_url('v1', 'events/impact'), params=params)
