#!/usr/bin/env python

import json
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
                    'poliflw': {
                        'name': 'PoliFLW',
                        'rules': {
                            'id': "meta.original_object_id",
                            'title': "title",
                            'description': "description",
                            'url': "meta.original_object_urls.html",
                            'created': "date",
                            'modified': "date",
                            'data': [
                                'parties',
                                'politicians',
                                'location',
                                'source',
                                'type',
                                'topics[*].name'
                            ]
                        }
                    }
                }
            }
        }

        self.post_transformer = JSONPathPostTransformer(config)

    def test_transform_no_valid_post(self):
        with self.assertRaises(ValueError):
            self.post_transformer.transform({})

    def test_transform_valid_post(self):
        expected = {
            'application': 'poliflw',
            'payload': {
                'id': 'https://www.cda.nl/noord-holland/amsterdam/actueel/nieuws/zomerborrel-6-september/',
                'title': 'Zomerborrel: 6 september',
                'description': (
                    'Donderdag 6 september hopen we op zomers weer, want dan vindt'
                    ' voor alle Amsterdamse CDA leden en geïnteresseerden de CDA '
                    'zomerborrel plaats. Voor €15,- ontvang je drie drankjes (bier,'
                    ' wijn, fris), een klein puntzakje friet en twee gefrituurde '
                    'snacks. Wie komt gezellig langs?&amp;nbsp;\nLocatie: Brasserie'
                    ' Nel, Amstelveld 12Aanvang: 19.30uAanmelden: via '
                    'dorienvoerman@hotmail.comBetaling: Je kunt de €15,- cash '
                    'meenemen of van te voren via CDA Afdeling Amsterdam op rekening '
                    'NL38INGB0000065005 overmaken o.v.v. CDA zomerborrel incl. je naam.'
                ),
                'url': 'https://www.cda.nl/noord-holland/amsterdam/actueel/nieuws/zomerborrel-6-september/',
                'created': '2018-07-25T12:31:38',
                'modified': '2018-07-25T12:31:38',
                'data': [
                    {'key': 'parties', 'value': 'CDA'},
                    {'key': 'parties', 'value': 'CDA'},
                    {'key': 'location', 'value': 'Amsterdam'},
                    {'key': 'source', 'value': 'Partij nieuws'},
                    {'key': 'type', 'value': 'Partij'},
                    {'key': 'topics[*].name', 'value': 'Zorg en gezondheid | Organisatie en beleid'}
                ]
            }
        }
        with open('tests/data/poliflw.json', 'r') as in_file:
            content = in_file.read()
        data = json.loads(content)
        result = self.post_transformer.transform(data)
        print(result)
        self.assertEqual(result, expected)
