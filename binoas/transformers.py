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

            result = {
                'application': post['application'],
                'payload': {}
            }
            for fld, expr in self.config['binoas']['applications'][post['application']]['rules'].items():
                jsonpath_expr = parse(expr)
                res = jsonpath_expr.find(post['payload'])[0].value
                result['payload'][fld] = res
            return result
