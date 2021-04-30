from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    print(request.headers)
    return 'Zemanta project!'


if __name__ == '__main__':
    app.run()
