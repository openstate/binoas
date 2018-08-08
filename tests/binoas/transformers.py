#!/usr/bin/env python

import unittest

from binoas.transformers import BasePostTransformer, JSONPathPostTransformer

class TestBasePostTransformer(unittest.TestCase):
    def setUp(self):
        config = {
            'binoas': {
                'applications': {
                    'poliflw': {}
                }
            }
        }
        self.post_transformer = BasePostTransformer(config)

    def test_transform(self):
        with self.assertRaises(NotImplementedError):
            self.post_transformer.transform({})



class TestJSONPathPostTransformer(unittest.TestCase):
    def setUp(self):
        config = {
            'binoas': {
                'applications': {
                    'poliflw': {}
                }
            }
        }
        self.post_transformer = JSONPathPostTransformer(config)

    def test_transform_no_valid_post(self):
        with self.assertRaises(ValueError):
            self.post_transformer.transform({})
