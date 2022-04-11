from datetime import date, datetime, time

import pytest
import pytz
from dateutil.parser import parse as parse_date

from predicthq.endpoints import decorators, schemas
from predicthq.endpoints.base import BaseEndpoint


def test_datetime_type():
    class SchemaExample(schemas.Model):

        my_datetime = schemas.DateTimeType()

    test_date = datetime(2016, 1, 1, tzinfo=pytz.UTC)
    assert SchemaExample({"my_datetime": "2016-01-01T00:00:00+00:00"}).my_datetime == test_date
    assert SchemaExample({"my_datetime": "2016-01-01T00:00:00+0000"}).my_datetime == test_date
    assert SchemaExample({"my_datetime": "2016-01-01T00:00:00Z"}).my_datetime == test_date
    assert SchemaExample({"my_datetime": test_date}).my_datetime == test_date


def test_date_or_datetime_type():
    class SchemaExample(schemas.Model):

        my_datetime = schemas.DateOrDateTimeType()

    test_date = date(2016, 1, 1)
    test_datetime = datetime(2016, 1, 1, 12, 30, 42, tzinfo=pytz.UTC)

    assert SchemaExample({"my_datetime": test_date}).my_datetime == test_date
    assert SchemaExample({"my_datetime": "2016-01-01"}).my_datetime == test_date
    assert SchemaExample({"my_datetime": "2016-01-01T12:30:42+00:00"}).my_datetime == test_datetime
    assert SchemaExample({"my_datetime": "2016-01-01T12:30:42+0000"}).my_datetime == test_datetime
    assert SchemaExample({"my_datetime": "2016-01-01T12:30:42Z"}).my_datetime == test_datetime
    assert SchemaExample({"my_datetime": test_datetime}).my_datetime == test_datetime


def test_date_type():
    class SchemaExample(schemas.Model):

        my_date = schemas.DateType()

    test_date = date(2016, 1, 1)
    assert SchemaExample({"my_date": "2016-01-01"}).my_date == test_date
    assert SchemaExample({"my_date": "2016-01-01T00:00:00+0000"}).my_date == test_date
    assert SchemaExample({"my_date": "2016-01-01T00:00:00Z"}).my_date == test_date
    assert SchemaExample({"my_date": test_date}).my_date == test_date


def test_string_model_and_string_model_type():
    class MyModel(schemas.StringModel):

        import_format = r"(?P<left>.*)==(?P<right>\d*)"
        export_format = "{left}=={right}"

        left = schemas.StringType()
        right = schemas.IntType()

    class SchemaExample(schemas.Model):

        my_model = schemas.StringModelType(MyModel)

    short_data = {"my_model": "ten==10"}
    long_data = {"my_model": {"left": "ten", "right": 10}}
    model_data = {"my_model": MyModel("ten==10")}
    invalid_data = {"my_model": "10==ten"}

    expected_data = {"my_model": "ten==10"}

    m = SchemaExample()

    assert m.import_data(short_data).to_primitive() == expected_data
    assert m.import_data(long_data).to_primitive() == expected_data
    assert m.import_data(model_data).to_primitive() == expected_data

    assert m.import_data(short_data).to_dict() == expected_data
    assert m.import_data(long_data).to_dict() == expected_data
    assert m.import_data(model_data).to_dict() == expected_data

    with pytest.raises(schemas.SchematicsDataError):
        m.import_data(invalid_data)


def test_string_list_type():
    class SchemaExample(schemas.Model):

        string_list = schemas.StringListType(schemas.StringType, separator="+")

    string_data = {"string_list": "a+b+c"}
    list_data = {
        "string_list": ["a", "b", "c"],
    }
    dict_data = {
        "string_list": ["a", "b", "c"],
    }

    expected_data = {"string_list": "a+b+c"}

    m = SchemaExample()
    assert m.import_data(string_data).to_primitive() == expected_data
    assert m.import_data(list_data).to_primitive() == expected_data
    assert m.import_data(dict_data).to_primitive() == expected_data

    unique_item_data = {"string_list": "a"}
    unique_item_dict_data = {
        "string_list": "a",
    }
    assert m.import_data(unique_item_data).to_primitive() == unique_item_data
    assert m.import_data(unique_item_dict_data).to_primitive() == unique_item_data


def test_list_type():
    class SchemaExample(schemas.Model):

        string_list = schemas.ListType(schemas.StringType)

    m = SchemaExample()
    assert m.import_data({"string_list": "string"}).to_primitive() == {"string_list": ["string"]}
    assert m.import_data({"string_list": ["string1", "string2"]}).to_primitive() == {
        "string_list": ["string1", "string2"]
    }


def test_geo_json_point_type():
    class SchemaExample(schemas.Model):

        point = schemas.GeoJSONPointType()

    m = SchemaExample()
    assert m.import_data({"point": [174.765742, -36.847585]}).to_primitive() == {"point": [174.765742, -36.847585]}

    with pytest.raises(schemas.SchematicsDataError):
        m.import_data({"point": [-36.847585, 174.765742]}, validate=True)


def test_date_around_type():
    class SchemaExample(schemas.Model):
        around = schemas.ModelType(schemas.DateAround)

    m = SchemaExample()

    assert m.import_data(
        {"around": {"origin": "2020-01-01", "offset": "1d", "scale": "0d", "decay": "0.1"}}
    ).to_primitive() == {"around": {"origin": "2020-01-01", "decay": 0.1, "scale": "0d", "offset": "1d"}}

    with pytest.raises(schemas.SchematicsDataError):
        m.import_data({"around": "2020-01-01"}, validate=True)


def test_location_around_type():
    class SchemaExample(schemas.Model):
        around = schemas.ModelType(schemas.LocationAround)

    m = SchemaExample()

    assert m.import_data(
        {"around": {"origin": "40.730610,-73.935242", "offset": "1km", "scale": "2km", "decay": "0.1"}}
    ).to_primitive() == {"around": {"origin": "40.730610,-73.935242", "decay": 0.1, "scale": "2km", "offset": "1km"}}

    with pytest.raises(schemas.SchematicsDataError):
        m.import_data({"around": "40.730610,-73.935242"}, validate=True)


def test_location_model():
    class SchemaExample(schemas.Model):

        location = schemas.StringModelType(schemas.Location)

    short_data = {"location": "@-36.847585,174.765742"}
    long_data = {"location": {"latitude": -36.847585, "longitude": 174.765742}}
    model_data = {"location": schemas.Location("@-36.847585,174.765742")}
    invalid_data = {"location": "-36.847585,174.765742"}

    expected_expected = {"location": "@-36.847585,174.765742"}

    m = SchemaExample()
    assert m.import_data(short_data).to_primitive() == expected_expected
    assert m.import_data(long_data).to_primitive() == expected_expected
    assert m.import_data(model_data).to_primitive() == expected_expected

    assert m.import_data(short_data).to_dict() == expected_expected
    assert m.import_data(long_data).to_dict() == expected_expected
    assert m.import_data(model_data).to_dict() == expected_expected

    with pytest.raises(schemas.SchematicsDataError):
        m.import_data(invalid_data)


def test_area_model():
    class SchemaExample(schemas.Model):

        area = schemas.StringModelType(schemas.Area)

    short_data = {"area": "10km@-36.847585,174.765742"}
    long_data = {"area": {"radius": "10km", "latitude": -36.847585, "longitude": 174.765742}}
    model_data = {"area": schemas.Area("10km@-36.847585,174.765742")}
    invalid_data = {"area": "10k@-36.847585,174.765742"}

    expected_expected = {"area": "10km@-36.847585,174.765742"}

    m = SchemaExample()
    assert m.import_data(short_data).to_primitive() == expected_expected
    assert m.import_data(long_data).to_primitive() == expected_expected
    assert m.import_data(model_data).to_primitive() == expected_expected

    assert m.import_data(short_data).to_dict() == expected_expected
    assert m.import_data(long_data).to_dict() == expected_expected
    assert m.import_data(model_data).to_dict() == expected_expected

    with pytest.raises(schemas.SchematicsDataError):
        m.import_data(invalid_data)


def test_resultset():
    class ResultExample(schemas.Model):

        value = schemas.IntType()

    class ResultSetExample(schemas.ResultSet):

        results = schemas.ResultType(ResultExample)

    class EndpointExample(BaseEndpoint):
        @decorators.returns(ResultSetExample)
        def load_page(self, page):
            page = int(page)
            return {
                "count": 9,
                "next": f"http://example.org/?page={page + 1}" if page < 3 else None,
                "previous": f"http://example.org/?page={page - 1}" if page > 1 else None,
                "results": [
                    {"value": 1 + (3 * (page - 1))},
                    {"value": 2 + (3 * (page - 1))},
                    {"value": 3 + (3 * (page - 1))},
                ],
            }

    endpoint = EndpointExample(None)

    p1 = endpoint.load_page(page=1)
    assert p1.count == 9
    assert list(p1) == [ResultExample({"value": 1}), ResultExample({"value": 2}), ResultExample({"value": 3})]
    assert p1.has_previous() is False
    assert p1.has_next() is True
    assert p1.get_previous() is None

    p2 = p1.get_next()

    assert list(p2) == [ResultExample({"value": 4}), ResultExample({"value": 5}), ResultExample({"value": 6})]
    assert p2.has_previous() is True
    assert p2.has_next() is True

    p3 = p2.get_next()
    assert list(p3) == [ResultExample({"value": 7}), ResultExample({"value": 8}), ResultExample({"value": 9})]
    assert p3.has_previous() is True
    assert p3.has_next() is False

    assert p3.get_next() is None
    assert list(p3.get_previous()) == list(p2)

    assert list(p1.iter_pages()) == [endpoint.load_page(page=2), endpoint.load_page(page=3)]
    assert list(p1.iter_all()) == list(p1) + list(p2) + list(p3)

    for item in p1.iter_all():
        assert item._endpoint == endpoint