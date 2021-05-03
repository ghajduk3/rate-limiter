import threading
import uuid
import requests
import time
import logging
from threading import Thread
from typing import List
logger = logging.getLogger(__name__)


class HttpJob(Thread):
    """
    Class that represents an HttpClient instantiated within a new thread.

    Attributes
    ----------
    url : str
        url to which the http client is to connect and issue requests.
    clientId : str
        client identifier through which http requests are to be issued.
    shutdownEvent: threading.Event
        threading.Event object which allows thread to be gracefully terminated.

    Methods
    -------
    run()
        continously making http requests with 0.5s pause between requests to the specified url with a specified client id.

    create_request(url: str, params: dict) -> Response
        makes a single HTTP GET request to the specified url with specified params.
        Returns a requests.response
    """
    shutdownEvent = threading.Event()

    def __init__(self, url, client_id):
        """
        Parameters
        ----------
        url : str
            url to which the http client is to connect and issue requests.
        client_id : str
            client identifier through which http requests are to be issued.
        """
        Thread.__init__(self)
        self.clientId = client_id
        self.url = url

    def run(self):
        """
        Continously making http requests with 0.5s pause between requests to the specified url with a specified client id.
        It gets envoked on HttpJob.start().
        """
        params = {'clientId': self.clientId}
        while True:
            if self.shutdownEvent.is_set():
                break
            logger.info(f"Client with id {self.clientId} has issued a request.")
            resp = HttpJob.create_request(self.url, params=params)
            logger.info(f"Client with id {self.clientId} has received a response "
                        f"{resp.json()['message']} with status code {resp.status_code}.")
            time.sleep(0.5)

    @staticmethod
    def create_request(url, params):
        """
        makes a single HTTP GET request to the specified url with specified params.
        Returns a requests.response

        Parameters
        ----------
        url : str
            url to which the http client is to connect and issue requests.
        params : dict
            a dictionary with query strings to be send with HTTP GET request.

        Returns
        -------
        requests.Response
            return Response object
        """
        return requests.get(url, params=params)


class HttpPool(object):
    """
    Class that represents a pool of threads.

    It creates a specified number of HttpJob clients, each within it's own thread with a uniquely generated id.

    Attributes
    ----------
    threadNumber : int
        number of threads(clients) to be instantiated.
    threads : List
        A pool of instantiated threads.
    __job: HttpJob
        an HttpJob object used to set shutdownEvent indicator

    Methods
    -------
    initialize(job, **kwargs)
        Initializes a pool of threads,

    terminate()
        Sets the shutdown flag in a extended thread class in order to gracefully stops all running threads.
    """

    def __init__(self, num_threads: int):
        """
        Parameters
        ----------
        num_threads : int
            number of threads(clients) to be instantiated.
        """
        self.threadNumber = num_threads
        self.threads = []
        self.__job = None

    def initialize(self, job, **kwargs):
        """
        Initializes a pool of threads(jobs) with given arguments.
        """
        self.__job = job
        self.threads = [job(kwargs['url'], uuid.uuid4()) for ind in range(self.threadNumber)]
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()
        logger.info(f"Pool with {self.threadNumber} threads has been initialized.")

    def terminate(self):
        """
        Gracefully terminates running threads.
        """
        self.__job.shutdownEvent.set()
        logger.info("Pool has been terminated.")