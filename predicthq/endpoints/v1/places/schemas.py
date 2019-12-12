from predicthq.endpoints.schemas import (
    LimitMixin, Model, ResultSet, ListType, StringType, GeoJSONPointType, StringListType,
    StringModelType, Location, DateTimeType, ResultType, SchematicsValidationError
)


class SearchParams(LimitMixin, Model):

    class Options:
        serialize_when_none = False

    q = StringType()
    id = ListType(StringType)
    location = StringListType(StringModelType(Location), separator="+")
    country = ListType(StringType)
    type = ListType(StringType(choices=('planet', 'continent', 'country', 'region', 'county', 'local', 'major', 'metro', 'all')))

    def validate(self, *args, **kwargs):
        super(SearchParams, self).validate(*args, **kwargs)
        if not any((self.q, self.id, self.location, self.country)):
            raise SchematicsValidationError("Places search requires one of q, id, location or country")


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
