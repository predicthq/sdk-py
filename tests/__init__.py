import functools
import json
import os
import re
from unittest import mock

import responses

from predicthq import Client
from predicthq.config import config


def load_fixture(name):
    fpath = "{}/fixtures/{}.json".format(os.path.dirname(__file__), name)
    with open(fpath) as fp:
        try:
            return json.loads(fp.read())
        except IOError:
            raise Exception("Fixture for this test does not exist: {}".format(fpath))


def load_reqresp_fixture(name):
    fpath = "{}/fixtures/requests_responses/{}.json".format(os.path.dirname(__file__), name)
    with open(fpath) as fp:
        try:
            return json.loads(fp.read())
        except IOError:
            raise Exception("Fixture for this test does not exist: {}".format(fpath))


def with_mock_responses(req_resp=None):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            class_name, func_name = (
                re.sub(r"([A-Z]+)", r"_\1", args[0].__class__.__name__).lower().strip("_"),
                f.__name__,
            )
            fixtures = load_reqresp_fixture(req_resp or "{}/{}".format(class_name, func_name))
            with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
                for fixture in fixtures:
                    if "url_re" in fixture:
                        url_re = fixture.pop("url_re")
                        fixture["url"] = re.compile(Client.build_url(url_re))
                    else:
                        fixture["url"] = Client.build_url(fixture["url"])
                    if "content_type" in fixture and fixture["content_type"] == "application/json":
                        fixture["body"] = json.dumps(fixture["body"])
                    rsps.add(**fixture)
                return f(responses=rsps, *args, **kwargs)

        return wrapper

    return decorator


def with_config(**new_config):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            old_config = {}

            for key, value in new_config.items():
                old_config[key] = getattr(config, key)
                setattr(config, key, value)

            result = f(*args, **kwargs)

            for key, value in old_config.items():
                setattr(config, key, value)

            return result

        return wrapper

    return decorator


def with_mock_client(request_returns=None, request_raises=None, *client_args, **client_kwargs):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            with mock.patch.object(Client, "request", return_value=request_returns, side_effect=request_raises):
                return f(client=Client(*client_args, **client_kwargs), *args, **kwargs)

        return wrapper

    return decorator


def with_client(*client_args, **client_kwargs):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f(client=Client(*client_args, **client_kwargs), *args, **kwargs)

        return wrapper

    return decorator
