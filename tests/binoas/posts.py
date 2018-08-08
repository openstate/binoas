#!/usr/bin/env python

import unittest

from binoas.posts import Post, BasePostTransformer, JSONPathPostTransformer


class TestPost(unittest.TestCase):
    def test_valid_post(self):
        payload = {
            'application': 'poliflw',
            'payload': {}
        }
        post = Post(payload)
        self.assertEqual(post['application'], 'poliflw')
        self.assertEqual(post['payload'], {})

    def test_no_application_post(self):
        payload = {
            'payload': {}
        }
        with self.assertRaises(ValueError):
            post = Post(payload)

    def test_no_payload_post(self):
        payload = {
            'application': 'politwoops'
        }
        with self.assertRaises(ValueError):
            post = Post(payload)

    def test_empty_post(self):
        payload = {
        }
        with self.assertRaises(ValueError):
            post = Post(payload)


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
