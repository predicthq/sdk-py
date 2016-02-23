# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

import os
import unittest

from predicthq.config import Config
from predicthq.exceptions import ConfigError


class ConfigTest(unittest.TestCase):

    def test_defaults(self):
        config = Config()
        self.assertEqual(config.ENDPOINT_URL, "https://api.predicthq.com")
        self.assertEqual(config.OAUTH2_CLIENT_ID, None)
        self.assertEqual(config.OAUTH2_CLIENT_SECRET, None)
        self.assertEqual(config.OAUTH2_SCOPE, None)
        self.assertEqual(config.OAUTH2_ACCESS_TOKEN, None)
        self.assertEqual(config.LOGGING_LOG_LEVEL, "WARNING")

    def test_defaults_from_locations(self):
        CONFIG_LOCATIONS = (
            os.path.join(os.path.dirname(__file__), 'fixtures', 'test.conf'),
            os.path.join(os.path.dirname(__file__), 'fixtures', 'test2.conf')
        )

        config = Config(*CONFIG_LOCATIONS)
        self.assertEqual(config.ENDPOINT_URL, "https://example.org")
        self.assertEqual(config.OAUTH2_CLIENT_ID, "client_id")
        self.assertEqual(config.OAUTH2_CLIENT_SECRET, "client_secret")
        self.assertEqual(config.OAUTH2_SCOPE, "account events")
        self.assertEqual(config.OAUTH2_ACCESS_TOKEN, "access_token")
        self.assertEqual(config.LOGGING_LOG_LEVEL, "DEBUG")

    def test_defaults_from_environment(self):
        os.environ["PREDICTHQ_ENDPOINT_URL"] = "https://example.org/endpoint/"
        try:
            config = Config(os.path.join(os.path.dirname(__file__), 'fixtures', 'test.conf'))
            self.assertEqual(config.ENDPOINT_URL, "https://example.org/endpoint/")
            self.assertEqual(config.OAUTH2_CLIENT_ID, "client_id")
            self.assertEqual(config.OAUTH2_CLIENT_SECRET, "client_secret")
            self.assertEqual(config.OAUTH2_SCOPE, "scope")
            self.assertEqual(config.OAUTH2_ACCESS_TOKEN, "access_token")
            self.assertEqual(config.LOGGING_LOG_LEVEL, "log_level")
        finally:
            del os.environ["PREDICTHQ_ENDPOINT_URL"]

    def test_get_config(self):
        config = Config()
        self.assertEqual(config.ENDPOINT_URL, "https://api.predicthq.com")

        with self.assertRaises(ConfigError):
            assert config.INVALID_CONFIG

    def test_set_config(self):
        config = Config()
        config.ENDPOINT_URL = "https://example.org"
        self.assertEqual(config.ENDPOINT_URL, "https://example.org")

        with self.assertRaises(ConfigError):
            config.INVALID_CONFIG = "invalid"
