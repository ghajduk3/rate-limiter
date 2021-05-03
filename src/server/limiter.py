from flask import request, Response
import json
from time import time
from rate_limiter import RateLimiterLocal, RateLimiterRedis
import logging
logger = logging.getLogger(__name__)


class RateLimiter(object):

    def __init__(self, requests, period, storage=None):
        self.requests = requests
        self.period = period
        self.storage = storage

    @property
    def limiter(self):
        if isinstance(self.storage, dict):
            return RateLimiterLocal(self.requests, self.period)
        else:
            return RateLimiterRedis(self.requests, self.period, self.storage)

    def __call__(self, func):
        def wrapped_func(*args,**kwargs):
            clientId = request.args.get("clientId", default=None)
            if clientId is not None:
                request_allowed = self.limiter.is_request_allowed(clientId)
                if request_allowed:
                    return Response(json.dumps({'message':'OK'}),status=200)
                else:
                    return Response(json.dumps({'message':'Service Unavailable'}),status=503)
            else:
                return func(*args,**kwargs)
        return wrapped_func
