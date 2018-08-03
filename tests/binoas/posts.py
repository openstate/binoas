#!/usr/bin/env python

import unittest

from binoas.posts import BasePostTransformer


class TestBasePostTransformer(unittest.TestCase):
    def setUp(self):
        config = {
            'binoas': {}
        }
        self.post_transformer = BasePostTransformer(config)

    def test_transform(self):
        with self.assertRaises(NotImplementedError):
            self.post_transformer.transform({})
