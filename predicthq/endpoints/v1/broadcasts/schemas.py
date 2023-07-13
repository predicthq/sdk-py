from predicthq.endpoints.schemas import (
    BooleanType,
    DateTimeType,
    FloatType,
    IntType,
    ListType,
    Model,
    ModelType,
    ResultSet,
    ResultType,
    StringType,
)


class GeoPoint(Model):

    lat = FloatType()
    lon = FloatType()


class BroadcastEventEntities(Model):
    class Options:
        serialize_when_none = False

    entity_id = StringType()
    type = StringType()
    name = StringType()
    formatted_address = StringType()


class BroadcastEventLocation(Model):
    class Options:
        serialize_when_none = False

    geopoint = ModelType(GeoPoint)
    place_hierarchies = ListType(ListType(StringType))
    country = StringType()


class BroadcastEventDates(Model):
    class Options:
        serialize_when_none = False

    start = DateTimeType()
    end = DateTimeType()
    start_local = DateTimeType()
    end_local = DateTimeType()
    timezone = StringType()

    # predicted_end_local is a paid feature.
    # It will only show up in your response body if you
    # have subscribed to it.
    predicted_end_local = DateTimeType()


class BroadcastEvent(Model):
    class Options:
        serialize_when_none = False

    event_id = StringType()
    title = StringType()
    category = StringType()
    labels = ListType(StringType)
    dates = ModelType(BroadcastEventDates)
    location = ModelType(BroadcastEventLocation)
    entities = ListType(ModelType(BroadcastEventEntities))

    # The following fields are paid features.
    # They will only show up in your response body if you
    # have subscribed to them.
    phq_attendance = IntType()
    phq_rank = IntType()
    local_rank = IntType()
    aviation_rank = IntType()


class Place(Model):
    class Options:
        serialize_when_none = False

    place_id = StringType()
    type = StringType()
    name = StringType()
    county = StringType()
    region = StringType()
    country = StringType()


class BroadcastLocation(Model):
    class Options:
        serialize_when_none = False

    geopoint = ModelType(GeoPoint)
    place_hierarchies = ListType(ListType(StringType))
    places = ListType(ModelType(Place))
    country = StringType()


class BroadcastDates(Model):
    class Options:
        serialize_when_none = False

    start = DateTimeType()
    start_local = DateTimeType()
    timezone = StringType()


class Broadcast(Model):
    class Options:
        serialize_when_none = False

    broadcast_id = StringType()
    updated = DateTimeType()
    first_seen = DateTimeType()
    dates = ModelType(BroadcastDates)
    location = ModelType(BroadcastLocation)
    phq_viewership = IntType()
    record_status = StringType()
    broadcast_status = StringType()
    event = ModelType(BroadcastEvent)


class BroadcastResultSet(ResultSet):

    overflow = BooleanType()
    results = ResultType(Broadcast)
