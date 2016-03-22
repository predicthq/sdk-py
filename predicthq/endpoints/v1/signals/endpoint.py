# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

import json

import itertools

from predicthq.endpoints.base import UserBaseEndpoint
from predicthq.endpoints.decorators import returns, accepts
from predicthq.endpoints.v1.signals.schemas import SignalsSearchParams, AnalysisResultSet, AnalysisParams, Dimensions
from .schemas import Signal, SignalID, SavedSignal, SignalResultSet, SignalDataPoints


def chunks(iterator, size):
   iterable = iter(iterator)
   while True:
       yield itertools.chain([next(iterable)], itertools.islice(iterable, size - 1))


class SignalsEndpoint(UserBaseEndpoint):

    @accepts(SignalsSearchParams)
    @returns(SignalResultSet)
    def search(self, **params):
        return self.client.get(self.build_url('v1', 'signals'), params=params)

    @accepts(SignalID)
    @returns(SavedSignal)
    def get(self, id):
        return self.client.get(self.build_url('v1', 'signals/{}'.format(id)))

    @accepts(Signal, query_string=False, role="create")
    @returns(SavedSignal)
    def create(self, **data):
        return self.client.post(self.build_url('v1', 'signals'), json=data)

    @accepts(SavedSignal, query_string=False, role="update")
    @returns(SavedSignal)
    def update(self, id, **data):
        return self.client.put(self.build_url('v1', 'signals/{}'.format(id)), json=data)

    @accepts(SignalID)
    def delete(self, id):
        self.client.delete(self.build_url('v1', 'signals/{}'.format(id)))

    @accepts(SignalDataPoints, query_string=False)
    def sink(self, id, data_points, chunk_size):
        for data_chunk in chunks(data_points, chunk_size):
            data = "\n".join(json.dumps(item, indent=None) for item in data_chunk)
            self.client.post(self.build_url('v1', 'signals/{}/sink'.format(id)), data=data, headers={"Content-Type": "application/x-ldjson"})

    @accepts(SignalID)
    @returns(Dimensions)
    def dimensions(self, id):
        return self.client.get(self.build_url('v1', 'signals/{}/dimensions'.format(id)))

    @accepts(AnalysisParams)
    @returns(AnalysisResultSet)
    def analysis(self, id, **params):
        return self.client.get(self.build_url('v1', 'signals/{}/analysis'.format(id)), params=params)
