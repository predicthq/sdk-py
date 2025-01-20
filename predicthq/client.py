import json
import logging
from platform import python_version
from urllib.parse import urljoin, urlparse, urlunparse
from weakref import proxy

import requests
import stamina

from .config import config
from .exceptions import ClientError, RetriableError, ServerError
from .version import __version__


class Client(object):
    @classmethod
    def build_url(cls, path):
        result = list(urlparse(path))
        result[2] = f"/{result[2].strip('/')}"
        return urljoin(config.ENDPOINT_URL, urlunparse(result))

    def __init__(self, access_token=None):
        self.logger = logging.getLogger("predicthq")
        self.logger.setLevel(config.LOGGING_LOG_LEVEL)
        self.access_token = access_token or config.OAUTH2_ACCESS_TOKEN
        self.initialize_endpoints()

    def initialize_endpoints(self):
        from predicthq import endpoints

        self.oauth2 = endpoints.OAuth2Endpoint(proxy(self))
        self.broadcasts = endpoints.BroadcastsEndpoint(proxy(self))
        self.events = endpoints.EventsEndpoint(proxy(self))
        self.features = endpoints.FeaturesEndpoint(proxy(self))
        self.accounts = endpoints.AccountsEndpoint(proxy(self))
        self.places = endpoints.PlacesEndpoint(proxy(self))
        self.radius = endpoints.SuggestedRadiusEndpoint(proxy(self))
        self.beam = endpoints.BeamEndpoint(proxy(self))

    def get_headers(self, headers):
        _headers = {
            "Accept": "application/json",
            "x-user-agent": f"PHQ-Py-SDK/{__version__} (python/{python_version()})",
        }
        if self.access_token:
            _headers.update(
                {
                    "Authorization": f"Bearer {self.access_token}",
                }
            )
        _headers.update(**headers)
        return _headers

    @stamina.retry(on=RetriableError, attempts=3)
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

            if response.status_code in (429, 503, 504):
                # We want to retry for these http status codes
                raise RetriableError(error)
            elif 400 <= response.status_code <= 499:
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
