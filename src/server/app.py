from flask import Flask
from flask import request
from limiter import RateLimiter

app = Flask(__name__)


# @app.route('/api/',defaults= {'clientid' : '5'})
@app.route('/api', methods = ['GET'])
@RateLimiter(requests=5,period=5)
def get_request():

    return 'Zemanta project!'


if __name__ == '__main__':
    app.run()
