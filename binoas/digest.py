#!/usr/bin/env python

import json
import logging

from elasticsearch.exceptions import NotFoundError
from elasticsearch.helpers import scan

from kafka import KafkaProducer

from binoas.es import setup_elasticsearch
from binoas.db import setup_db
from binoas.models import User, UserQueries
from binoas.mixins import ProducerMixin


class Digest(ProducerMixin):
    def __init__(self, config):
        self.config = config
        self.role = 'subfetcher'
        self.es = setup_elasticsearch(self.config)
        self.db = setup_db(self.config)
        self.init_producer()

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
            scan_results = [
                r for r in scan(
                    self.es, es_query, index=index_name, doc_type='item')]
        except NotFoundError:
            scan_results = []

        if len(scan_results) <= 0:
            return

        for r in scan_results:
            req_head, req_body = self._make_percolate_query(index_name, r)
            perc_req += '%s \n' % (json.dumps(req_head),)
            perc_req += '%s \n' % (json.dumps(req_body),)

        try:
            results = self.es.msearch(body=perc_req)
        except ValueError as e:
            results = {'responses': []}

        queries = {}
        for d, r in zip(scan_results, results['responses']):
            if r['hits']['total'] <= 0:
                continue
            #logging.info('Document %s' % (d['_id'],))
            for q in r['hits']['hits']:
                #logging.info('* %s' % (q['_id'],))
                try:
                    queries[q['_id']]['documents'].append(d['_source'])
                except LookupError:
                    queries[q['_id']] = {
                        'query': q['_source'],
                        'documents': [d['_source']]
                    }

        user_queries = self.db.query(UserQueries).filter(
            UserQueries.query_id.in_(queries.keys())
        ).filter(
            UserQueries.frequency == None
        ).all()
        logging.info('Found user queries:')
        logging.info([u.user_id for u in user_queries])

        users_with_queries = {}
        for uq in user_queries:
            try:
                users_with_queries[uq.user_id].append(uq)
            except LookupError:
                users_with_queries[uq.user_id] = [uq]

        for user_id, uq in users_with_queries.items():
            logging.info(
                '%s alert for %s with ids : %s and %s documents' % (
                    application, uq[0].user.email,
                    [u.query_id for u in uq],
                    sum([len(queries[q]['documents']) for q in [u.query_id for u in uq]])))
            pl = {
                'application': application,
                'payload': {
                    'alerts': [
                        queries[u.query_id] for u in users_with_queries[user_id]],
                    'user': {
                        'id': uq[0].user_id,
                        'email': uq[0].user.email
                    }
                }
            }

            self.produce_message(pl)
