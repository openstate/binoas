#!/usr/bin/env python

import json
import logging

from elasticsearch.exceptions import NotFoundError
from elasticsearch.helpers import scan

from binoas.es import setup_elasticsearch


class Digest:
    def __init__(self, config):
        self.config = config
        self.es = setup_elasticsearch(self.config)

    def _make_percolate_query(self, index_name, r):
        return {
                "index": index_name,
                "type": "queries"
            }, {
                "query": {
                    "percolate": {
                        "field": "query",
                        "document_type": 'item',
                        "document": r['_source']
                    }
                },
                "highlight": {
                    "fields": {
                        "*": {}
                    }
                }
            }

    def make(self, application):
        if application not in self.config['binoas']['applications']:
            raise ValueError('Application could not be found')

        es_query = {
            "query": {
                "range": {
                    "modified": {
                        "gte": "now-365d/d",
                        "lt":  "now/d"
                    }
                }
            }
        }
        index_name = 'binoas_%s' % (application,)

        perc_req = ''
        try:
            for r in scan(self.es, es_query, index=index_name, doc_type='item'):
                req_head, req_body = self._make_percolate_query(index_name, r)
                perc_req += '%s \n' % (json.dumps(req_head),)
                perc_req += '%s \n' % (json.dumps(req_body),)
        except NotFoundError:
            pass

        try:
            results = self.es.msearch(body=perc_req)
        except ValueError as e:
            results = {'responses': []}

        for r in results['responses']:
            if r['hits']['total'] > 0:
                logging.info(r)
