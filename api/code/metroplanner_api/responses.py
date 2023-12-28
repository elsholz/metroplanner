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
    raise HTTPException(status_code=401, detail="Unauthorized")


def forbidden_403():
    raise HTTPException(status_code=403, detail="Forbidden")


# using 410 over 404 as a workaround, since AWS CloudFront will return index.html on 404 errors
def gone_410():
    raise HTTPException(status_code=410, detail="Gone")


def method_not_allowed_405():
    raise HTTPException(status_code=405, detail="Method Not Allowed")


def not_acceptable_406():
    raise HTTPException(status_code=406, detail="Not Acceptable")


### 5xx
def internal_server_error_500():
    raise HTTPException(status_code=500, detail="Internal Server Error")


def not_implemented_501():
    raise HTTPException(status_code=501, detail="Not Implemented")
