from json import dumps
from fastapi import HTTPException


### 2xx
def ok_200(body="OK"):
    if isinstance(body, str):
        return {"statusCode": 200, "body": "OK"}
    else:
        return {"statusCode": 200, "body": dumps(body, indent=4)}


def created_201(body={}):
    return {"statusCode": 201, "body": dumps(body, indent=4)}


def no_content_204():
    return {"statusCode": 204, "body": "No Content"}


### 4xx
def bad_request_400():
    raise HTTPException(status_code=400, detail="Bad Request")


def unauthorized_401():
    raise HTTPException(statusCode=401, body="Unauthorized")


def forbidden_403():
    raise HTTPException(statusCode=403, body="Forbidden")


# using 410 over 404 as a workaround, since AWS CloudFront will return index.html on 404 errors
def gone_410():
    raise HTTPException(statusCode=410, body="Gone")


def method_not_allowed_405():
    raise HTTPException(statusCode=405, body="Method Not Allowed")


def not_acceptable_406():
    raise HTTPException(statusCode=406, body="Not Acceptable")


### 5xx
def internal_server_error_500():
    raise HTTPException(statusCode=500, body="Internal Server Error")


def not_implemented_501():
    raise HTTPException(statusCode=501, body="Not Implemented")