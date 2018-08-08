import sys
from jsonpath_rw import jsonpath, parse

from binoas.posts import Post

class BasePostTransformer:
    def __init__(self, config):
        self.config = config

    def transform(self, payload):
        raise NotImplementedError


class JSONPathPostTransformer(BasePostTransformer):
        def transform(self, payload):
            post = Post(payload)
            return
