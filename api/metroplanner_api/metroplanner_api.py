import json
import endpoints
import responses
import environment
from datetime import datetime

ENV = environment.Environment()


def private_handler(route, method, event, context, env: environment.Environment):
    try:
        sub = env.check_auth(event)
        try:
            endpoint: endpoints.EndpointCollection = endpoints.PrivateEndpoint.children[
                route
            ]
            try:
                endpoint_method: endpoints.EndpointMethod = endpoint.children[method]
                try:
                    action = endpoint_method(event, context, env, sub)
                    return action()
                except Exception as e:
                    print("Exception calling endpoint method:", e)
                    return responses.internal_server_error_500()
            except KeyError as e:
                return responses.method_not_allowed_405()
            except Exception as e:
                print("Exception getting endpoint method:", e)
                return responses.internal_server_error_500()
        except KeyError as e:
            print("Exception in private handler:", e)
            return responses.bad_request_400()
        except Exception as e:
            print("Exception in private handler:", e)
            return responses.internal_server_error_500()
    except environment.BadRequestError as e:
        print("Exception in private handler:", e)
        return responses.bad_request_400()
    except environment.InvalidTokenError as e:
        print("Exception in private handler:", e)
        return responses.unauthorized_401()
    except Exception as e:
        print("Exception in private handler:", e)
        return responses.internal_server_error_500()


def public_handler(route, method, event, context, env: environment.Environment):
    try:
        endpoint: endpoints.EndpointCollection = endpoints.PublicEndpoint.children[
            route
        ]
        try:
            endpoint_method: endpoints.EndpointMethod = endpoint.children[method]
            try:
                action = endpoint_method(event, context, env)
                return action()
            except Exception as e:
                print("Exception calling endpoint method:", e)
                return responses.internal_server_error_500()
        except KeyError as e:
            return responses.method_not_allowed_405()
        except Exception as e:
            print("Exception getting endpoint method:", e)
            return responses.internal_server_error_500()
    except KeyError as e:
        return responses.bad_request_400()
    except Exception as e:
        print("Exception in public handler:", e)
        return responses.internal_server_error_500()


def lambda_handler(event, context):
    try:
        print("Event:", event)
        print("Context:", context)

        request_context = event["requestContext"]

        if not ENV.is_initialized:
            print("Initializing Environment")
            ENV.initialize_environment(request_context["stage"])

        route_key = event["routeKey"]
        method, route_path = route_key.split(" ")
        path_parameters = event.get("pathParameters", None)
        headers = event["headers"]
        authentication_provided = headers.get("Authorization", None) is not None
        http = request_context["http"]
        source_ip = http["sourceIp"]
        user_agent = http.get("userAgent", None)
        request_id = request_context["requestId"]

        print("Method:", method)
        print("RoutePath:", route_path)

        if route_path.startswith("/api/_"):
            print("Calling private handler")
            res = private_handler(route_path, method, event, context, ENV)
        else:
            print("Calling public handler")
            res = public_handler(route_path, method, event, context, ENV)
    except Exception as e:
        print("Exception handling request:", e)
        res = responses.internal_server_error_500()

    print("Result to be returned:", res)

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
