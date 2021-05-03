from flask import request, Response
import json
import logging
logger = logging.getLogger(__name__)


class RateLimiter(object):
    """
    Class that represents a Rate Limiter decorator.
    """

    def __init__(self, rate_limiter):
        self.limiter = rate_limiter

    def __call__(self, func):
        def wrapped_func(*args, **kwargs):
            client_id = request.args.get("clientId", default=None)
            if client_id is not None:
                request_allowed = self.limiter.is_request_allowed(client_id)
                if request_allowed:
                    return Response(json.dumps({'message': 'OK'}), status=200)
                else:
                    return Response(json.dumps({'message': 'Service Unavailable'}), status=503)
            else:
                return func(*args, **kwargs)
        return wrapped_func
