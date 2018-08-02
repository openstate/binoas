#!/usr/bin/env python

import unittest

from utils import load_config


class TestLoadConfig(unittest.TestCase):
    def test_load_config(self):
        result = load_config('tests/test.yaml')
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
