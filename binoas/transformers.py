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
                if fld != 'data':
                    jsonpath_expr = parse(expr)
                    try:
                        res = jsonpath_expr.find(post['payload'])[0].value
                    except IndexError:
                        res = None
                    result['payload'][fld] = res
                else:
                    result['payload']['data'] = []
                    for expr_info in expr:
                        if not isinstance(expr_info, dict):
                            expr_info = {
                                'path': expr_info,
                                'name': expr_info
                            }
                        jsonpath_expr = parse(expr_info['path'])
                        for res in jsonpath_expr.find(post['payload']):
                            if type(res.value) is list:
                                values = res.value
                            else:
                                values = [res.value]
                            for value in values:
                                result['payload']['data'].append({
                                    'key': expr_info['name'],
                                    'value': value
                                })

            return result
