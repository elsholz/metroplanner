from fastapi import FastAPI, APIRouter, HTTPException, Request
from mangum import Mangum
from datetime import datetime
import json
from .environment import ENV, send_log_message
from . import responses


app = FastAPI(
    servers=[{"url": ENV.api_url, "description": "CloudFront URL"}],
    root_path="/dev",
    root_path_in_servers=False,
)

from . import v1

router = APIRouter(prefix="/api")
router.include_router(v1.router)

app.include_router(router)


@app.exception_handler(404)
async def custom_404_handler(request: Request, _):
    print(
        "Handling 404 for request to",
        request.url,
        request.path_params,
        request.query_params,
    )
    raise responses.gone_410()


def lambda_handler(event, context):
    started_at = datetime.now()
    asgi_handler = Mangum(app)

    try:
        print("Event:", event)
        print("Context:", context)

        if event.get("source", None) == "aws.scheduler":
            print("Scheduled invocation at", datetime.now().isoformat())
            return

        request_context = event["requestContext"]

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

        # if route_path.startswith("/api/_"):
        #     print("Calling private handler")
        #     res = private_handler(route_path, method, event, context, ENV)
        # else:
        #     print("Calling public handler")
        #     res = public_handler(route_path, method, event, context, ENV)

        print("Handling request to asgi_handler")
        res = asgi_handler(event, context)  # Call the instance with the event arguments
        print("Response from asgi_handler:", res)
    except Exception as e:
        print("Exception handling request:", e)
        res = responses.internal_server_error_500()

    print("Result to be returned:", res)

    try:
        send_log_message(
            json.dumps(
                {"code": str(res["statusCode"])}
                | {
                    "timestamp": datetime.now().isoformat(),
                    "execution_time": (datetime.now() - started_at).total_seconds()
                    * 1000,
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


# lambda_handler = Mangum(app, lifespan="off", api_gateway_base_path="/api")
