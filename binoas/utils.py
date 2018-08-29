from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

import re

from binoas.exceptions import ConfigurationError


def load_config(config_file='config.yaml'):
    """
    Loads a configuration file (which is a YAML file). The location iof the
    file can be specified using the parameter. It further checks if it is a
    valid configuration file and if so, returns the parsed data strcture.
    """
    config = {}
    with open(config_file) as f:
        config = load(f, Loader=Loader)

    if not is_valid_config(config):
        raise ConfigurationError('Not a valid binoas configuration file')

    return config


def is_valid_config(config):
    """
    Checks if a data structure can be considered as a valid binoas
    configuration file. Returns true or false.
    """
    return (
        len(config.keys()) == 1 and
        ('binoas' in config)
    )


def parse_frequency(freq):
    """
    Parses a frequency string and returns the number of seconds.
    Supported formats: 1s, 1m, 1h, 1d, 1w, 1y
    """
    m = re.search('^(\d+)(s|m|h|d|w|y)$', freq.lower())
    if m is None:
        raise ValueError('Input not in required format')

    multipliers = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
        'w': 604800,
        'y': 31536000,
    }

    return int(m.group(1)) * multipliers[m.group(2)]
