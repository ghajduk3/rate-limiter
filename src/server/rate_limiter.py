from abc import ABCMeta, abstractmethod
from flask import request, Response
import json
from time import time
import logging
logger = logging.getLogger(__name__)

class RateLimiterBase(metaclass=ABCMeta):

    def __init__(self, requests, period, storage=None):
        self.requests = requests
        self.period = period
        self.storage = {} if not storage else storage

    @abstractmethod
    def is_request_allowed(self):
        pass

class RateLimiterLocal(RateLimiterBase):

    def __init__(self, requests, period):
        super().__init__(requests,period)

    def is_request_allowed(self, key):
        if self.__is_new_request(key):
            self.storage[key] = {
                'num_requests' : 1,
                'first_request' : time()
            }
        else:
            self.storage[key]['num_requests'] += 1
        logger.info("Client with id {} has issued a {} request at {} for the current timeframe started at {}".format(key,self.storage[key]['num_requests'],time(),self.storage[key]['first_request']))

        return self.storage[key]['num_requests'] <= self.requests

    def __is_new_request(self,key: int)->bool:
        return (key not in self.storage or time() - self.storage[key]['first_request'] > self.period)

class RateLimiterRedis(RateLimiterBase):

    def __init__(self, requests, period, storage):
        super().__init__(requests, period, storage=storage)

    def is_request_allowed(self, key):
        if self.storage.setnx(key, 0):
            self.storage.expire(key, self.period)
        self.storage.incr(key)
        logger.info("Client with id {} has issued a {} request at {} for the current timeframe started at {}".format(key,int(self.storage.get(key)),time(),self.storage.ttl(key)))
        return int(self.storage.get(key)) <= self.requests




