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
            params.update(_flatten_dict(value, glue, separator, parent_key=key))
        else:
            params[key] = value
    return params


def _flatten_dict(d, glue, separator, parent_key=""):
    flat_dict = {}
    for k, v in d.items():
        if isinstance(v, dict):
            flat_dict.update(_flatten_dict(v, glue, separator, f"{parent_key}{glue}{k}" if parent_key else k))
            continue
        if isinstance(v, list):
            flat_dict.update({f"{parent_key}{glue}{k}" if parent_key else k: separator.join(map(str, v))})
            continue
        flat_dict.update({f"{parent_key}{glue}{k}" if parent_key else k: v})
    return flat_dict


def _assign_nested_key(parent_dict, keys, value):
    current_key = keys[0]
    if len(keys) > 1:
        if current_key not in parent_dict:
            parent_dict[current_key] = dict()
        _assign_nested_key(parent_dict[current_key], keys[1:], value)
    else:
        parent_dict[current_key] = value        


def _process_kwargs(kwargs, separator="__"):
    data = dict()
    for key, value in kwargs.items():
        if separator in key:
            _assign_nested_key(data, key.split(separator), value)
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
                loaded_model = model(**data)
                loaded_model._more = functools.partial(wrapper, endpoint)
                loaded_model._endpoint = endpoint
                return loaded_model
            except PydanticValidationError as e:
                raise ValidationError(e)

        return wrapper

    return decorator
