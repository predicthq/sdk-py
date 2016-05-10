# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

from predicthq.endpoints.schemas import PaginatedMixin, SortableMixin, Model, ResultSet, \
    ListType, StringType, GeoJSONPointType, StringListType, StringModelType, Area, \
    ModelType, IntRange, IntType, DateTimeRange, DateTimeType, FloatType, ResultType, \
    DictType, DateType, Place


class SearchParams(PaginatedMixin, SortableMixin, Model):

    class Options:
        serialize_when_none = False

    id = ListType(StringType)
    q = StringType()
    label = ListType(StringType)
    category = ListType(StringType)
    start = ModelType(DateTimeRange)
    end = ModelType(DateTimeRange)
    active = ModelType(DateTimeRange)
    rank_level = ListType(IntType(min_value=1, max_value=5))
    rank = ModelType(IntRange)
    country = ListType(StringType)
    within = StringListType(StringModelType(Area), separator="+")
    place = ModelType(Place)


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


class Count(Model):

    count = IntType()
    top_rank = FloatType()
    rank_levels = DictType(IntType)
    categories = DictType(IntType)
    labels = DictType(IntType)


class TopEventsSearchParams(SortableMixin, Model):

    limit = IntType(min_value=0, max_value=10)


class CalendarParams(SearchParams):

    top_events = ModelType(TopEventsSearchParams)
    view = StringType(choices=('active', 'start'))


class CalendarDay(Model):

    date = DateType()
    count = IntType()
    top_rank = FloatType()
    rank_levels = DictType(IntType)
    categories = DictType(IntType)
    labels = DictType(IntType)
    top_events = ModelType(EventResultSet)


class CalendarResultSet(ResultSet):

    results = ResultType(CalendarDay)
