import threading
import uuid
import requests
import time
from threading import Thread
import logging
logger = logging.getLogger(__name__)

class HttpJob(Thread):
    shutdownEvent = threading.Event()
    def __init__(self,url,clientId):
        Thread.__init__(self)
        self.clientId = clientId
        self.url = url

    def run(self):
        params = {'clientId': self.clientId}
        while True:
            if self.shutdownEvent.is_set():
                break
            logger.info("Client with id {} has issued a request.".format(self.clientId))
            resp = HttpJob.create_request(self.url,params=params)
            logger.info("Client with id {} has received a response {} with status code {}.".format(self.clientId,resp.json()['message'],resp.status_code))
            time.sleep(0.5)
    @staticmethod
    def create_request(url, params):
        return requests.get(url,params=params)

class HttpPool(object):
    def __init__(self,num_threads):
        self.threadNumber = num_threads
        self.__jobName = None
        self.threads = []

    def initialize(self, job, **kwargs):
        self.__job = job
        self.threads = [job(kwargs['url'], uuid.uuid4()) for ind in range(self.threadNumber)]
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()
        logger.info("Pool with {} threads has been initialized.".format(self.threadNumber))

    def terminate(self):
        self.__job.shutdownEvent.set()
        logger.info("Pool has been terminated.")

