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
```
3. After all the project related dependencies have been successfully installed, we can start the `Flask` server by issuing:
```shell script
venv/bin/python src/server/app.py
```
4. With server successfully started, issue following commands and fill in the .env file with the valid url and port exposed by the server.
```shell script
cp .env.example .env
```
5. In order to run client cli application with help description issue:
```shell script
venv/bin/python src/client/cli.py --help
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
1. First, we need to run a `rate-limiter-server`. In order to run a docker container issue:
```shell script
docker run --network <network-name> -p 5001:5001 --name <container-name> ghajduk3/rate-limiter-server
```
After the server has successfully started copy the `.env.example` to `.env` and change the base_url part of `WEBSITE_URL` to the afore created `<container_name>`, i.e `WEBSITE_URL=http://<container-name>:5001/api`.

2. In order to run a `rate-limiter-client` CLI application with help description issue:
```shell script
docker run --network <network-name> --name <container-name> ghajduk3/rate-limiter-client --help
```
<a name="description"></a>
### Description


