# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

import re

import itertools

from datetime import datetime, date

from dateutil.parser import parse as parse_date
import six
import pytz

from schematics.models import Model
from schematics.transforms import Role
from schematics.types import StringType, DateTimeType as SchematicsDateTimeType, IntType, FloatType, URLType, GeoPointType, BooleanType, DateType as SchematicsDateType
from schematics.types.compound import ListType as SchematicsListType, ModelType, DictType
from schematics.exceptions import ValidationError as SchematicsValidationError, DataError as SchematicsDataError, ConversionError
from schematics.types.serializable import serializable



class DateTimeType(SchematicsDateTimeType):

    def to_native(self, value, context=None):
        if isinstance(value, datetime):
            return value
        return parse_date(value)


class DateType(SchematicsDateType):

    def to_native(self, value, context=None):
        if isinstance(value, date):
            return value
        return parse_date(value).date()


class StringModelType(ModelType):

    def _convert(self, value, context):
        if isinstance(value, six.string_types):
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
        if isinstance(raw_data, six.string_types):
            try:
                raw_data = re.match(self.import_format, six.text_type(raw_data)).groupdict()
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
        if isinstance(value, six.string_types):
            return value.split(self.separator)
        elif isinstance(value, dict):
            return [value]
        else:
            return super(StringListType, self)._coerce(value)

    def _export(self, *args, **kwargs):
        data = super(StringListType, self)._export(*args, **kwargs)
        return self.separator.join(map(six.text_type, data))


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

    radius = StringType(regex='\d+(k?m|ft|mi)', required=True)
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


class DateTimeRange(Model):

    class Options:
        serialize_when_none = False

    gt = DateTimeType()
    gte = DateTimeType()
    lt = DateTimeType()
    lte = DateTimeType()
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


class LimitMixin(Model):

    limit = IntType(min_value=1, max_value=200)


class OffsetMixin(Model):

    offset = IntType(min_value=0, max_value=50)


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
        return dict(six.moves.urllib.parse.parse_qsl(six.moves.urllib.parse.urlparse(url).query))

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
