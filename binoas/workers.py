#!/usr/bin/env python
import threading
import itertools
import logging
import time
import multiprocessing
import sys
import json

from kafka import KafkaConsumer, KafkaProducer

from binoas.utils import load_config
from binoas.transformers import JSONPathPostTransformer
from binoas.es import setup_elasticsearch
from binoas.db import setup_db
from binoas.mixins import ConsumerMixin, ProducerMixin
from binoas.models import User, UserQueries
from binoas.mail import send_mail
from binoas.template import Templater


class Consumer(multiprocessing.Process, ConsumerMixin, ProducerMixin):
    """
    A class which acts as a consumer of one or more Kafka topic(s). It is
    intended to be generic and it's behavior can be altered in subclasses.
    This class basically acts as a simple transformer from one topic (input)
    to output topics. It has a transform method which does not do anything.
    """
    def __init__(self, role, group=None):
        """
        Initializes the process. The role is passed to give more information.
        """
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        self.role = role
        self.group = group
        self.config = load_config()

    def stop(self):
        self.stop_event.set()

    def run(self):
        """
        Runs the consumer. This is basically a never stopping routine.
        """

        if self.group is not None:
            logging.info('Running as group: %s' % (self.group,))

        self.init_consumer()
        self.init_producer()

        while not self.stop_event.is_set():
            for message in self.consumer:
                transformed = self.transform(message)
                self.output(transformed)
                if self.stop_event.is_set():
                    break

        self.consumer.close()

    def transform(self, message):
        """
        Transform the message. Currently simply returns the value (Ie. it is
        not altered).
        """
        return message.value

    def output(self, transformed_message):
        """
        This is a routine that outputs the transformed messages if there
        is an Kafka output topic defined.
        """
        self.produce_message(transformed_message)


class JSONTransformer(Consumer):
    """
    This transformer applies a json path transformer and return the result.
    """
    def __init__(self, role, group=None):
        super().__init__(role, group)
        self.transformer = JSONPathPostTransformer(self.config)

    def transform(self, message):
        try:
            return self.transformer.transform(message.value)
        except ValueError as e:
            logging.error(e)


class ElasticsearchBaseConsumer(Consumer):
    """
    Base class for consumers that works with Elasticsearch. Makes the
    Elasticsearch connection available in the consumer.
    """
    def __init__(self, role, group=None):
        super().__init__(role, group)
        self.es = setup_elasticsearch(self.config)


class ElasticsearchLoader(ElasticsearchBaseConsumer):
    """
    This class loads the messages in an Elasticsearch store, as specified in
    the configuration file.
    """
    def output(self, transformed_message):
        logging.info('Should save to Elasticsearch now!')
        logging.info(transformed_message)

        # Index documents into new index
        index_name = 'binoas_%s' % (transformed_message['application'],)
        doc_type = 'item'
        object_id = transformed_message['payload']['id']

        self.es.index(
            index=index_name, doc_type=doc_type,
            body=transformed_message['payload'], id=object_id)


class ElasticsearchPercolator(ElasticsearchBaseConsumer):
    """
    This class uses the Elasticsearch percolator function to find alerts
    """
    def transform(self, message):
        index_name = 'binoas_%s' % (message.value['application'],)
        doc_type = 'item'
        results = self.es.search(index=index_name, body={
            "query": {
                "percolate": {
                    "field": "query",
                    "document_type": doc_type,
                    "document": message.value['payload']
                }
            },
            "highlight": {
                "fields": {
                    "*": {}
                }
            }
        })

        if results['hits']['total'] > 0:
            return {
                'application': message.value['application'],
                'payload': message.value['payload'],
                'alerts': results
            }


class DatabaseBaseConsumer(Consumer):
    """
    Base class for consumers that works with the database. Makes the
    database connection available in the consumer.
    """
    def __init__(self, role, group=None):
        super().__init__(role, group)
        self.db = setup_db(self.config)


class DatabaseSubscriberFetcher(DatabaseBaseConsumer):
    def transform(self, message):
        query_ids = {
            h['_id']: h for h in message.value['alerts']['hits']['hits']}
        logging.info('Found queries:')
        logging.info(query_ids)

        user_queries = self.db.query(UserQueries).filter(
            UserQueries.query_id.in_(query_ids.keys())
        ).filter(
            UserQueries.frequency == None
        ).all()
        logging.info('Found user queries:')
        logging.info([u.user_id for u in user_queries])

        result = []
        for u in user_queries:
            result.append({
                'application': message.value['application'],
                'payload': {
                    'alerts': [
                        {
                            # FIXME: put query title/desc here ...
                            'query': query_ids[u.query_id],
                            'documents': [
                                message.value['payload']
                            ],
                        }
                    ],
                    'user': {
                        'id': u.user_id,
                        'email': u.user.email
                    }
                }
            })
        return result

    def output(self, transformed_message):
        """
        This is a routine that outputs the transformed messages if there
        is an Kafka output topic defined.
        """

        if transformed_message is None:
            return

        if self.producer is not None:
            for r in transformed_message:
                for t in self.topics_out:
                    if 'user' in r:
                        logging.info('Producing to channel: %s (u: %s/%s)' % (
                            t, r['user']['id'], r['user']['email'],))
                    logging.info(r)
                    self.producer.send(t, r)


class Mailer(Consumer):
    def output(self, transformed_message):
        logging.info(transformed_message)
        if transformed_message is None:
            return
        if 'user' not in transformed_message['payload']:
            logging.info('Discarding message (no user in payload)')
            return

        if 'application' not in transformed_message:
            logging.info('Discarding message (no valid application specification)')
            return

        logging.info('Should go and send an email to %s now!' % (
            transformed_message['payload']['user']['email'],))

        templater = Templater(self.config)
        content = templater.compile(transformed_message)

        send_mail(
            self.config['binoas']['sendgrid']['api_key'],
            '[%s] new alert' % (transformed_message['application'],),
            content, [transformed_message['payload']['user']['email']])


def start_worker(argv, klass):
    """
    This routine starts a worker with the given class.
    """
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO)

    role = argv[1]
    logging.info('Starting up with role : %s' % (role,))

    if len(argv) > 2:
        group = argv[2]
    else:
        group = None

    tasks = [
        klass(role, group)
    ]

    for t in tasks:
        t.start()

    while True:
        time.sleep(10)

    for task in tasks:
        task.stop()

    for task in tasks:
        task.join()

registry = {
    'transformer': JSONTransformer,
    'loader': ElasticsearchLoader,
    'percolator': ElasticsearchPercolator,
    'subfetcher': DatabaseSubscriberFetcher,
    'mailer': Mailer
}
