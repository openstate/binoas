#!/usr/bin/env python

import unittest

from binoas.posts import BasePostTransformer, JSONPathPostTransformer


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

    def test_valid_post(self):
        post = {
            'application': 'poliflw',
            'payload': {}
        }
        self.assertTrue(self.post_transformer.is_valid_post(post))

    def test_invalid_application_post(self):
        post = {
            'application': 'politwoops',
            'payload': {}
        }
        self.assertFalse(self.post_transformer.is_valid_post(post))

    def test_no_application_post(self):
        post = {
            'payload': {}
        }
        self.assertFalse(self.post_transformer.is_valid_post(post))

    def test_no_payload_post(self):
        post = {
            'application': 'politwoops'
        }
        self.assertFalse(self.post_transformer.is_valid_post(post))

    def test_empty_post(self):
        post = {
        }
        self.assertFalse(self.post_transformer.is_valid_post(post))


class TestJSONPathPostTransformer(unittest.TestCase):
    def setUp(self):
        rules = {}
        self.post_transformer = JSONPathPostTransformer(rules)

    def test_transform(self):
        self.assertEqual(self.post_transformer.transform({}), None)
