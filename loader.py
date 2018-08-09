import sys
import logging

from worker import Consumer, start_worker


class Loader(Consumer):
    def output(self, transformed_message):
        logging.info('Should save to Elasticsearch now!')
        logging.info(transformed_message)

if __name__ == "__main__":
    start_worker(sys.argv, Loader)
