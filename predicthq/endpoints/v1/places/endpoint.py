# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

from predicthq.endpoints.base import BaseEndpoint
from predicthq.endpoints.decorators import accepts, returns
from .schemas import SearchParams, PlaceResultSet


class PlacesEndpoint(BaseEndpoint):

    @accepts(SearchParams)
    @returns(PlaceResultSet)
    def search(self, **params):
        return self.client.get(self.build_url('v1', 'places'), params=params)
