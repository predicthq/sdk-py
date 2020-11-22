import json
import logging
from urllib.parse import urljoin, urlparse, urlunparse
from weakref import proxy

import requests

from .config import config
from .exceptions import ClientError, ServerError
from .version import __version__


class Client(object):

    @classmethod
    def build_url(cls, path):
        result = list(urlparse(path))
        result[2] = "/{}/".format(result[2].strip('/'))
        return urljoin(config.ENDPOINT_URL, urlunparse(result))

    def __init__(self, access_token=None):
        self.logger = logging.getLogger('predicthq')
        self.logger.setLevel(config.LOGGING_LOG_LEVEL)
        self.access_token = access_token or config.OAUTH2_ACCESS_TOKEN
        self.initialize_endpoints()

    def initialize_endpoints(self):
        from predicthq import endpoints
        self.oauth2 = endpoints.OAuth2Endpoint(proxy(self))
        self.broadcasts = endpoints.BroadcastsEndpoint(proxy(self))
        self.events = endpoints.EventsEndpoint(proxy(self))
        self.accounts = endpoints.AccountsEndpoint(proxy(self))
        self.places = endpoints.PlacesEndpoint(proxy(self))

    def get_headers(self, headers):
        _headers = {"Accept": "application/json", "x-user-agent": "PHQ-Py-SDK/{}".format(__version__)}
        if self.access_token:
            _headers.update({"Authorization": "Bearer {}".format(self.access_token),})
        _headers.update(**headers)
        return _headers

    def request(self, method, path, **kwargs):
        headers = self.get_headers(kwargs.pop("headers", {}))
        response = requests.request(method, self.build_url(path), headers=headers, **kwargs)
        self.logger.debug(response.request.url)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            try:
                error = response.json()
            except ValueError:
                error = response.content

            if 400 <= response.status_code <= 499:
                raise ClientError(error)
            else:
                raise ServerError(error)

        try:
            result = response.json() or None
        except:
            result = None

        if self.logger.getEffectiveLevel() == logging.DEBUG:
            self.logger.debug(json.dumps(result, indent=True))

        return result

    def get(self, path, **kwargs):
        return self.request("get", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("post", path, **kwargs)

    def put(self, path, **kwargs):
        return self.request("put", path, **kwargs)

    def patch(self, path, **kwargs):
        return self.request("patch", path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("delete", path, **kwargs)

    def authenticate(self, **kwargs):
        token = self.oauth2.get_token(**kwargs)
        self.access_token = token.access_token
        return token
