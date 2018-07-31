#!/usr/bin/env python
import threading
import logging
import time
import multiprocessing

from kafka import KafkaConsumer, KafkaProducer

from utils import load_config


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
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        self.config = load_config()

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(
            bootstrap_servers=self.config['binoas']['zookeeper'],
            auto_offset_reset='earliest', consumer_timeout_ms=1000)
        # FIXME: allow to set the topic in the config
        consumer.subscribe(['topic'])

        while not self.stop_event.is_set():
            for message in consumer:
                logging.info(self.config['binoas']['applications'])
                logging.info(message)
                if self.stop_event.is_set():
                    break

        consumer.close()


def main():
    tasks = [
        # Producer(),
        Consumer()
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
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
    main()
