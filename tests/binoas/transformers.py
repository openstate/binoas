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
                                {
                                    'name': 'topic',
                                    'path': 'topics[*].name'
                                }
                            ]
                        }
                    },
                    'politwoops': {
                        'name': 'Politwoops',
                        'rules': {
                            'id': "details.id_str",
                            'title': "details.text",
                            'description': "details.extended_tweet.full_text",
                            'url': "details.id_str",
                            'created': "created_at",
                            'modified': "updated_at",
                            'data': [
                                'user_name',
                                'politician_id',
                                'politician.party_id',
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

    def test_transform_valid_post_poliflw(self):
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
                    {'key': 'topic', 'value': 'Zorg en gezondheid | Organisatie en beleid'}
                ]
            }
        }
        with open('tests/data/poliflw.json', 'r') as in_file:
            content = in_file.read()
        data = json.loads(content)
        result = self.post_transformer.transform(data)
        self.assertEqual(result, expected)

    def test_transform_valid_post_politwoops(self):
        expected = {
            'application': 'politwoops',
            'payload': {
                'id': '1025749465611808768',
                'title': (
                    'Fijn de steun voor de initiatiefwet van @D66 @PvdA &amp; '
                    '@groenlinks van het Kabinet @KajsaOllongren &amp; '
                    '@markharbers om… https://t.co/YBlgoGseOQ'),
                'description': (
                    'Fijn de steun voor de initiatiefwet van @D66 @PvdA &amp; '
                    '@groenlinks van het Kabinet @KajsaOllongren &amp; '
                    '@markharbers om artikel 1 vd #Grondwet uit te breiden! '
                    '\uf64f\uf3fb! Nog wel wat werk te doen samen met collega'
                    '’s @kirstenvdhul &amp; @NevinOzutok, maar dit is een '
                    'fijne stimulans!\uf44a\uf3fb\uf308 https://t.co/KwCjmGt1cM'),
                'url': '1025749465611808768',
                'created': '2018-08-04T16:25:04+02:00',
                'modified': '2018-08-04T16:29:59+02:00',
                'data': [
                    {'key': 'user_name', 'value': 'Vera_Bergkamp'},
                    {'key': 'politician_id', 'value': 911},
                    {'key': 'politician.party_id', 'value': 3}
                ]
            }
        }

        with open('tests/data/politwoops.json', 'r') as in_file:
            content = in_file.read()
        data = json.loads(content)
        result = self.post_transformer.transform(data)
        self.assertEqual(result, expected)

    def test_transform_valid_post_politwoops_no_find_no_data(self):
        expected = {
            'application': 'politwoops',
            'payload': {
                'id': None,
                'title': (
                    'Fijn de steun voor de initiatiefwet van @D66 @PvdA &amp; '
                    '@groenlinks van het Kabinet @KajsaOllongren &amp; '
                    '@markharbers om… https://t.co/YBlgoGseOQ'),
                'description': (
                    'Fijn de steun voor de initiatiefwet van @D66 @PvdA &amp; '
                    '@groenlinks van het Kabinet @KajsaOllongren &amp; '
                    '@markharbers om artikel 1 vd #Grondwet uit te breiden! '
                    '\uf64f\uf3fb! Nog wel wat werk te doen samen met collega'
                    '’s @kirstenvdhul &amp; @NevinOzutok, maar dit is een '
                    'fijne stimulans!\uf44a\uf3fb\uf308 https://t.co/KwCjmGt1cM'),
                'url': '1025749465611808768',
                'created': '2018-08-04T16:25:04+02:00',
                'modified': '2018-08-04T16:29:59+02:00',
                'data': [
                    {'key': 'user_name', 'value': 'Vera_Bergkamp'},
                    {'key': 'politician_id', 'value': 911},
                    {'key': 'politician.party_id', 'value': 3}
                ]
            }
        }

        self.post_transformer.config[
            'binoas']['applications']['politwoops']['rules']['id'] = (
                'meta.original_object_id')

        with open('tests/data/politwoops.json', 'r') as in_file:
            content = in_file.read()
        data = json.loads(content)
        result = self.post_transformer.transform(data)
        self.assertEqual(result, expected)
