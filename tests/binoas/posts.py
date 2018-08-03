#!/usr/bin/env python

import unittest

from binoas.posts import BasePostTransformer, JSONPathPostTransformer


class TestBasePostTransformer(unittest.TestCase):
    def setUp(self):
        rules = {}
        self.post_transformer = BasePostTransformer(rules)

    def test_transform(self):
        with self.assertRaises(NotImplementedError):
            self.post_transformer.transform({})


class TestJSONPathPostTransformer(unittest.TestCase):
    def setUp(self):
        rules = {}
        self.post_transformer = JSONPathPostTransformer(rules)

    def test_transform(self):
        self.assertEqual(self.post_transformer.transform({}), None)
