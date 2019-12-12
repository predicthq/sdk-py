import pytest

from predicthq.endpoints import decorators, schemas
from predicthq.endpoints.base import BaseEndpoint
from predicthq.exceptions import ValidationError


def test_to_params():
    kwargs = {"string_type": "my-string", "list_type": [1, 2, 3], "dict_type": {"key1": "val1", "key2": "val2"}, "bool_type": True}
    expected = {'string_type': 'my-string', 'list_type': '1,2,3', 'dict_type.key1': u'val1', 'dict_type.key2': 'val2', 'bool_type': 1}
    assert decorators._to_url_params(kwargs) == expected


def test_kwargs_processor():
    kwargs = {"normal_arg": "value", "nested__arg": "value"}
    expected = {'normal_arg': 'value', 'nested': {'arg': 'value'}}
    assert decorators._process_kwargs(kwargs) == expected


def test_accepts():

    class SchemaExample(schemas.Model):
        arg1 = schemas.StringType(required=True)
        arg2 = schemas.ListType(schemas.IntType)

    class EndpointExample(BaseEndpoint):

        @decorators.accepts(SchemaExample)
        def func(self, **kwargs):
            return kwargs

    endpoint = EndpointExample(None)
    assert endpoint.func(arg1="test", arg2=[1, 2]) == {'arg1': 'test', 'arg2': '1,2'}

    assert endpoint.func(SchemaExample({"arg1": "test", "arg2": [1, 2]})) == {'arg1': 'test', 'arg2': '1,2'}

    assert endpoint.func({"arg1": "test", "arg2": [1, 2]}) == {'arg1': 'test', 'arg2': '1,2'}

    with pytest.raises(ValidationError):
        endpoint.func(arg2=[1, 2])

    with pytest.raises(ValidationError):
        endpoint.func(arg1="value", arg2="invalid")


def test_accepts_for_body_use():

    class SchemaExample(schemas.Model):
        arg1 = schemas.StringType(required=True)
        arg2 = schemas.ListType(schemas.IntType)

    class EndpointExample(BaseEndpoint):

        @decorators.accepts(SchemaExample, query_string=False)
        def func(self, **kwargs):
            return kwargs

    endpoint = EndpointExample(None)
    assert endpoint.func({"arg1": "test", "arg2": [1, 2]}) == {'arg1': 'test', 'arg2': [1, 2]}


def test_returns():

    class SchemaExample(schemas.Model):
        arg1 = schemas.StringType(required=True)
        arg2 = schemas.ListType(schemas.IntType)

    class EndpointExample(BaseEndpoint):

        @decorators.returns(SchemaExample)
        def func(self, **kwargs):
            return kwargs

    endpoint = EndpointExample(None)
    assert endpoint.func(arg1="test", arg2=[1, 2]) == SchemaExample({'arg1': 'test', 'arg2': [1, 2]})

    with pytest.raises(ValidationError):
        endpoint.func(arg2=[1, 2])

    with pytest.raises(ValidationError):
        endpoint.func(arg1="value", arg2="invalid")


def test_returns_resultset_of_native_types():

    class SchemaExample(schemas.ResultSet):

        results = schemas.ListType(schemas.StringType)

    class EndpointExample(BaseEndpoint):

        @decorators.returns(SchemaExample)
        def func(self, **kwargs):
            return kwargs

    endpoint = EndpointExample(None)
    assert endpoint.func(results=["item1", "item2"]) == SchemaExample({"results": ["item1", "item2"]})
    assert endpoint.func()._more(results=["item3", "item4"]) == SchemaExample({'results': ['item3', 'item4']})
    assert endpoint == endpoint.func()._endpoint


def test_returns_resultset_of_models():

    class ModelExample(schemas.ResultSet):

        name = schemas.StringType()

    class SchemaExample(schemas.ResultSet):

        results = schemas.ResultType(ModelExample)

    class EndpointExample(BaseEndpoint):

        @decorators.returns(SchemaExample)
        def func(self, **kwargs):
            return kwargs

    endpoint = EndpointExample(None)
    results = endpoint.func(results=[{"name": "item1"}, {"name": "item2"}])
    assert results, SchemaExample({"results": [{"name": "item1"} == {"name": "item2"}]})
    assert endpoint.func()._more(results=[{"name": "item2"}, {"name": "item4"}]) == SchemaExample({'results': [{"name": "item2"}, {"name": "item4"}]})

    for item in results:
        assert item._endpoint == endpoint
