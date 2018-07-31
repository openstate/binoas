from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def load_config():
    config = {}
    with open('config.yaml') as f:
        config = load(f, Loader=Loader)
    return config['binoas']
