import sys
from jsonpath_rw import jsonpath, parse


class BasePostTransformer(object):
    def __init__(self, rules):
        self.rules = rules

    def transform(self, post):
        raise NotImplementedError


class JSONPathPostTransformer(BasePostTransformer):
        def transform(self, post):
            return
