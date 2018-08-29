#!/usr/bin/env python

import unittest

from binoas.utils import load_config, is_valid_config, parse_frequency
from binoas.exceptions import ConfigurationError


class TestLoadConfig(unittest.TestCase):
    def test_valid_config(self):
        config = {
            'binoas': {}
        }
        self.assertTrue(is_valid_config(config))

    def test_invalid_config_no_main_key(self):
        config = {
            'dummy': {}
        }
        self.assertFalse(is_valid_config(config))

    def test_invalid_config_multiple_keys(self):
        config = {
            'binoas': {},
            'other': 'yes'
        }
        self.assertFalse(is_valid_config(config))

    def test_invalid_config_multiple_keys_no_main_key(self):
        config = {
            'dummy': {},
            'other': 'yes'
        }
        self.assertFalse(is_valid_config(config))

    def test_invalid_config_empty(self):
        config = {
        }
        self.assertFalse(is_valid_config(config))

    def test_load_config(self):
        result = load_config('tests/data/test.yaml')
        expected = {
            'binoas': {
                'zookeeper': 'kafka',
                '_defaults': {
                    'routes': {
                        'app': {
                            'topics': {
                                'in': [
                                    'topic'
                                ]
                            },
                        },
                        'transformer': {
                            'topics': {
                                'in': [
                                    'topic'
                                ],
                                'out': [
                                    'objects'
                                ]
                            }
                        },
                        'loader': {
                            'topics': {
                                'in': [
                                    'objects'
                                ]
                            }
                        }
                    }
                },
                'applications': {
                    'poliflw': {
                        'name': 'PoliFLW'
                    },
                    'politwoops': {
                        'name': 'politwoops'
                    },
                    'openraadsinformatie': {
                        'name': "Open Raadsinformatie"
                    }
                }
            }
        }

        self.assertEqual(result, expected)

    def test_load_invalid_config(self):
        with self.assertRaises(ConfigurationError):
            load_config('tests/data/invalid.yaml')


class TestParseFrequency(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(ValueError):
            parse_frequency('')

    def test_seconds(self):
        result = parse_frequency('1s')
        self.assertEqual(result, 1)

    def test_minutes(self):
        result = parse_frequency('1m')
        self.assertEqual(result, 60)

    def test_hours(self):
        result = parse_frequency('1h')
        self.assertEqual(result, 3600)

    def test_days(self):
        result = parse_frequency('1d')
        self.assertEqual(result, 86400)

    def test_weeks(self):
        result = parse_frequency('1w')
        self.assertEqual(result, 604800)

    def test_years(self):
        result = parse_frequency('1y')
        self.assertEqual(result, 31536000)

    def test_invalid_period(self):
        with self.assertRaises(ValueError):
            parse_frequency('1q')

    def test_garbage(self):
        with self.assertRaises(ValueError):
            parse_frequency('asdq')

    def test_numbers_only(self):
        with self.assertRaises(ValueError):
            parse_frequency('1234')
