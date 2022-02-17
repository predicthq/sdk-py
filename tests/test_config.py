import os

import pytest

from predicthq.config import Config
from predicthq.exceptions import ConfigError


def test_defaults():
    config = Config()
    assert config.ENDPOINT_URL == "https://api.predicthq.com"
    assert config.OAUTH2_CLIENT_ID is None
    assert config.OAUTH2_CLIENT_SECRET is None
    assert config.OAUTH2_SCOPE is None
    assert config.OAUTH2_ACCESS_TOKEN is None
    assert config.LOGGING_LOG_LEVEL == "WARNING"


def test_defaults_from_locations():
    CONFIG_LOCATIONS = (
        os.path.join(os.path.dirname(__file__), "fixtures", "test.conf"),
        os.path.join(os.path.dirname(__file__), "fixtures", "test2.conf"),
    )

    config = Config(*CONFIG_LOCATIONS)
    assert config.ENDPOINT_URL == "https://example.org"
    assert config.OAUTH2_CLIENT_ID == "client_id"
    assert config.OAUTH2_CLIENT_SECRET == "client_secret"
    assert config.OAUTH2_SCOPE == "account events"
    assert config.OAUTH2_ACCESS_TOKEN == "access_token"
    assert config.LOGGING_LOG_LEVEL == "DEBUG"


def test_defaults_from_environment():
    os.environ["PREDICTHQ_ENDPOINT_URL"] = "https://example.org/endpoint/"
    try:
        config = Config(os.path.join(os.path.dirname(__file__), "fixtures", "test.conf"))
        assert config.ENDPOINT_URL == "https://example.org/endpoint/"
        assert config.OAUTH2_CLIENT_ID == "client_id"
        assert config.OAUTH2_CLIENT_SECRET == "client_secret"
        assert config.OAUTH2_SCOPE == "scope"
        assert config.OAUTH2_ACCESS_TOKEN == "access_token"
        assert config.LOGGING_LOG_LEVEL == "log_level"
    finally:
        del os.environ["PREDICTHQ_ENDPOINT_URL"]


def test_get_config():
    config = Config()
    assert config.ENDPOINT_URL == "https://api.predicthq.com"

    with pytest.raises(ConfigError):
        assert config.INVALID_CONFIG


def test_set_config():
    config = Config()
    config.ENDPOINT_URL = "https://example.org"
    assert config.ENDPOINT_URL == "https://example.org"

    with pytest.raises(ConfigError):
        config.INVALID_CONFIG = "invalid"
