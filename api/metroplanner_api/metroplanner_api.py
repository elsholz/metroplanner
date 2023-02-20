import json
from jsonschema import validate, ValidationError
import schemas
import base64
import endpoints
import responses
import environment
from datetime import datetime

ENV = environment.Environment(env="dev")


def private_handler(event, context):
    try:
        pass
    except Exception as e:
        return responses.unauthorized_401()


def public_handler(event, context):
    api_path = "plans"
    method = "get"

    try:
        endpoint_collection: endpoints.Endpoint = (
            endpoints.PublicEndpoint.method_mapping[api_path]
        )
        try:
            endpoint = endpoint_collection.method_mapping[method]
            try:
                endpoint(event, context)
            except Exception as e:
                return responses.internal_server_error_500()
        except KeyError as e:
            return responses.method_not_allowed_405()
        except Exception as e:
            return responses.internal_server_error_500()
    except KeyError as e:
        return responses.bad_request_400()
    except Exception as e:
        return responses.internal_server_error_500()


def lambda_handler(event, context):
    try:
        if False:
            res = private_handler(event, context)
        else:
            res = public_handler(event, context)
    except Exception as e:
        res = responses.internal_server_error_500()

    try:
        ENV.send_log_message(
            json.dumps(
                res
                | {
                    "timestamp": datetime.now().isoformat(),
                    # "event": event,
                    # "context": context
                },
                indent=4,
                ensure_ascii=False,
            )
        )
        print("Event:", event)
        print("Context:", context)
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
