#!/usr/bin/env python

import logging
import uuid
import json
import random

import requests

# from binoas.utils import load_config
# from binoas.db import setup_db
# from binoas.es import setup_elasticsearch
# from binoas.subscriptions import Subscription


def main():
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO)

    # config = load_config()
    # session = setup_db(config)
    # print(session)
    # es = setup_elasticsearch(config)

    prefix = str(uuid.uuid4())
    email = '%s@bje.dds.nl' % (prefix.replace('-', ''))
    print(email)

    subscription_options = {
        'title': {
            'title': random.choice(
                'dit is een lijst die bestaat uit onzinnige woorden'.split())
        },
        'topic': {
            'data.key': 'topic',
            'data.value': random.choice('tag1 tag2'.split())
        }
    }
    fld = random.choice(list(subscription_options.keys()))
    print(fld)

    subscription = {
        'application': 'politwoops',
        'email': email,
        'frequency': '6H',
        'subscription': subscription_options[fld]
    }
    print(requests.post(
        'http://app:5000/subscriptions/new',
        data=json.dumps(subscription)).json())
    # u, q = Subscription(subscription).save()

if __name__ == '__main__':
    main()
