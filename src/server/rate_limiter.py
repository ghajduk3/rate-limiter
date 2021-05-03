import logging
from abc import ABCMeta, abstractmethod
from time import time

logger = logging.getLogger(__name__)


class RateLimiterBase(metaclass=ABCMeta):
    """
      Abstract base class that represents rate limiter. Rate limiter works on a fixed window principle.
      It takes the number of requests that are allowed for a fixed time frame as arguments.
      Requests that are exceeding the number of allowed requests per time frame get disregarded.
      ```
      Attributes
      ----------
      requests : int
          the number of allowed requests for a time frame
      period : int
          the number of seconds defining the time frame
      storage : Optional[Redis]
          type of storage to be used. It is either a Redis or a local dictionary.

      Methods
      -------
      is_request_allowed(key: str) -> bool
          checks whether the requests is within a specified time frame
           and/or whether it exceeds the limit of allowed requests.
      """
    def __init__(self, requests, period, storage=None):
        """
        Parameters
        ----------
        requests : int
            the number of allowed requests for a time frame
        period : int
            the number of seconds defining the time frame
        storage : Optional[Redis]
            type of storage to be used. It is either a Redis or a local dictionary.
        """
        self.requests = requests
        self.period = period
        self.storage = {} if not storage else storage

    @abstractmethod
    def is_request_allowed(self, key: str) -> bool:
        pass


class RateLimiterLocal(RateLimiterBase):
    """
    Class that represents implementation of RateLimiterBase class. It uses python dictionary for storage.
    """
    def __init__(self, requests, period):
        super().__init__(requests, period)

    def is_request_allowed(self, key: str) -> bool:
        """
        Checks whether a request with a given key is allowed.

        Parameters
        ----------
        key : str
            key identifier of a given request.

        Returns
        ------
        flag : bool
            indicates whether the request is allowed.
        """
        if self.__is_new_request(key):
            self.storage[key] = {
                'num_requests': 1,
                'first_request': time()
            }
        else:
            self.storage[key]['num_requests'] += 1
        logger.info(f"Client with id {key} has issued a {self.storage[key]['num_requests']} request at"
                    f" {time()} for the current timeframe started at {self.storage[key]['first_request']}")

        return self.storage[key]['num_requests'] <= self.requests

    def __is_new_request(self, key: str) -> bool:
        """
        Indicates whether a request for a given key is a new request.

        Checks if the key does not exist, or if the current time frame is passed. In latter case it creates a new, active time frame.

        Parameters
        ----------
        key : str
            key identifier of a given request.

        Returns
        ------
        flag : bool
            indicates whether the request is new.
        """
        return (key not in self.storage or time() - self.storage[key]['first_request'] > self.period)


class RateLimiterRedis(RateLimiterBase):
    """
    Class that represents implementation of RateLimiterBase class. It uses Redis server for storage.
    """
    def __init__(self, requests, period, storage):
        super().__init__(requests, period, storage=storage)

    def is_request_allowed(self, key: str) -> bool:
        """
        Checks whether a request with a given key is allowed.

        Parameters
        ----------
        key : str
            key identifier of a given request.

        Returns
        ------
        flag : bool
            indicates whether the request is allowed.
        """
        if self.storage.setnx(key, 0):
            self.storage.expire(key, self.period)
        self.storage.incr(key)
        logger.info(f"Client with id {key} has issued a {int(self.storage.get(key))} "
                    f"request at {time()} for the current timeframe started at {self.storage.ttl(key)}")
        return int(self.storage.get(key)) <= self.requests



