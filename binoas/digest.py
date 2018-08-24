#!/usr/bin/env python

import logging

from elasticsearch.exceptions import NotFoundError
from elasticsearch.helpers import scan

from binoas.es import setup_elasticsearch


class Digest:
    def __init__(self, config):
        self.config = config
        self.es = setup_elasticsearch(self.config)

    def make(self, application):
        if application not in self.config['binoas']['applications']:
            raise ValueError('Application could not be found')

        es_query = {
            "query": {
                "range": {
                    "modified": {
                        "gte": "now-1d/d",
                        "lt":  "now/d"
                    }
                }
            }
        }
        index_name = 'binoas_%s' % (application,)

        try:
            results = [r for r in scan(self.es, es_query, index=index_name, doc_type='item')]
        except NotFoundError as e:
            results = None
        logging.info(results)
