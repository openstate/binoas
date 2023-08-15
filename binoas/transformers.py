import sys
import logging

from jsonpath_rw import jsonpath, parse

from binoas.posts import Post

class BasePostTransformer:
    """
    This is the base class for a transformer. It does nothing more than store
    the config in the instance and provide a method for transformation of a post
    which is not implemented in this class.
    """
    def __init__(self, config):
        self.config = config

    def transform(self, payload):
        raise NotImplementedError


class JSONPathPostTransformer(BasePostTransformer):
    """
    This class transforms the given payload according to json path statements
    specified in the configuration file. It applies these rules and returns the
    transformed message.
    """
    def transform(self, payload):
        """
        This class transforms the given payload according to json path statements
        specified in the configuration file. It applies these rules and returns the
        transformed message.
        """
        post = Post(payload)
        logging.info('Got a message for application %s' % (post['application'],))
        logging.info(self.config['binoas']['applications'][post['application']])
        # The result should be a valid post also ...
        result = {
            'application': post['application'],
            'payload': {}
        }
        for fld, expr in self.config['binoas']['applications'][post['application']]['rules'].items():
            # we have several fields and also a data field. The non-data fields
            # are used in the email (Ie. to provide title and description and
            # so on.)
            if fld != 'data':
                # if it is not a data field we have a simple transformation
                jsonpath_expr = parse(expr)
                try:
                    res = jsonpath_expr.find(post['payload'])[0].value
                except IndexError:
                    res = None
                result['payload'][fld] = res
            else:
                # the data fields have a more elaborate transformation as it
                # can contain a lot of information
                result['payload']['data'] = []
                for expr_info in expr:
                    # the data fields can be specified as a list of strings or
                    # as a list of dicts (or in between). This allows you to
                    # override the keys in the transformed result. (Otherwise
                    # the keys would have taken the json path expressions which
                    # can be quite complex)
                    if not isinstance(expr_info, dict):
                        expr_info = {
                            'path': expr_info,
                            'name': expr_info
                        }
                    jsonpath_expr = parse(expr_info['path'])
                    for res in jsonpath_expr.find(post['payload']):
                        # if the values of the requested path are a list we
                        # should transform accordingly (Ie. returns multiple
                        # data objects)
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
