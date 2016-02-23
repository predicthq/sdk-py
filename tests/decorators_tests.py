# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

import unittest

from predicthq import schemas
from predicthq import decorators
from predicthq.endpoints.base import BaseEndpoint
from predicthq.exceptions import ValidationError


class DecoratorsTest(unittest.TestCase):

    def test_to_params(self):
        kwargs = {"string_type": "my-string", "list_type": [1, 2, 3], "dict_type": {"key1": "val1", "key2": "val2"}, "bool_type": True}
        expected = {'string_type': 'my-string', 'list_type': '1,2,3', 'dict_type.key1': u'val1', 'dict_type.key2': 'val2', 'bool_type': 1}
        self.assertDictEqual(decorators._to_url_params(kwargs), expected)

    def test_kwargs_processor(self):
        kwargs = {"normal_arg": "value", "nested__arg": "value"}
        expected = {'normal_arg': 'value', 'nested': {'arg': 'value'}}
        self.assertDictEqual(decorators._process_kwargs(kwargs), expected)

    def test_accepts(self):

        class SchemaExample(schemas.Model):
            arg1 = schemas.StringType(required=True)
            arg2 = schemas.ListType(schemas.IntType)

        class EndpointExample(object):

            @decorators.accepts(SchemaExample)
            def func(self, **kwargs):
                return kwargs

        endpoint = EndpointExample()
        self.assertDictEqual(endpoint.func(arg1="test", arg2=[1, 2]), {'arg1': 'test', 'arg2': '1,2'})

        self.assertDictEqual(endpoint.func(SchemaExample({"arg1": "test", "arg2": [1, 2]})), {'arg1': 'test', 'arg2': '1,2'})

        self.assertDictEqual(endpoint.func({"arg1": "test", "arg2": [1, 2]}), {'arg1': 'test', 'arg2': '1,2'})

        with self.assertRaises(ValidationError):
            endpoint.func(arg2=[1, 2])

        with self.assertRaises(ValidationError):
            endpoint.func(arg1="value", arg2="invalid")

    def test_accepts_for_body_use(self):

        class SchemaExample(schemas.Model):
            arg1 = schemas.StringType(required=True)
            arg2 = schemas.ListType(schemas.IntType)

        class EndpointExample(object):

            @decorators.accepts(SchemaExample, query_string=False)
            def func(self, **kwargs):
                return kwargs

        endpoint = EndpointExample()
        self.assertDictEqual(endpoint.func({"arg1": "test", "arg2": [1, 2]}), {'arg1': 'test', 'arg2': [1, 2]})

    def test_returns(self):

        class SchemaExample(schemas.Model):
            arg1 = schemas.StringType(required=True)
            arg2 = schemas.ListType(schemas.IntType)

        class EndpointExample(object):

            @decorators.returns(SchemaExample)
            def func(self, **kwargs):
                return kwargs

        endpoint = EndpointExample()
        self.assertEqual(endpoint.func(arg1="test", arg2=[1, 2]), SchemaExample({'arg1': 'test', 'arg2': [1, 2]}))

        with self.assertRaises(ValidationError):
            endpoint.func(arg2=[1, 2])

        with self.assertRaises(ValidationError):
            endpoint.func(arg1="value", arg2="invalid")

    def test_returns_resultset_of_native_types(self):

        class SchemaExample(schemas.ResultSet):

            results = schemas.ListType(schemas.StringType)

        class EndpointExample(BaseEndpoint):

            @decorators.returns(SchemaExample)
            def func(self, **kwargs):
                return kwargs

        endpoint = EndpointExample(None)
        self.assertEqual(endpoint.func(results=["item1", "item2"]), SchemaExample({"results": ["item1", "item2"]}))
        self.assertEqual(endpoint.func()._more(results=["item3", "item4"]), SchemaExample({'results': ['item3', 'item4']}))
        self.assertEqual(endpoint, endpoint.func()._endpoint)

    def test_returns_resultset_of_models(self):

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
        self.assertEqual(results, SchemaExample({"results": [{"name": "item1"}, {"name": "item2"}]}))
        self.assertEqual(endpoint.func()._more(results=[{"name": "item2"}, {"name": "item4"}]), SchemaExample({'results': [{"name": "item2"}, {"name": "item4"}]}))

        for item in results:
            self.assertEqual(item._endpoint, endpoint)
