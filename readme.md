# ZEMANTA BACKEND ENGINEER CHALLENGE
##### author: Gojko Hajdukovic, 05.2021

Table of contents:
1. [Introduction](#introduction)
2. [Setup](#setup)

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




