from predicthq.endpoints.schemas import (
    GeoJSONPointType,
    Model,
    ResultSet,
    ResultType,
    StringType,
)


class Place(Model):

    id = StringType()
    type = StringType()
    name = StringType()
    county = StringType()
    region = StringType()
    country = StringType()
    country_alpha2 = StringType()
    country_alpha3 = StringType()
    location = GeoJSONPointType()


class PlaceResultSet(ResultSet):

    results = ResultType(Place)
