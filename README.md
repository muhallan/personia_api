# PERSONIA API
This is an API created to help Personia, the HR manager who works at 
Ever-changing Hierarchy GmbH. It is part of the interviews for the backend 
engineer role at Personio.

The API helps Personia easily understand her ever changing company's 
hierarchy, and also to respond to employee's queries about who their boss is.

This has been developed using the Python language with the aid of Flask 
micro web framework. It uses SQLite for the database.

## Getting started
These instructions will get you a copy of the project up and running on your 
local machine for development and testing purposes. A linux machine is assumed.

### Pre-requisites
* [Python](https://docs.python.org/3/) versions 3.6 to 3.8
* [Git](https://git-scm.com/)
* [pipenv](https://github.com/pypa/pipenv)

### Installation
* Navigate to the root of the project

```shell
$ cd personio_api
```
* Create the virtual environment to run from, and install the requirements
```shell
pipenv install
pipenv shell
```
* Create a file called `.env` in the root of the project, and paste there, the 
contents of `.env.sample`. Adjust the configurations according to your local 
settings.

* Export the environment variables in the .env
```shell
$ source .env
```

## Running the API
* To run the API
```shell
$ python manage.py runserver
```
The API should now be available at http://127.0.0.1:5000. You can interact 
with it using [Postman](https://www.postman.com/downloads/).
See below for the documentation of the endpoints

* To run the tests without coverage
```shell
$ python manage.py test
```

* To run the tests with coverage
```shell
$ python manage.py cov
```

## API Documentation

All API responses come in standard JSON. All requests must include a 
content-type of `application/json` and the body must be valid JSON.

**Register**
----
This signs up a user to enable them make authenticated requests 

* **URL:**

    > /api/v1/auth/register


* **Method:**

  `POST`

* **Data Params:**

    Sample POST data:
    ```json
    {
        "username": "uname",
        "password": "pswd",
        "name": "John Doe"
    }
    
    ```

* **Success Response:**
  
  * **Code:** 201 CREATED<br />
  * **Content:** 
    ```json
    {
      "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTI3ODE5NTcsImlhdCI6MTU5Mjc2NzU1Nywic3ViIjoiMzE1ZjlmNmU5NWM5NGZiNzk4NzA1OTViZTUzOTM1MjUifQ.Pl0WZYyO1waBh-7QrAO6-6JwgtRFhuZ3Q75zrjkZIbg",
      "message": "Successfully registered.",
      "status": "success"
    }
    ```
 
* **Sample Error Response:**

  * **Code:** 400 BAD REQUEST <br />
  * **Content:** 
    ```json
    {
      "message": "Incomplete data. Ensure valid data for username, name and password are provided",
      "status": "fail"
    }
    ```

* **Sample Request:**
    ```json
    $ curl -d '{"username": "uname", "password": "pswd", "name": "John Doe"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/auth/register
    ```

* **Notes:**

    After getting a successful response, copy the auth token provided, for 
    use in subsequent requests that require authentication. This token must 
    be prepended with the `"Bearer "` string before being sent in the 
    `Authorization` header.

**Login**
----
This signs in an already registered user to enable them make authenticated 
requests 

* **URL:**

    > /api/v1/auth/login


* **Method:**

  `POST`

* **Data Params:**

    Sample POST data:
    ```json
    {
        "username": "uname",
        "password": "pswd"
    }
    
    ```

* **Success Response:**
  
  * **Code:** 200 OK<br />
  * **Content:** 
    ```json
    {
      "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTI3ODI5NjcsImlhdCI6MTU5Mjc2ODU2Nywic3ViIjoiMzE1ZjlmNmU5NWM5NGZiNzk4NzA1OTViZTUzOTM1MjUifQ.lz2eBeLn2jw7GjOeybyalEc1MtTdK3-JUQyejwFQnNM",
      "message": "Successfully logged in.",
      "status": "success"
    }
    ```
 
* **Sample Error Response:**

  * **Code:** 401 UNAUTHORISED <br />
  * **Content:** 
    ```json
    {
      "message": "Invalid username or password.",
      "status": "fail"
    }
    ```

* **Sample Request:**
    ```json
    $ curl -d '{"username": "uname", "password": "pswd"}'  -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1/auth/login
    ```

* **Notes:**

    After getting a successful response, copy the auth token provided, for 
    use in subsequent requests that require authentication. This token must 
    be prepended with the `"Bearer "` string before being sent in the 
    `Authorization` header.

**Structure Hierarchy**
----
This endpoint is used to properly structure JSON data into an ordered 
employee hierarchy with the most senior employee at the top of the nested 
dictionary.

* **URL:**

    > /api/v1/hierarchy/structure


* **Method:**

  `POST`

* **Data Params:**

    Sample POST data:
    ```json
    {
        "Pete": "Nick",
        "Barbara": "Nick",
        "Nick": "Sophie",
        "Sophie": "Jonas"
    }
    
    ```

* **Success Response:**
  
  * **Code:** 201 CREATED<br />
  * **Content:** 
    ```json
    {
      "employee_hierarchy": {
        "Jonas": {
          "Sophie": {
            "Nick": {
              "Barbara": {},
              "Pete": {}
            }
          }
        }
      },
      "status": "success"
    }
    ```
 
* **Sample Error Response:**

  * **Code:** 400 BAD REQUEST <br />
  * **Content:** 
    ```json
    {
      "message": "The posted JSON contains loops. These employees have more than one supervisor: ['Barbara']",
      "status": "fail"
    }
    ```

* **Sample Request:**
    ```json
    $ curl -d '{"Pete": "Nick", "Barbara": "Nick", "Nick": "Sophie", "Sophie": "Jonas"}'  -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTI3ODMxMDQsImlhdCI6MTU5Mjc2ODcwNCwic3ViIjoiMzE1ZjlmNmU5NWM5NGZiNzk4NzA1OTViZTUzOTM1MjUifQ.14FhyRZVZV2VZlD8vVwBOjAdX30RyV9ipjN8CSxurSA"  -X POST http://127.0.0.1:5000/api/v1/hierarchy/structure
    ```

* **Notes:**

    This endpoint needs authentication. Ensure you include the 
    `Authorization` header in the request. The token sent should be valid 
    and should start with the `"Bearer "` string. 

**Get two immediate supervisors**
----
This endpoint returns the the supervisor and the supervisor's supervisor of a
 the employee passed in the query parameter. If any of them doesn't exist, it
  will return null.
* **URL**

  > /api/v1/hierarchy/two_supervisors/<employee_name>

* **Method:**

  `GET`

* **Success Response:**

  * **Code:** 200 OK<br />
    **Content:** 
    ```json
    {
      "message": "Both supervisors are available",
      "status": "success",
      "supervisors": {
        "supervisor": "Sophie",
        "supervisor_of_supervisor": "Jonas"
      }
    }
    ```
 
* **Sample Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** 
    ```json
    {
      "message": "The requested employee: 'Nic' doesn't exist",
      "status": "fail"
    }
    ```


* **Sample Request:**
    ```json
    $ curl -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTI3ODMxMDQsImlhdCI6MTU5Mjc2ODcwNCwic3ViIjoiMzE1ZjlmNmU5NWM5NGZiNzk4NzA1OTViZTUzOTM1MjUifQ.14FhyRZVZV2VZlD8vVwBOjAdX30RyV9ipjN8CSxurSA" -X GET http://127.0.0.1:5000/api/v1/hierarchy/two_supervisors/Nick
    ```
* **Notes:**

    This endpoint needs authentication. Ensure you include the 
    `Authorization` header in the request. The token sent should be valid 
    and should start with the `"Bearer "` string.  
    
    The employee name sent in the URL is case-sensitive. E.g. 
    `Nick` doesn't match `NicK`.
    
## Assumptions
* The employee names sent in the hierarchy JSON are unique
* Every time a new JSON is posted, it is a fresh complete hierarchy meaning we 
can discard the old hierarchy and replace it with the new one.
* The employee names are case-sensitive


## Author
Allan Muhwezi
