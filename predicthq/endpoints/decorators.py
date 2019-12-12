import functools
from collections import defaultdict

from predicthq.endpoints.schemas import ResultSet, Model, SchematicsDataError
from predicthq.exceptions import ValidationError


def _to_url_params(data, glue=".", separator=","):
    """
    Converts data dictionary to url parameters
    """
    params = {}
    for key, value in data.items():
        if isinstance(value, bool):
            params[key] = 1 if value else 0
        elif isinstance(value, list):
            params[key] = separator.join(map(str, value))
        elif isinstance(value, dict):
            for subkey, subvalue in value.items():
                if isinstance(subvalue, list):
                    params[glue.join((key, subkey))] = separator.join(map(str, subvalue))
                else:
                    params[glue.join((key, subkey))] = subvalue
        else:
            params[key] = value
    return params


def _process_kwargs(kwargs, separator="__"):
    data = defaultdict(dict)
    for key, value in kwargs.items():
        if separator in key:
            k, subk = key.split(separator)
            data[k][subk] = value
        else:
            data[key] = value
    return data


def accepts(schema_class, query_string=True, role=None):

    def decorator(f):

        @functools.wraps(f)
        def wrapper(endpoint, *args, **kwargs):

            schema = getattr(endpoint.Meta, f.__name__, {}).get("accepts", schema_class)

            if not kwargs:  # accept instance of schema_class
                new_args = tuple(a for a in args if not isinstance(a, (schema, dict)))
                if args != new_args:
                    instance = next(a for a in args if isinstance(a, (schema, dict)))
                    if isinstance(instance, dict):
                        kwargs = instance
                    else:
                        kwargs = instance.to_dict()
                    args = new_args

            try:
                data = _process_kwargs(kwargs)
                model = schema()
                model.import_data(data, strict=True, partial=False)
                model.validate()
            except SchematicsDataError as e:
                raise ValidationError(e.messages)

            if query_string:
                params = _to_url_params(model.to_primitive(role=role))
            else:
                params = model.to_primitive(role=role)

            return f(endpoint, *args, **params)

        return wrapper

    return decorator


def returns(schema_class):

    def decorator(f):

        @functools.wraps(f)
        def wrapper(endpoint, *args, **kwargs):

            schema = getattr(endpoint.Meta, f.__name__, {}).get("returns", schema_class)

            data = f(endpoint, *args, **kwargs)
            try:
                model = schema()
                model._endpoint = endpoint

                # if schema class is a ResultSet, tell it how to load more results
                if issubclass(schema_class, ResultSet):
                    model._more = functools.partial(wrapper, endpoint)

                    # if results are of type Model, make sure to set the endpoint on each item
                    if data is not None and 'results' in data \
                            and hasattr(model._fields['results'], 'model_class') \
                            and issubclass(model._fields['results'].model_class, Model):
                        def initialize_result_type(item_data):
                            item = model._fields['results'].model_class(item_data, strict=False)
                            item._endpoint = endpoint
                            return item
                        # Use generator so results are not iterated over more than necessary
                        data['results'] = (initialize_result_type(item_data) for item_data in data['results'])

                model.import_data(data, strict=False)
                model.validate()
            except SchematicsDataError as e:
                raise ValidationError(e.messages)
            return model

        return wrapper

    return decorator
