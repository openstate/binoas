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
