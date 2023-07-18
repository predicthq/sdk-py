import functools

from predicthq.config import config


DEFAULT_CONFIG_MAPPING = {
    "client_id": config.OAUTH2_CLIENT_ID,
    "client_secret": config.OAUTH2_CLIENT_SECRET,
    "scope": config.OAUTH2_SCOPE,
    "grant_type": "client_credentials",
    "token_type_hint": "access_token",
}


def preload_config_defaults(defaults_to_load):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(endpoint, *args, **kwargs):
            for key in defaults_to_load:
                if key not in kwargs and key in DEFAULT_CONFIG_MAPPING:
                    kwargs[key] = DEFAULT_CONFIG_MAPPING[key]

            if kwargs.get("scope") and "," in kwargs["scope"]:
                kwargs["scope"] = " ".join(kwargs["scope"].split(","))

            return f(endpoint, *args, **kwargs)

        return wrapper

    return decorator
