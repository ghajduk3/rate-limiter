import os
from exceptions import ServiceException
import signal
import argparse
from dotenv import load_dotenv
from multithread import HttpJob, HttpPool
import logging
logger = logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
load_dotenv()


def signal_handler(signum, frame):
    raise ServiceException("Program is interrupted!")


def process_args():
    parser = argparse.ArgumentParser(description="CLI application for creating and generating HTTP requests. Specified number of clients is created, each within its own thread. Each client continously generates HTTP requests to the web url specified within .env file. Clients are to be gracefully stopped by pressing CTRL + C keyboard combination.")
    parser.add_argument('-c', '--clients', required=True, default=1, type=int, help="Number of HTTP clients to be created.")
    return parser.parse_args()


def main():
    global pool
    signal.signal(signal.SIGINT, signal_handler)
    args = process_args()
    try:
        pool = HttpPool(args.clients)
        pool.initialize(HttpJob, url=os.getenv('WEBSITE_URL'))
    except ServiceException:
        if isinstance(pool, HttpPool):
            pool.terminate()


if __name__ == '__main__':
    main()
