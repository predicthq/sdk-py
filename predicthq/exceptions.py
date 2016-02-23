# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function


class PredictHQError(Exception):
    pass


class ConfigError(PredictHQError):
    pass


class APIError(PredictHQError):
    pass


class ClientError(APIError):
    pass


class ServerError(APIError):
    pass


class ValidationError(PredictHQError):
    pass
