import sys
from jsonpath_rw import jsonpath, parse


class BasePostTransformer(object):
    def __init__(self, config):
        self.config = config

    def transform(self, post):
        raise NotImplementedError

    def is_valid_post(self, post):
        return (
            ('application' in post) and
            ('payload' in post) and
            (post['application'] in self.config['binoas']['applications'].keys()))


class JSONPathPostTransformer(BasePostTransformer):
        def transform(self, post):
            return
