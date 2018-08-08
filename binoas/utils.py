from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


from binoas.exceptions import ConfigurationError


def load_config(config_file='config.yaml'):
    config = {}
    with open(config_file) as f:
        config = load(f, Loader=Loader)

    if not is_valid_config(config):
        raise ConfigurationError('Not a valid binoas configuration file')

    return config


def is_valid_config(config):
    return (
        len(config.keys()) == 1 and
        ('binoas' in config)
    )
