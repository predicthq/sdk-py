# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

from schematics.transforms import blacklist, wholelist, whitelist

from predicthq.endpoints.schemas import Model, StringType, ListType, ModelType, DateTimeType, ResultSet, ResultType, SortableMixin, FloatType, IntType, DictType, \
    PaginatedMixin, DateTimeRange, StringListType, StringModelType, Area, BooleanType, DateType, Place


class SignalsSearchParams(SortableMixin, Model):

    class Options:
        serialize_when_none = False


class Dimension(Model):

    class Options:
        serialize_when_none = True
        roles = {
            "create": wholelist(),
            "update": wholelist()
        }

    name = StringType(required=True)
    type = StringType(choices=("category", "number", "date"), required=True)


class SignalID(Model):

    id = StringType(required=True)


class Signal(Model):

    class Options:
        serialize_when_none = True
        roles = {
            "create": whitelist("name", "country", "dimensions"),
            "update": blacklist("created_at", "updated_at")
        }

    id = StringType()
    name = StringType(required=True)
    country = StringType(max_length=2, min_length=2, required=True)
    dimensions = ListType(ModelType(Dimension), default=[])
    created_at = DateTimeType()
    updated_at = DateTimeType()

    def add_dimension(self, dimension_name, dimension_type):
        self.dimensions.append(Dimension({"name": dimension_name, "type": dimension_type}))

    def remove_dimension(self, dimension_name):
        self.dimensions = [dimension for dimension in self.dimensions if dimension.name != dimension_name]

    def save(self, endpoint=None):
        if endpoint is not None:
            self._endpoint = endpoint
        if self.id:
            return self._endpoint.update(self)
        else:
            return self._endpoint.create(self)

    def delete(self):
        self._endpoint.delete(id=self.id)

    def sink(self, data_points, chunk_size=1000):
        return self._endpoint.sink(id=self.id, data_points=data_points, chunk_size=chunk_size)

    def summary(self):
        return self._endpoint.dimensions(id=self.id)

    def analysis(self, **params):
        return self._endpoint.analysis(id=self.id, **params)


class NewSignal(Signal):

    class Options(Signal.Options):
        pass


class SavedSignal(SignalID, Signal):

    class Options(Signal.Options):
        pass


class SignalResultSet(ResultSet):

    results = ResultType(SavedSignal)


class DataPoint(Model):

    uid = StringType(required=True)
    date = DateTimeType(required=True)
    latitude = FloatType(min_value=-90, max_value=90, required=True)
    longitude = FloatType(min_value=-180, max_value=180, required=True)
    initiated = DateTimeType()
    completed = DateTimeType()
    # @todo: Support custom dimensions from signal


class SignalDataPoints(Model):

    id = StringType(required=True)
    data_points = ListType(ModelType(DataPoint), required=True)
    chunk_size = IntType(default=1000, max_value=5000, required=True)


class DateDimension(Model):

    type = StringType()
    count = IntType()
    min = DateTimeType()
    max = DateTimeType()


class GeoDimension(Model):

    type = StringType()
    bbox = ListType(FloatType)


class CategoryDimensionComponent(Model):

    name = StringType()
    count = IntType()


class CategoryDimension(Model):

    type = StringType()
    options = ListType(ModelType(CategoryDimensionComponent))


class NumberDimension(Model):

    type = StringType()
    count = IntType()
    min = IntType()
    max = IntType()
    avg = FloatType()
    std_deviation = FloatType()


class Dimensions(Model):

    date = ModelType(DateDimension)
    initiated = ModelType(DateDimension)
    completed = ModelType(DateDimension)
    location = ModelType(GeoDimension)
    # @todo: Support custom dimensions from signal


class DailyAnalysisDetailsComponent(Model):

    count = IntType()
    min = IntType()
    max = IntType()
    avg = FloatType()
    sum = IntType()
    sum_of_squares = IntType()
    variance = FloatType()
    std_deviation = FloatType()
    std_deviation_bounds = DictType(FloatType)
    percentiles = DictType(FloatType)


class DailyAnalysisDetails(Model):

    lead = ModelType(DailyAnalysisDetailsComponent)
    span = ModelType(DailyAnalysisDetailsComponent)


class DailyAnalysis(Model):

    date = DateType()
    trend = FloatType()
    actual = FloatType()
    expected = FloatType()
    excess = FloatType()
    details = ModelType(DailyAnalysisDetails)


class AnalysisResultSet(ResultSet):

    results = ResultType(DailyAnalysis)


class AnalysisParams(PaginatedMixin, SortableMixin, Model):

    class Options:
        serialize_when_none = False

    id = StringType(required=True)
    date = ModelType(DateTimeRange)
    initiated = ModelType(DateTimeRange)
    completed = ModelType(DateTimeRange)
    within = StringListType(StringModelType(Area), separator="+")
    significance = IntType(min_value=0, max_value=100)
    lead = BooleanType(default=False)
    span = BooleanType(default=False)
    place = ModelType(Place)

    # @todo: Support custom dimensions from signal
