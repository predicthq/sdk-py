import functools

from pydantic import ValidationError as PydanticValidationError

from predicthq.exceptions import ValidationError

from predicthq.endpoints.schemas import ArgKwargResultSet


def _kwargs_to_key_list_mapping(kwargs, separator="__"):
    """
    Converts kwargs to a nested dictionary mapping keys to lists of values
    """
    data = {}
    for key, value in kwargs.items():
        keys = key.split(separator, 1)
        if len(keys) > 1:
            value = {keys[1]: value}
        if isinstance(value, dict):
            value = _kwargs_to_key_list_mapping(value)

        data[keys[0]] = [] if not data.get(keys[0]) else data[keys[0]]
        data[keys[0]].append(value)
    return data


def _to_url_params(key_list_mapping, glue=".", separator=",", parent_key=""):
    """
    Converts key_list_mapping to url parameters
    """
    params = {}
    for key, value in key_list_mapping.items():
        current_key = f"{parent_key}{glue}{key}" if parent_key else key
        for v in value:
            if isinstance(v, dict):
                params.update(_to_url_params(v, glue, separator, current_key))
            elif isinstance(v, list):
                params.update({current_key: separator.join(map(str, v))})
            elif isinstance(v, bool):
                params.update({current_key: 1 if v else 0})
            else:
                params.update({current_key: v})
    return params


def _to_json(key_list_mapping, json=None):
    """
    Converts key_list_mapping to json
    """
    if json is None:
        json = {}
    for key, value in key_list_mapping.items():
        for v in value:
            json[key] = dict() if not json.get(key) else json[key]
            if isinstance(v, dict):
                _to_json(v, json[key])
            else:
                json[key] = v
    return json


def accepts(query_string=True, role=None):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(endpoint, *args, **kwargs):
            key_list_mapping = _kwargs_to_key_list_mapping(kwargs)
            if hasattr(endpoint, "mutate_bool_to_default_for_type"):
                endpoint.mutate_bool_to_default_for_type(key_list_mapping)

            if query_string:
                data = _to_url_params(key_list_mapping)
            else:
                data = _to_json(key_list_mapping)

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
                if isinstance(loaded_model, ArgKwargResultSet):
                    loaded_model._args = args
                    loaded_model._kwargs = kwargs
                return loaded_model
            except PydanticValidationError as e:
                raise ValidationError(e)

        return wrapper

    return decorator
