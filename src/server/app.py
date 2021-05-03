from flask import Flask
from limiter import RateLimiter
import logging
import redis
from redis_client import RedisClient
logger = logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)

app = Flask(__name__)
redis_client = RedisClient()
redis_connection = redis_client.get_connection()

@app.route('/api', methods = ['GET'])
@RateLimiter(requests=5, period=5, storage=redis_connection)
def get_request():
    return 'Zemanta project!'

if __name__ == '__main__':
    app.run(host ='0.0.0.0', port=5001, debug = True)
