from json import dumps

def ok_200(body="OK"):
    if isinstance(body, str):
        return {"statusCode": 200, "body": "OK"}
    else:
        return {"statusCode": 200, "body": dumps(body, indent=4)}
def created_201():
    return {"statusCode": 201, "body": "Created"}
def no_content_204():
    return {"statusCode": 204, "body": "No Content"}

def bad_request_400():
    return {"statusCode": 400, "body": "Bad Request"}
def unauthorized_401():
    return {"statusCode": 401, "body": "Unauthorized"}
def forbidden_403():
    return {"statusCode": 403, "body": "Forbidden"}
def not_found_404():
    return {"statusCode": 404, "body": "Not Found"}
def method_not_allowed_405():
    return {"statusCode": 405, "body": "Method Not Allowed"}
def not_acceptable_406():
    return {"statusCode": 406, "body": "Not Acceptable"}


def internal_server_error_500():
    return {"statusCode": 500, "body": "Internal Server Error"}
def not_implemented_501():
    return {"statusCode": 501, "body": "Not Implemented"}
