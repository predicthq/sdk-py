# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

from predicthq.endpoints.base import UserBaseEndpoint
from predicthq.endpoints.decorators import accepts, returns
from .schemas import SearchParams, EventResultSet, Count, CalendarParams, CalendarResultSet


class EventsEndpoint(UserBaseEndpoint):

    @accepts(SearchParams)
    @returns(EventResultSet)
    def search(self, **params):
        return self.client.get(self.build_url('v1', 'events'), params=params)

    @accepts(SearchParams)
    @returns(Count)
    def count(self, **params):
        return self.client.get(self.build_url('v1', 'events/count'), params=params)

    @accepts(CalendarParams)
    @returns(CalendarResultSet)
    def calendar(self, **params):
        return self.client.get(self.build_url('v1', 'events/calendar'), params=params)
