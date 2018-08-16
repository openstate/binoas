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

    words = 'dit is een lijst van onzinnige woorden'.split()
    alert = random.choice(words)

    subscription = {
        'application': 'test',
        'email': email,
        'frequency': '6H',
        'subscription': {
            'title': alert
        }
    }
    print(requests.post(
        'http://app:5000/subscriptions/new',
        data=json.dumps(subscription)).json())
    # u, q = Subscription(subscription).save()

if __name__ == '__main__':
    main()
