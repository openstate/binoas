from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def load_config(config_file='config.yaml'):
    config = {}
    with open(config_file) as f:
        config = load(f, Loader=Loader)
    return config
