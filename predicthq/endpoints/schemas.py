import re
from datetime import datetime, date, time as dt_time
from urllib.parse import parse_qsl, urlparse

import pytz
from dateutil.parser import parse as parse_date

from schematics.exceptions import (
    ValidationError as SchematicsValidationError, DataError as SchematicsDataError, ConversionError
)
from schematics.models import Model
from schematics.transforms import Role
from schematics.types import (
    StringType, DateTimeType as SchematicsDateTimeType, IntType, FloatType, URLType, GeoPointType, BooleanType,
    DateType as SchematicsDateType
)
from schematics.types.compound import ListType as SchematicsListType, ModelType, DictType
from schematics.types.serializable import serializable


class DateTimeType(SchematicsDateTimeType):

    def to_native(self, value, context=None):
        if isinstance(value, datetime):
            return value
        return parse_date(value)


class DateTimeEndType(SchematicsDateTimeType):

    def to_native(self, value, context=None):
        if isinstance(value, datetime):
            return value
        return datetime.combine(parse_date(value), dt_time.max)


class DateType(SchematicsDateType):

    def to_native(self, value, context=None):
        if isinstance(value, date):
            return value
        return parse_date(value).date()


class StringModelType(ModelType):

    def _convert(self, value, context):
        if isinstance(value, str):
            return self.model_class._convert(value, context=context)
        else:
            return super(StringModelType, self)._convert(value, context=context)


class StringModel(Model):

    @property
    def import_format(self):  # pragma: nocover
        raise NotImplementedError()

    @property
    def export_format(self):  # pragma: nocover
        raise NotImplementedError()

    def convert(self, raw_data, **kw):
        if isinstance(raw_data, str):
            try:
                raw_data = re.match(self.import_format, str(raw_data)).groupdict()
            except AttributeError:
                raise SchematicsValidationError("'{}' is not a valid format for {}".format(raw_data, self.__class__.__name__))
        return super(StringModel, self).convert(raw_data, **kw)

    def export(self, *args, **kwargs):
        return self.export_format.format(**super(StringModel, self).export(*args, **kwargs))


class StringListType(SchematicsListType):

    def __init__(self, field, separator=" ", **kwargs):
        self.separator = separator
        super(StringListType, self).__init__(field, **kwargs)

    def _coerce(self, value):
        if isinstance(value, str):
            return value.split(self.separator)
        elif isinstance(value, dict):
            return [value]
        else:
            return super(StringListType, self)._coerce(value)

    def _export(self, *args, **kwargs):
        data = super(StringListType, self)._export(*args, **kwargs)
        return self.separator.join(map(str, data))


class ListType(SchematicsListType):

    def _coerce(self, value):
        if not isinstance(value, (list, tuple)):
            return [value]
        else:
            return super(ListType, self)._coerce(value)


class GeoJSONPointType(GeoPointType):

    def _normalize(self, value):
        return tuple(reversed(super(GeoJSONPointType, self)._normalize(value)))


class Area(StringModel):

    import_format = r'(?P<radius>\d+(k?m|ft|mi))@(?P<latitude>-?\d+(\.\d+)?),(?P<longitude>-?\d+(\.\d+)?)'
    export_format = "{radius}@{latitude},{longitude}"

    radius = StringType(regex=r'\d+(k?m|ft|mi)', required=True)
    latitude = FloatType(required=True)
    longitude = FloatType(required=True)


class Location(StringModel):

    import_format = r'@(?P<latitude>-?\d+(\.\d+)?),(?P<longitude>-?\d+(\.\d+)?)'
    export_format = "@{latitude},{longitude}"

    latitude = FloatType(required=True)
    longitude = FloatType(required=True)


class Place(Model):

    class Options:
        serialize_when_none = False

    scope = ListType(StringType)
    exact = ListType(StringType)


class DateAround(Model):

    class Options:
        serialize_when_none = False

    origin = DateType(required=True)
    offset = StringType(regex=r'\d+d')
    scale = StringType(regex=r'\d+d')
    decay = FloatType()


class LocationAround(Model):

    class Options:
        serialize_when_none = False

    origin = StringType(regex=r'(-?\d+(\.\d+)?),(-?\d+(\.\d+)?)', required=True)
    offset = StringType(regex=r'\d+(\.\d+)?(cm|m|km|in|ft|mi)')
    scale = StringType(regex=r'\d+(\.\d+)?(cm|m|km|in|ft|mi)')
    decay = FloatType()


class DateTimeRange(Model):

    class Options:
        serialize_when_none = False

    gt = DateTimeType()
    gte = DateTimeType()
    lt = DateTimeEndType()
    lte = DateTimeEndType()
    tz = StringType(choices=pytz.all_timezones)


class FloatRange(Model):

    class Options:
        serialize_when_none = False

    gt = FloatType()
    gte = FloatType()
    lt = FloatType()
    lte = FloatType()


class IntRange(Model):

    class Options:
        serialize_when_none = False

    gt = IntType()
    gte = IntType()
    lt = IntType()
    lte = IntType()


class BrandUnsafe(Model):

    class Options:
        serialize_when_none = False

    exclude = BooleanType()


class Entity(Model):

    class Options:
        serialize_when_none = False

    id = StringType()


class LimitMixin(Model):

    limit = IntType(min_value=1)


class OffsetMixin(Model):

    offset = IntType(min_value=0)


class PaginatedMixin(LimitMixin, OffsetMixin):

    pass


class SortableMixin(Model):

    sort = ListType(StringType())


class ResultSet(Model):

    count = IntType()
    previous = URLType()
    next = URLType()

    @property
    def results(self):  # pragma: nocover
        raise NotImplementedError()

    def _parse_params(self, url):
        return dict(parse_qsl(urlparse(url).query))

    def has_previous(self):
        return self.previous is not None

    def has_next(self):
        return self.next is not None

    def get_next(self):
        if not self.has_next() or not hasattr(self, '_more'):
            return
        params = self._parse_params(self.next)
        return self._more(**params)

    def get_previous(self):
        if not self.has_previous() or not hasattr(self, '_more'):
            return
        params = self._parse_params(self.previous)
        return self._more(**params)

    def iter_pages(self):
        next_page = self
        while next_page.has_next():
            next_page = next_page.get_next()
            yield next_page

    def iter_items(self):
        return iter(self.results)

    def iter_all(self):
        for item in self.iter_items():
            yield item
        for page in self.iter_pages():
            for item in page.iter_items():
                yield item

    def __iter__(self):
        return self.iter_items()


class ResultType(SchematicsListType):

    def __init__(self, field, *args, **kwargs):
        super(ResultType, self).__init__(ModelType(field), *args, **kwargs)
