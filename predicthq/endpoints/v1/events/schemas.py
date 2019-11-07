# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

from predicthq.endpoints.schemas import (
    PaginatedMixin, SortableMixin, Model, ResultSet, ListType, StringType, GeoJSONPointType,
    StringListType, StringModelType, Area, ModelType, IntRange, IntType, DateTimeRange,
    DateTimeType, FloatType, ResultType, DictType, DateType, Place, DateAround,
    LocationAround, BooleanType, BrandUnsafe, Entity
)


class SearchParams(PaginatedMixin, SortableMixin, Model):

    class Options:
        serialize_when_none = False

    id = ListType(StringType)
    q = StringType()
    label = ListType(StringType)
    category = ListType(StringType)
    start = ModelType(DateTimeRange)
    start_around = ModelType(DateAround)
    end = ModelType(DateTimeRange)
    end_around = ModelType(DateAround)
    active = ModelType(DateTimeRange)
    updated = ModelType(DateTimeRange)
    state = StringType(choices=('active', 'deleted'))
    rank = ModelType(IntRange)
    rank_level = ListType(IntType(min_value=1, max_value=5))

    # `local_rank` and `aviation_rank` are paid features.
    # If you haven't subscribed to a paid feature, using it as a
    # search param will have no effect on your search results.
    local_rank = ModelType(IntRange)
    local_rank_level = ListType(IntType(min_value=1, max_value=5))
    aviation_rank = ModelType(IntRange)
    aviation_rank_level = ListType(IntType(min_value=1, max_value=5))

    country = ListType(StringType)
    location_around = ModelType(LocationAround)
    within = StringListType(StringModelType(Area), separator="+")
    place = ModelType(Place)
    relevance = ListType(StringType)
    brand_unsafe = ModelType(BrandUnsafe)
    entity = ModelType(Entity)


class Entities(Model):

    class Options:
        serialize_when_none = True

    entity_id = StringType()
    name = StringType()
    type = StringType()
    formatted_address = StringType()


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

    # `local_rank` and `aviation_rank` are paid features.
    # They will only show up in your response body if you
    # have subscribed to them.
    local_rank = IntType()
    aviation_rank = IntType()

    entities = ListType(ModelType(Entities))
    location = GeoJSONPointType()
    place_hierarchies = ListType(ListType(StringType()))
    scope = StringType()
    relevance = FloatType()
    state = StringType()
    first_seen = DateTimeType()
    updated = DateTimeType()
    deleted_reason = StringType()
    duplicate_of_id = StringType()


class EventResultSet(ResultSet):

    overflow = BooleanType()

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
