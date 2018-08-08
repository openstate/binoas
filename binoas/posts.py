from collections import UserDict
import sys
from jsonpath_rw import jsonpath, parse


class Post(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (
            ('application' in self) and
            ('payload' in self)
        ):
            raise ValueError('Not a valid post')


class BasePostTransformer(object):
    def __init__(self, config):
        self.config = config

    def transform(self, payload):
        raise NotImplementedError


class JSONPathPostTransformer(BasePostTransformer):
        def transform(self, payload):
            post = Post(payload)
            return
