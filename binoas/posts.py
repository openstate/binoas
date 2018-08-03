import sys
from jsonpath_rw import jsonpath, parse


class BasePostTransformer(object):
    def __init__(self, config):
        self.config = config

    def transform(self, post):
        raise NotImplementedError
