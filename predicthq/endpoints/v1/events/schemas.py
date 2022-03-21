from predicthq.endpoints.schemas import (
    Area,
    BooleanType,
    BrandUnsafe,
    ConfigMixin,
    DateAround,
    DateTimeRange,
    DateTimeType,
    DateType,
    DictType,
    Entity,
    FloatType,
    GeoJSONPointType,
    IntRange,
    IntType,
    ListType,
    LocationAround,
    Model,
    ModelType,
    PaginatedMixin,
    Place,
    PolyModelType,
    ResultSet,
    ResultType,
    SortableMixin,
    StringListType,
    StringModelType,
    StringType,
)
from schematics.common import NONEMPTY


class SearchParams(PaginatedMixin, SortableMixin, ConfigMixin, Model):
    class Options:
        serialize_when_none = False

    active = ModelType(DateTimeRange)
    cancelled = ModelType(DateTimeRange)
    category = ListType(StringType)
    country = ListType(StringType)
    deleted_reason = ListType(StringType(choices=("cancelled", "duplicate", "invalid", "postponed")))
    end = ModelType(DateTimeRange)
    end_around = ModelType(DateAround)
    id = ListType(StringType)
    label = ListType(StringType)
    location_around = ModelType(LocationAround)
    place = ModelType(Place)
    postponed = ModelType(DateTimeRange)
    q = StringType()
    relevance = ListType(StringType)
    start = ModelType(DateTimeRange)
    start_around = ModelType(DateAround)
    state = ListType(StringType(choices=("active", "deleted"), default="active"))
    updated = ModelType(DateTimeRange)
    within = StringListType(StringModelType(Area), separator="+")

    # The below parameters are only available if they are enabled in your plan.
    # If you are not subscribed to a feature, using the parameter will have no
    # effect on your search results.
    aviation_rank = ModelType(IntRange)
    aviation_rank_level = ListType(IntType(min_value=1, max_value=5))
    brand_unsafe = ModelType(BrandUnsafe)
    entity = ModelType(Entity)
    local_rank = ModelType(IntRange)
    local_rank_level = ListType(IntType(min_value=1, max_value=5))
    phq_attendance = ModelType(IntRange)
    predicted_end = ModelType(DateTimeRange)
    rank = ModelType(IntRange)
    rank_level = ListType(IntType(min_value=1, max_value=5))


class Entities(Model):
    class Options:
        serialize_when_none = True

    entity_id = StringType()
    name = StringType()
    type = StringType()
    formatted_address = StringType()


class Point(Model):

    type = StringType()
    coordinates = ListType(FloatType())

    @classmethod
    def _claim_polymorphic(cls, data):
        return data.get("type") in ["Point"]


class MultiPoint(Model):

    type = StringType()
    coordinates = ListType(ListType(FloatType()))

    @classmethod
    def _claim_polymorphic(cls, data):
        return data.get("type") in ["MultiPoint", "LineString"]


class Polygon(Model):

    type = StringType()
    coordinates = ListType(ListType(ListType(FloatType())))

    @classmethod
    def _claim_polymorphic(cls, data):
        return data.get("type") in ["MultiLineString", "Polygon"]


class MultiPolygon(Model):

    type = StringType()
    coordinates = ListType(ListType(ListType(ListType(FloatType()))))

    @classmethod
    def _claim_polymorphic(cls, data):
        return data.get("type") in ["MultiPolygon"]


class Geo(Model):

    geometry = PolyModelType(model_spec=[Point, MultiPoint, Polygon, MultiPolygon])


class ParentEvent(Model):

    parent_event_id = StringType()


class ImpactPatternImpacts(Model):

    date_local = DateType()
    value = IntType()
    position = StringType()


class ImpactPattern(Model):

    vertical = StringType()
    impact_type = StringType()
    impacts = ListType(ModelType(ImpactPatternImpacts))


class Event(Model):
    class Options:
        serialize_when_none = True

    cancelled = DateTimeType()
    category = StringType()
    country = StringType()
    deleted_reason = StringType()
    description = StringType()
    duplicate_of_id = StringType()
    duration = IntType()
    end = DateTimeType()
    first_seen = DateTimeType()
    geo = ModelType(Geo)
    id = StringType()
    impact_patterns = ListType(ModelType(ImpactPattern))
    labels = ListType(StringType())
    location = GeoJSONPointType()
    parent_event = ModelType(ParentEvent)
    place_hierarchies = ListType(ListType(StringType()))
    postponed = DateTimeType()
    relevance = FloatType()
    scope = StringType()
    start = DateTimeType()
    state = StringType()
    timezone = StringType()
    title = StringType()
    updated = DateTimeType()

    # The below fields are only available if they are enabled in your plan.
    aviation_rank = IntType()  # Aviation Rank add-on
    brand_safe = BooleanType()
    entities = ListType(ModelType(Entities))  # Venues and addresses add-on
    local_rank = IntType()  # Local Rank add-on
    phq_attendance = IntType()  # PHQ Attendance add-on
    predicted_end = DateTimeType()
    private = BooleanType()  # Loop add-on
    rank = IntType()  # PHQ Rank add-on


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
