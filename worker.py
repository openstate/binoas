#!/usr/bin/env python
import threading
import itertools
import logging
import time
import multiprocessing
import sys

from kafka import KafkaConsumer, KafkaProducer

from binoas.utils import load_config


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
    def __init__(self, role):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        self.role = role
        self.config = load_config()

    def stop(self):
        self.stop_event.set()

    def run(self):
        self.consumer = KafkaConsumer(
            bootstrap_servers=self.config['binoas']['zookeeper'],
            auto_offset_reset='earliest', consumer_timeout_ms=1000)

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
            self.producer = KafkaProducer(bootstrap_servers='kafka')
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
        return message.value

    def output(self, transformed_message):
        logging.info(transformed_message)
        if self.producer is not None:
            for t in self.topics_out:
                self.producer.send(t, transformed_message)


def start_worker(argv, klass):
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO)

    role = argv[1]
    logging.info('Starting up with role : %s' % (role,))

    tasks = [
        klass(role)
    ]

    for t in tasks:
        t.start()

    while True:
        time.sleep(10)

    for task in tasks:
        task.stop()

    for task in tasks:
        task.join()


if __name__ == "__main__":
    start_worker(sys.argv, Consumer)
