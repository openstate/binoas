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


class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.config = load_config()

    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers='kafka')

        while not self.stop_event.is_set():
            producer.send('my-topic', b"test")
            producer.send('my-topic', b"\xc2Hola, mundo!")
            time.sleep(1)

        producer.close()


class Consumer(multiprocessing.Process):
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
        self.consumer = KafkaConsumer(
            bootstrap_servers=self.config['binoas']['zookeeper'],
            auto_offset_reset='earliest', consumer_timeout_ms=1000,
            value_deserializer=json.loads, group_id=self.group)

        self.topics_in = list(set(itertools.chain.from_iterable(
            [
                a['routes'][self.role]['topics'].get('in', []) for k, a in
                self.config['binoas']['applications'].items()])))
        logging.info('Consuming topics: %s' % (self.topics_in,))
        self.consumer.subscribe(self.topics_in)

        self.topics_out = list(set(itertools.chain.from_iterable(
            [
                a['routes'][self.role]['topics'].get('out', []) for k, a in
                self.config['binoas']['applications'].items()])))

        if len(self.topics_out) > 0:
            logging.info('Producing for topics: %s' % (self.topics_out,))
            self.producer = KafkaProducer(
                bootstrap_servers='kafka',
                value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        else:
            logging.info('Not setting up producers')
            self.producer = None

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
        logging.info(transformed_message)

        if transformed_message is None:
            return

        if self.producer is not None:
            for t in self.topics_out:
                logging.info('Producing to channel: %s' % (t,))
                self.producer.send(t, transformed_message)


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
        return {
            'application': message.value['application'],
            'payload': message.value['payload'],
            'alerts': results
        }


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
