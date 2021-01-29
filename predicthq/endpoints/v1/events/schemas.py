from schematics.common import NONEMPTY

from predicthq.endpoints.schemas import (
    PaginatedMixin, SortableMixin, Model, ResultSet, ListType, StringType, GeoJSONPointType,
    StringListType, StringModelType, Area, ModelType, IntRange, IntType, DateTimeRange,
    DateTimeType, FloatType, ResultType, DictType, DateType, Place, DateAround,
    LocationAround, BooleanType, BrandUnsafe, Entity
)


class SearchParams(PaginatedMixin, SortableMixin, Model):

    class Options:
        serialize_when_none = False

    active = ModelType(DateTimeRange)
    brand_unsafe = ModelType(BrandUnsafe)
    category = ListType(StringType)
    country = ListType(StringType)
    deleted_reason = StringType(choices=('cancelled', 'duplicate', 'invalid', 'postponed'))
    end = ModelType(DateTimeRange)
    end_around = ModelType(DateAround)
    entity = ModelType(Entity)
    id = ListType(StringType)
    label = ListType(StringType)
    location_around = ModelType(LocationAround)
    place = ModelType(Place)
    q = StringType()
    rank = ModelType(IntRange)
    rank_level = ListType(IntType(min_value=1, max_value=5))
    relevance = ListType(StringType)
    start = ModelType(DateTimeRange)
    start_around = ModelType(DateAround)
    state = StringType(choices=('active', 'deleted'))
    updated = ModelType(DateTimeRange)
    within = StringListType(StringModelType(Area), separator="+")

    # `aviation_rank`, `local_rank`, `phq_attendance` are
    # paid features. If you haven't subscribed to a paid feature, using it
    # as a search param will have no effect on your search results.
    aviation_rank = ModelType(IntRange)
    aviation_rank_level = ListType(IntType(min_value=1, max_value=5))
    local_rank = ModelType(IntRange)
    local_rank_level = ListType(IntType(min_value=1, max_value=5))
    phq_attendance = ModelType(IntRange)


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

    category = StringType()
    country = StringType()
    deleted_reason = StringType()
    description = StringType()
    duplicate_of_id = StringType()
    duration = IntType()
    end = DateTimeType()
    entities = ListType(ModelType(Entities))
    first_seen = DateTimeType()
    id = StringType()
    labels = ListType(StringType())
    location = GeoJSONPointType()
    place_hierarchies = ListType(ListType(StringType()))
    rank = IntType()
    relevance = FloatType()
    scope = StringType()
    start = DateTimeType()
    state = StringType()
    timezone = StringType()
    title = StringType()
    updated = DateTimeType()

    # `aviation_rank`, `local_rank`, `phq_attendance` are
    # paid features. They will only show up in your response body if you have
    # subscribed to them.
    aviation_rank = IntType()
    local_rank = IntType()
    phq_attendance = IntType()


class EventResultSet(ResultSet):

    overflow = BooleanType()

    results = ResultType(Event)


class CountResultSet(Model):

    count = IntType()
    top_rank = FloatType()
    rank_levels = DictType(IntType)
    categories = DictType(IntType)
    labels = DictType(IntType)


class TopEventsSearchParams(SortableMixin, Model):

    limit = IntType(min_value=0, max_value=10)


class CalendarParams(SearchParams):

    top_events = ModelType(TopEventsSearchParams)


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


class ImpactParams(SearchParams):

    top_events = ModelType(TopEventsSearchParams)
    impact_rank = StringType(choices=('rank', 'aviation_rank'))


class ImpactDay(Model):

    date = DateType()
    count = IntType()
    impact = IntType()

    rank_levels = DictType(IntType, export_level=NONEMPTY)
    rank_levels_impact = DictType(IntType, export_level=NONEMPTY)

    aviation_rank_levels = DictType(IntType, export_level=NONEMPTY)
    aviation_rank_levels_impact = DictType(IntType, export_level=NONEMPTY)

    categories = DictType(IntType)
    categories_impact = DictType(IntType)


class ImpactResultSet(ResultSet):

    results = ResultType(ImpactDay)
