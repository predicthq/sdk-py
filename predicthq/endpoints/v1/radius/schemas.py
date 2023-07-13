from predicthq.endpoints.schemas import (
    FloatType,
    Model,
    ModelType,
    StringType,
)


class LocationResult(Model):

    lat = FloatType(required=True)
    lon = FloatType(required=True)


class SuggestedRadiusResultSet(Model):

    radius = FloatType()
    radius_unit = StringType()
    location = ModelType(LocationResult)
