import functools
from collections import defaultdict

from pydantic import ValidationError as PydanticValidationError

from predicthq.endpoints.schemas import ResultSet
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



def accepts(query_string=True, role=None):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(endpoint, *args, **kwargs):
            data = _process_kwargs(kwargs)
            if hasattr(endpoint, "mutate_bool_to_default_for_type"):
                endpoint.mutate_bool_to_default_for_type(data)

            if query_string:
                data = _to_url_params(data=data)

            return f(endpoint, *args, **data)

        return wrapper

    return decorator


def returns(model_class):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(endpoint, *args, **kwargs):

            model = getattr(endpoint.Meta, f.__name__, {}).get("returns", model_class)

            data = f(endpoint, *args, **kwargs)
            try:
                loaded_model = model(**data) if data else model()
                loaded_model._more = functools.partial(wrapper, endpoint)
                loaded_model._endpoint = endpoint
                return loaded_model
            except PydanticValidationError as e:
                if not data:
                    return
                raise ValidationError(e)

        return wrapper

    return decorator
