# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

from predicthq.schemas import PaginatedMixin, SortableMixin, Model, ResultSet, ListType, StringType, \
                              GeoJSONPointType, StringListType, StringModelType, Area, ModelType, IntRange, \
                              IntType, DateRange, DateTimeType, FloatType, ResultType


class SearchParams(PaginatedMixin, SortableMixin, Model):

    class Options:
        serialize_when_none = False

    id = ListType(StringType)
    q = StringType()
    label = ListType(StringType)
    category = ListType(StringType)
    start = ModelType(DateRange)
    end = ModelType(DateRange)
    rank_level = ListType(IntType(min_value=1, max_value=5))
    rank = ModelType(IntRange)
    country = ListType(StringType)
    within = StringListType(StringModelType(Area), separator="+")


class Event(Model):

    class Options:
        serialize_when_none = True

    id = StringType()
    title = StringType()
    description = StringType()
    start = DateTimeType()
    end = DateTimeType()
    timezone = StringType()
    duration = IntType()
    category = StringType()
    labels = ListType(StringType())
    country = StringType()
    rank = IntType()
    location = GeoJSONPointType()
    scope = StringType()
    relevance = FloatType()


class EventResultSet(ResultSet):

    results = ResultType(Event)
