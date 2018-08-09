#!/usr/bin/env python
import sys

from binoas.workers import Loader, start_worker

if __name__ == "__main__":
    start_worker(sys.argv, Loader)
