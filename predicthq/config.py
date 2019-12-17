import configparser
import os

from predicthq.exceptions import ConfigError


CONFIG_LOCATIONS = (
    '/etc/predicthq.conf',
    os.path.join(os.path.expanduser('~'), '.predicthq', 'predicthq.conf'),
    os.path.join(os.getcwd(), 'predicthq.conf'),
)


class Config(object):

    _config_sections = (
        'endpoint',
        'oauth2',
        'logging',
    )

    _defaults = {
        "ENDPOINT_URL": "https://api.predicthq.com",
        "OAUTH2_CLIENT_ID": None,
        "OAUTH2_CLIENT_SECRET": None,
        "OAUTH2_SCOPE": None,
        "OAUTH2_ACCESS_TOKEN": None,
        "LOGGING_LOG_LEVEL": "WARNING",
    }

    _config = {}

    def __init__(self, *config_locations):
        self.load_defaults()
        self.load_defaults_from_locations(config_locations)
        self.load_defaults_from_environment()

    def load_defaults(self):
        for key, value in self._defaults.items():
            self._config[key] = value

    def load_defaults_from_locations(self, config_locations):
        cp = configparser.ConfigParser()
        for file_location in config_locations:
            if os.path.isfile(file_location):
                with open(file_location) as f:
                    cp.read_file(f)
                for section in self._config_sections:
                    try:
                        for key, value in cp.items(section):
                            self._config["{0}_{1}".format(section.upper(), key.upper())] = value
                    except configparser.NoSectionError:  # pragma: nocover
                        pass

    def load_defaults_from_environment(self):
        for key in self._defaults:
            self._config[key] = os.getenv("PREDICTHQ_{}".format(key), self._config[key])

    def __getattr__(self, item):
        try:
            return self._config[item]
        except KeyError:
            raise ConfigError("{} is not a valid config key".format(item))

    def __setattr__(self, item, value):
        if item not in self._config:
            raise ConfigError("{} is not a valid config key".format(item))
        self._config[item] = value


config = Config(*CONFIG_LOCATIONS)
