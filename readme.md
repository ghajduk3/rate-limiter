# ZEMANTA BACKEND ENGINEER CHALLENGE
##### author: Gojko Hajdukovic, 05.2021

Table of contents:
1. [Introduction](#introduction)
2. [Setup](#setup)
3. [Description](#setup)

<a name="introduction"></a>
### Introduction
This project implements a simple HTTP Denial-of-service protection system.


<a name="setup"></a>
### Setup
These instructions assume that the user is in repo's root.
```shell script
cd <repo_root>
```

**Running the app locally**
1. In order to set-up virtual environment issue:
```shell script
python -m venv venv
#Activate the environment
source venv/bin/activate
```
2. To install project related dependencies issue:
```shell script
pip3 install -r requirements.txt
sudo apt-get install redis-server
```
3. In order to use `redis` for storage, in the development environment issue:
```shell script
docker run --name redis-serv -d redis redis-server --appendonly yes
```
4. After all the project related dependencies have been successfully installed, we can start the `Flask` server by issuing:
```shell script
python src/server/app.py
```
5. With server successfully started, issue following commands and fill in the .env file with the valid url and port exposed by the server. For redis-server usage in the dev environment keep the pre-defined configuration.
```shell script
cp .env.example .env
```
6. In order to run client cli application with help description issue:
```shell script
python src/client/cli.py --help
```

**Running the app with docker**
This project builds up three docker images, a `base` image which sets up the environment and project related dependencies, a client and a server one.
All the three pre-built images are publicly available at [dockerHub](https://hub.docker.com/u/ghajduk3).

#### Re-building the images locally 

Since, the client CLI application requires communication to the server application,
we create a docker network to set up inter-container visibility.
1. To create a docker network issue:
```shell script
docker network create <network-name>
```
After the images are run and the containers are built within a same network they become visible to each-other by the container name.

2. To re-build all images issue:
```shell script
docker-compose build --no-cache
```

#### Pulling the images from docker hub
1. In order to pull pre-built images issue:
```shell script
docker pull ghajduk3/rate-limiter-server
docker pull ghajduk3/rate-limiter-client
```

#### Running images
1. First, in order to use `redis`, we pull pre-built image from dockerHub by issuing:
```shell script
docker run --network <network-name> -p 6379:6379--name <container-name> -d redis redis-server --appendonly yes
```   
After the redis container has been created, copy the `.env.example` to `.env` and change the base part of `REDIS_URL` to `<container-name>` afore created, i.e REDIS_URL = redis://<container-name>:6379 

2. Second, we need to run a `rate-limiter-server`. In order to run a docker container issue:
```shell script
docker run --network <network-name> -p 5001:5001 --name <container-name> ghajduk3/rate-limiter-server
```
After the server has successfully started change the base_url part of `WEBSITE_URL` to the afore created `<container_name>`, i.e `WEBSITE_URL=http://<container-name>:5001/api`.

3. In order to run a `rate-limiter-client` CLI application with help description issue:
```shell script
docker run --network <network-name> --name <container-name> ghajduk3/rate-limiter-client --help
```
<a name="description"></a>
### Description
In the following subsections I present a brief description of the project.
####Tech stack used
* Python
* Flask
* Redis

####Server module
**Rate Limiter**

`RateLimiter` serves as a simple denial-of-service protection system.
It is implemented based on a fixed window principle, which discards all the requests coming from the specific client that exceed the limit of requests for a given timeframe.

The implementation  exposes two classes  `RateLimiterLocal` and `RateLimiterRedis`  that differ in the type of the storage used.
`RateLimiterLocal` stores its computational data in a `dictionary` while `RateLimitRedis` uses Redis for storing computational data. 
Both classes accept number `requests` and the duration of a timeframe `period` specified in seconds, while `RateLimiterRedis` in addition takes established connection to Redis.

For usage convenience a `RateLimiter` is additionaly exposed as a `python decorator`. The decorator takes instantiated object of afore described `RateLimiters` as an argument. 
In the current implementation `RateLimiter` decorator is to be used with HTTP endpoints that receive `clientId` query parameter.

Usage:
```python
rate_limiter_redis = RateLimiterRedis(requests=5,period=5,storage= redis_connection)
@app.route('/api', methods=['GET'])
@RateLimiter(rate_limiter=rate_limiter_redis)
def get_request():
    return 'Hello world!'

```


**Server** 

For the implementation of HTTP server we have used `flask`. The server exposes a HTTP endpoints on `/api` based mapping.
* `GET /` 
  * welcome endpoint which greets you.
* `GET /{clientId}` 
    * decorated with @RateLimiter, it checks whether the request is allowed
    * produces a `200 OK Response` if the request is allowed
    * produces a `503 Service Unavailable Response` if the request is not-allowed


####Client module
Client module consists of a CLI application that simulates scenario in which multiple clients issue HTTP get requests in parallel to the server.
The application takes the number of clients to be simulated as a command-line argument and sets up each client within its own thread thus allowing requests to be issued in parallel.

Each client issues a requests continously with a pause of `0.5 seconds` after each request. 
Keyboard combination `CTRL + C` is to be used in order to stop the program. After the exiting signal all the clients are gracefully terminated.

