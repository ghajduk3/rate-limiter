import os
from redis import StrictRedis
from dotenv import load_dotenv
load_dotenv()


class RedisClient(object):
    REDIS_URL = os.getenv("REDIS_URL")
    _instance = None

    def get_connection(self):
        return self._redis

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._redis = StrictRedis.from_url(cls.REDIS_URL)
        return cls._instance
