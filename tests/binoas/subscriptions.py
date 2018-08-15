#!/usr/bin/env python

import unittest

from binoas.subscriptions import Subscription


class TestSubscription(unittest.TestCase):
    def test_empty_subscription(self):
        payload = {
        }
        with self.assertRaises(ValueError):
            subscription = Subscription(payload)

    def test_only_application_subscription(self):
        payload = {
            'application': 'poliflw'
        }
        with self.assertRaises(ValueError):
            subscription = Subscription(payload)

    def test_only_application_email_subscription(self):
        payload = {
            'application': 'poliflw',
            'email': 'breyten@openstate.eu'
        }
        with self.assertRaises(ValueError):
            subscription = Subscription(payload)

    def test_only_application_email_freq_subscription(self):
        payload = {
            'application': 'poliflw',
            'email': 'breyten@openstate.eu',
            'frequency': '6H'
        }
        with self.assertRaises(ValueError):
            subscription = Subscription(payload)

    def test_valid_subscription_subscription(self):
        payload = {
            'application': 'poliflw',
            'email': 'breyten@openstate.eu',
            'frequency': '6H',
            'subscription': {
                'title': 'test'
            }
        }
        subscription = Subscription(payload)
        self.assertEqual(subscription['application'], 'poliflw')
        self.assertEqual(subscription['email'], 'breyten@openstate.eu')
        self.assertEqual(subscription['frequency'], '6H')
        self.assertEqual(subscription['subscription']['title'], 'test')

    def test_valid_subscription_query(self):
        payload = {
            'application': 'poliflw',
            'email': 'breyten@openstate.eu',
            'frequency': '6H',
            'query': {
                'match': {'title': 'test'}
            }
        }
        subscription = Subscription(payload)
        self.assertEqual(subscription['application'], 'poliflw')
        self.assertEqual(subscription['email'], 'breyten@openstate.eu')
        self.assertEqual(subscription['frequency'], '6H')
        self.assertEqual(subscription['query']['match']['title'], 'test')

    def test_build_query_empty_query(self):
        payload = {
            'application': 'poliflw',
            'email': 'breyten@openstate.eu',
            'frequency': '6H',
            'query': {
            }
        }

        expected = {}

        subscription = Subscription(payload)
        result = subscription.build_query()
        self.assertEqual(result, expected)

    def test_build_query_empty_subscription(self):
        payload = {
            'application': 'poliflw',
            'email': 'breyten@openstate.eu',
            'frequency': '6H',
            'subscription': {
            }
        }

        expected = {
            'query': {
                'bool': {
                    'must': [
                    ]
                }
            }
        }

        subscription = Subscription(payload)
        result = subscription.build_query()
        self.assertEqual(result, expected)

    def test_build_query_basic_query(self):
        payload = {
            'application': 'poliflw',
            'email': 'breyten@openstate.eu',
            'frequency': '6H',
            'query': {
                "match": {
                    "title": "test"
                }
            }
        }

        expected = {
            "match": {
                "title": "test"
            }
        }

        subscription = Subscription(payload)
        result = subscription.build_query()
        self.assertEqual(result, expected)

    def test_build_query_basic_subscription(self):
        payload = {
            'application': 'poliflw',
            'email': 'breyten@openstate.eu',
            'frequency': '6H',
            'subscription': {
                'title': 'test'
            }
        }

        expected = {
            'query': {
                'bool': {
                    'must': [
                        {
                            'term': {
                                'title': 'test'
                            }
                        }
                    ]
                }
            }
        }

        subscription = Subscription(payload)
        result = subscription.build_query()
        self.assertEqual(result, expected)

    def test_build_query_complex_subscription(self):
        payload = {
            'application': 'poliflw',
            'email': 'breyten@openstate.eu',
            'frequency': '6H',
            'subscription': {
                'title': 'test',
                'tag': 'tag1'
            }
        }

        expected = {
            'query': {
                'bool': {
                    'must': [
                        {
                            'term': {
                                'title': 'test'
                            }
                        },
                        {
                            'term': {
                                'tag': 'tag1'
                            }
                        }
                    ]
                }
            }
        }

        subscription = Subscription(payload)
        result = subscription.build_query()
        self.assertEqual(result, expected)
