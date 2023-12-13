import pytest
from typing import List, Optional

from pydantic import BaseModel

from predicthq.endpoints import decorators, schemas
from predicthq.endpoints.base import BaseEndpoint
from predicthq.exceptions import ValidationError


def test_to_params():
    kwargs = {
        "string_type": "my-string",
        "list_type": [1, 2, 3],
        "dict_type": {"key1": "val1", "key2": "val2"},
        "bool_type": True,
        "nested_dict_type": {"key1": {"key2": "val2", "key3": "val3"}},
    }
    expected = {
        "string_type": "my-string",
        "list_type": "1,2,3",
        "dict_type.key1": u"val1",
        "dict_type.key2": "val2",
        "bool_type": 1,
        "nested_dict_type.key1.key2": "val2",
        "nested_dict_type.key1.key3": "val3",
    }
    assert decorators._to_url_params(kwargs) == expected


def test_kwargs_processor():
    kwargs = {"normal_arg": "value", "nested__arg": "value", "multiple__level__nested": "value"}
    expected = {"normal_arg": "value", "nested": {"arg": "value"}, "multiple": {"level": {"nested": "value"}}}
    assert decorators._process_kwargs(kwargs) == expected


def test_accepts():
    class EndpointExample(BaseEndpoint):
        @decorators.accepts()
        def func(self, *args, **kwargs):
            return args, kwargs

    endpoint = EndpointExample(None)

    transformed_args, transformed_kwargs = endpoint.func(arg1="test", arg2=[1, 2])
    assert transformed_kwargs == {"arg1": "test", "arg2": "1,2"}
    assert transformed_args == ()

    transformed_args, transformed_kwargs = endpoint.func(**{"arg1": "test", "arg2": [1, 2]})
    assert transformed_kwargs == {"arg1": "test", "arg2": "1,2"}
    assert transformed_args == ()

    transformed_args, transformed_kwargs = endpoint.func({"arg1": "test", "arg2": [1, 2]})
    assert transformed_kwargs == {}
    assert transformed_args == ({"arg1": "test", "arg2": [1, 2]},)


def test_returns():
    class SchemaExample(BaseModel):
        arg1: str
        arg2: List[int]

    class EndpointExample(BaseEndpoint):
        @decorators.returns(SchemaExample)
        def func(self, **kwargs):
            return kwargs

    endpoint = EndpointExample(None)
    assert endpoint.func(arg1="test", arg2=[1, 2]).model_dump(exclude_none=True) == SchemaExample(**{"arg1": "test", "arg2": [1, 2]}).model_dump(exclude_none=True)

    with pytest.raises(ValidationError):
        endpoint.func(arg2=[1, 2])

    with pytest.raises(ValidationError):
        endpoint.func(arg1="value", arg2="invalid")


def test_returns_resultset_of_native_types():
    class SchemaExample(schemas.ResultSet):
        results: Optional[List[str]] = []

    class EndpointExample(BaseEndpoint):
        @decorators.returns(SchemaExample)
        def func(self, **kwargs):
            return kwargs

    endpoint = EndpointExample(None)
    assert endpoint.func(results=["item1", "item2"]).model_dump(exclude_none=True) == SchemaExample(**{"results": ["item1", "item2"]}).model_dump(exclude_none=True)
    assert endpoint.func()._more(results=["item3", "item4"]).model_dump(exclude_none=True) == SchemaExample(**{"results": ["item3", "item4"]}).model_dump(exclude_none=True)
    assert endpoint == endpoint.func()._endpoint


def test_returns_resultset_of_models():
    class ModelExample(schemas.ResultSet):
        name: str

    class SchemaExample(schemas.ResultSet):
        results: Optional[List[ModelExample]] = None

    class EndpointExample(BaseEndpoint):
        @decorators.returns(SchemaExample)
        def func(self, **kwargs):
            return kwargs

    endpoint = EndpointExample(None)
    results = endpoint.func(results=[{"name": "item1"}, {"name": "item2"}])
    assert results.model_dump(exclude_none=True) == SchemaExample(**{"results": [{"name": "item1"}, {"name": "item2"}]}).model_dump(exclude_none=True)
    assert endpoint.func()._more(results=[{"name": "item2"}, {"name": "item4"}]).model_dump(exclude_none=True) == SchemaExample(
        **{"results": [{"name": "item2"}, {"name": "item4"}]}
    ).model_dump(exclude_none=True)
