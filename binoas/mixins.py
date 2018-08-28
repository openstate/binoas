#!/usr/bin/env python

import itertools
import json
import logging

from kafka import KafkaConsumer, KafkaProducer


class KafkaBaseMixin:
    def get_topics(self, direction='in'):
        return list(set(itertools.chain.from_iterable(
            [
                a['routes'][self.role]['topics'].get(direction, []) for k, a in
                self.config['binoas']['applications'].items()])))


class ConsumerMixin(KafkaBaseMixin):
    def topics_in():
        doc = "The topics property."

        def fget(self):
            return self.get_topics('in')

        return locals()
    topics_in = property(**topics_in())

    def init_consumer(self):
        if len(self.topics_in) <= 0:
            logging.info('Not consuming any topics')
            self.consumer = None
            return

        self.consumer = KafkaConsumer(
            bootstrap_servers=self.config['binoas']['zookeeper'],
            auto_offset_reset='earliest', consumer_timeout_ms=1000,
            value_deserializer=json.loads, group_id=self.group)
        logging.info('Consuming topics: %s' % (self.topics_in,))
        self.consumer.subscribe(self.topics_in)


class ProducerMixin:
    def topics_out():
        doc = "The topics property."

        def fget(self):
            return self.get_topics('out')

        return locals()
    topics_out = property(**topics_out())

    def init_producer(self):
        if len(self.topics_out) <= 0:
            logging.info('Not setting up producers')
            self.producer = None
            return

        self.producer = KafkaProducer(
            bootstrap_servers='kafka',
            value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        logging.info('Producing for topics: %s' % (self.topics_out,))

        def produce_message(self, transformed_message):
            logging.debug(transformed_message)

            if transformed_message is None:
                return

            if self.producer is not None:
                for t in self.topics_out:
                    logging.info('Producing to channel: %s' % (t,))
                    self.producer.send(t, transformed_message)
