#!/usr/bin/env python

import unittest

from binoas.utils import load_config, is_valid_config
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
