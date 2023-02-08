from predicthq.endpoints.schemas import (
    ConfigMixin,
    FloatType,
    ListType,
    Model,
    ModelType,
    StringType,
)


class LocationParams(Model):
    class Options:
        serialize_when_none = False

    origin = StringType(regex=r"(-?\d+(\.\d+)?),(-?\d+(\.\d+)?)")


class SearchParams(ConfigMixin, Model):
    class Options:
        serialize_when_none = False

    location = ModelType(LocationParams, required=True)
    radius_unit = ListType(
        StringType(
            choices=(
                "km",
                "m",
                "mi",
                "ft",
            )
        )
    )
    industry = ListType(
        StringType(
            choices=(
                "parking",
                "restaurants",
                "retail",
                "accommodation",
            )
        )
    )


class LocationResult(Model):

    lat = FloatType(required=True)
    lon = FloatType(required=True)


class SuggestedRadiusResultSet(Model):

    radius = FloatType()
    radius_unit = StringType()
    location = ModelType(LocationResult)
