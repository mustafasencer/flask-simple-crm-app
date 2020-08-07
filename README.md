# Blu TV Challenge

BluTV challenge, Flask app with Mongodb and Redis. 

I made my development on a Linux system so I hope there won't be edge cases that are not covered.

# Installation

## Run with virtual environment
```bash
export SECRET_KEY="blutv"
export MONGO_HOST="localhost"
export REDIS_HOST="localhost"
export MONGO_PORT=27017
export REDIS_PORT=6379
```
After activating the virtual environment.

```bash
pip install -r requirements.txt
```
Run the application
```bash
python application.py
```

## Run with Dockerfile
 
This run selection uses the host's local MongoDB and Redis on default ports.


After going to the project's root directory. Build the Dockerfile with the following command.

```bash
docker build -t blutv_challenge:latest .
```

Run the Docker image with the following command. I utilized a slight trick in order to reach MongoDB and Redis active on host environment by adding --net="host" although it is not best practice.

If this method is utilized MongoDB and Redis should be available on host machine as per the environment variables.
```bash
docker run -d -p 5000:5000 --net="host" blutv_challenge
```

## Run with docker-compose (Not sure to fit all environments)


This is the last alternative to consider, where every application (Flask, MongoDB and Redis) are containerized and gathered in a YAML file.

It could not work as expected if the ports are already in use or other system differences. Some conflicts may be expected.

```bash
docker-compose build
```
```bash
docker-compose up
```
# API Documentation
I tried to follow the requirements. I hope I did not misinterpret some parts of the document.

a) **Register contact**

```http request
POST /contacts
```
- Request Body
```json
{
	"first_name": "string",
	"last_name": "string",
	"email": "string",
	"username": "string",
	"password": "string"
}
```
b) **Get contact info**
```http request
GET /contacts/<cid>
```
c) **Delete contact** 

   - JWT required
```http request
DELETE /contacts/<cid>
```
d) **List contacts**
```http request
GET /contacts
```
e) **Reset contact password**

   - JWT required
```http request
POST /contacts/<cid>/reset-password
```
- Request body
```json
{
	"new_password": "string",
	"new_password_repeat": "string"
}
```
f) **Login**
```http request
POST /login
```
- Request body
```json
{
	"email": "string",
	"password": "string"
}
```
### Default Response Schema
- **Success Response**
```json
{
    "code": "integer",
    "success": {
        "isSuccess": "boolean",
        "message": "string"
    }
}
```

- **Error Response**
```json
{
    "code": "integer",
    "error": {
        "extra": "string",
        "message": "string"
    }
}
```
# Unit Test
Pytest library has been utilized for the unit tests.

```bash
pytest -v 
```
The command above executes the following test script:
- Register contact
- Get all the contacts
- Get the registered contact
- Login with the registered contact
- Reset password of registered contact
- Delete registered contact
