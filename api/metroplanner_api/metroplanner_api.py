import json
from jsonschema import validate, ValidationError
import schemas
import base64
import endpoints
import responses
import environment
from datetime import datetime

ENV = environment.Environment()


def private_handler(route, method, event, context, env):
    try:
        pass
    except Exception as e:
        return responses.unauthorized_401()


def public_handler(route, method, event, context, env):
    try:
        endpoint: endpoints.Endpoint = endpoints.PublicEndpoint.children[route]
        try:
            endpoint_method: endpoints.EndpointMethod = endpoint.children[method]
            try:
                action = endpoint_method(event, context, env)
                return action()
            except Exception as e:
                print('Exception calling endpoint method:', e)
                return responses.internal_server_error_500()
        except KeyError as e:
            return responses.method_not_allowed_405()
        except Exception as e:
            print('Exception getting endpoint method:', e)
            return responses.internal_server_error_500()
    except KeyError as e:
        return responses.bad_request_400()
    except Exception as e:
        print('Exception in public handler:', e)
        return responses.internal_server_error_500()


def lambda_handler(event, context):
    try:
        print("Event:", event)

        try:
            route_key = event["routeKey"]
            method, route_path = route_key.split(" ")
            path_parameters = event["pathParameters"]
            request_context = event["requestContext"]
            headers = event["headers"]
            authentication_provided = headers.get("authentication", None) is not None
            http = request_context["http"]
            source_ip = http["sourceIp"]
            user_agent = http["userAgent"]
            request_id = request_context["requestId"]
        except Exception as e:
            print(e)

        print('Method:', method)
        print('RoutePath:', route_path)

        if not ENV.is_initialized:
            print('Initializing Environment')
            ENV.initialize_environment(request_context["stage"])

        if route_path[1] == "_":
            print('Calling private handler')
            res = private_handler(route_path, method, event, context, ENV)
        else:
            print('Calling public handler')
            res = public_handler(route_path, method, event, context, ENV)
    except Exception as e:
        print("Exception handling request:", e)
        res = responses.internal_server_error_500()

    print('Result to be returned:', res)

    try:
        ENV.send_log_message(
            json.dumps(
                {"code": str(res["statusCode"])}
                | {
                    "timestamp": datetime.now().isoformat(),
                    "route_key": route_key,
                    "source_ip": source_ip,
                    "user_agent": user_agent,
                    "request_id": request_id,
                    "authentication_provided": authentication_provided,
                    "path_parameters": path_parameters,
                    "remaining_time_millis": context.get_remaining_time_in_millis(),
                },
                indent=4,
                ensure_ascii=False,
            )
        )
    except Exception as e:
        print("Error sending Log Message:")
        print(e, res)

    return res

    try:
        stage = event["requestContext"]["stage"]
        assert stage in [globals.DEV, globals.PROD]
        userdata_collection = database.get_userdata_collection(stage)
    except Exception as e:
        return {"statusCode": 400, "body": "Bad Request"}

    try:
        try:
            userid = auth.check_auth(event)
        except Exception as e:
            print(e)
            return {"statusCode": 401, "body": "Not Authorized"}

        method = event["requestContext"]["http"]["method"]

        if method == "GET":
            try:
                userdata = userdata_collection.find_one({"_id": userid})
            except Exception as e:
                print(e)
                return {"statusCode": 500, "body": "Internal Server Error"}
            try:
                if not userdata:
                    userdata = userdata or {"_id": userid, "hours": {}}
                    userdata_collection.insert_one(userdata)

                return {
                    "statusCode": 200,
                    "body": json.dumps(userdata, ensure_ascii=False, indent=4),
                }
            except Exception as e:
                print(e)
                return {"statusCode": 500, "body": "Internal Server Error"}
        elif method == "PATCH":
            try:
                data = json.loads(base64.b64decode(event.get("body", None)))
                try:
                    validate(instance=data, schema=schemas.patch_request_schema)

                    year, month, day = data["year"], data["month"], data["day"]
                    hours = data["hours"]

                    userdata_collection.update_one(
                        {
                            "_id": userid,
                        },
                        {
                            "$set": {
                                f"hours.{year}.{str(month).zfill(2)}.{str(day).zfill(2)}": hours
                            }
                        },
                        upsert=True,
                    )

                    return {"statusCode": 200, "body": "OK"}
                except ValidationError as e:
                    print(e)
                    return {"statusCode": 401, "body": ""}
                except Exception as e:
                    print(e)
                    return {"statusCode": 500, "body": ""}
            except Exception as e:
                print(e)
                return {"statusCode": 401, "body": ""}

        elif method == "DELETE":
            pass
        else:
            print("Invalid Method:", method)
            return {
                "statusCode": 501,
                "body": json.dumps(
                    {
                        "message": "Method not implemented",
                    }
                ),
            }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "message": "Internal Server Error",
                }
            ),
        }
