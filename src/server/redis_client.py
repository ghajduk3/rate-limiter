import os

from redis import StrictRedis
from dotenv import load_dotenv
load_dotenv()
_connection = None

def get_redis_connection():
    global _connection
    if _connection is None:
        print(os.getenv('REDIS_URL'))
        _connection = StrictRedis.from_url(os.getenv('REDIS_URL'))
    return _connection