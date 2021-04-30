from flask import request, Response
import json
import time
from datetime import datetime, timedelta

class RateLimiter(object):

    def __init__(self, requests, period):
        self.requests = requests
        self.period = period
        self.storage = {}

    def __call__(self, func):
        def wrapped_func(*args,**kwargs):
            clientId = request.args.get("clientId", default=None, type=int)
            if clientId is not None:
                return Response(json.dumps({'message':'OK'}),status=200) if self.__is_call_allowed(clientId) else Response(json.dumps({'message':'Service Unavailable'}),status=503)
            else:
                return func(*args,**kwargs)
        return wrapped_func

    def __is_call_allowed(self, key: int)->bool:
        if self.__is_new_call(key):
            self.storage[key] = {
                'num_requests' : 1,
                'last_request' : datetime.utcnow()
            }
        else:
            self.storage[key]['num_requests'] +=1

        return self.storage[key]['num_requests'] < self.requests

    def __is_new_call(self,key: int)->bool:
        return (key not in self.storage or datetime.utcnow() - self.storage[key]['last_request'] > timedelta(seconds = self.period))


