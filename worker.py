#!/usr/bin/env python
import sys

from binoas.workers import registry, start_worker

if __name__ == "__main__":
    klass = registry[sys.argv[1]]
    start_worker(sys.argv, klass)
