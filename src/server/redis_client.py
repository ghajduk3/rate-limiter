import os
import redis
import logging
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)


class RedisClient(object):
    """
    A singleton pattern class which represents RedisClient.

    Methods
    -------
    get_connection()
        Return an open established connection to Redis server.
    """
    REDIS_URL = os.getenv("REDIS_URL")
    _instance = None

    def get_connection(self):
        return self._redis

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            try:
                cls._redis = redis.StrictRedis.from_url(cls.REDIS_URL)
            except redis.exceptions.ConnectionError:
                logger.exception("An error has occured while connecting to Redis server!")
            except Exception:
                logger.exception("Unexpected error")
        return cls._instance
