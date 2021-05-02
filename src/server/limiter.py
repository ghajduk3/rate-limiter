from flask import request, Response
import json
from time import time
import logging
logger = logging.getLogger(__name__)
class RateLimiter(object):

    def __init__(self, requests, period, storage=None):
        self.requests = requests
        self.period = period
        self.storage = {} if not storage else storage

    def __call__(self, func):
        def wrapped_func(*args,**kwargs):
            clientId = request.args.get("clientId", default=None)
            if clientId is not None:
                request_allowed = self.__is_request_allowed(clientId) if isinstance(self.storage,dict) else self.__is_request_allowed_redis(clientId)
                return Response(json.dumps({'message':'OK'}),status=200) if request_allowed else Response(json.dumps({'message':'Service Unavailable'}),status=503)
            else:
                return func(*args,**kwargs)
        return wrapped_func

    def __is_request_allowed_redis(self, key:str):
            if self.storage.setnx(key, 0):
                self.storage.expire(key, self.period)
            self.storage.incr(key)
            logger.info(
                "Client with id {} has issued a {} request at {} for the current timeframe started at {}".format(key,int(self.storage.get(key)),time(),self.storage.ttl(key)))
            print(int(self.storage.get(key)))
            return int(self.storage.get(key)) <= self.requests

    def __is_request_allowed(self, key: str)->bool:
        if self.__is_new_request(key):
            self.storage[key] = {
                'num_requests' : 1,
                'first_request' : time()
            }
        else:
            self.storage[key]['num_requests'] += 1
        logger.info(
            "Client with id {} has issued a {} request at {} for the current timeframe started at {}".format(key,self.storage[key]['num_requests'],time(),self.storage[key]['first_request']))

        return self.storage[key]['num_requests'] <= self.requests

    def __is_new_request(self,key: int)->bool:
        return (key not in self.storage or time() - self.storage[key]['first_request'] > self.period)
