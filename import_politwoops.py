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

    for p in range(1, 50):
        logging.info('Getting page %s' % (p,))
        data = requests.get(
            'https://www.politwoops.nl/index.json?page=%s' % (p,)).json()
        for t in data['tweets']:
            requests.post(
                'http://app:5000/posts/new',
                data=json.dumps({'application': 'politwoops', 'payload': t}))

if __name__ == '__main__':
    main()
