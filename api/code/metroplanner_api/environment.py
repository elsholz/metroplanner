"""
Loads data that is dependent on the environment like
the authorization and database connection secrets.
Connects to the database, creates a bearer token verifier
and exposes 
"""

from pymongo import MongoClient
import json
import boto3
from urllib.request import urlopen
from jose import jwt
from fastapi import Request, HTTPException
from os import environ
import requests


class BadRequestError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


DEV = "dev"
PROD = "prod"
REGION = "eu-central-1"


class Environment:
    is_initialized: bool = False

    def __init__(self) -> None:
        env = (
            environ["AWS_LAMBDA_FUNCTION_NAME"].removeprefix("MetroplannerFunc").lower()
        )

        print("Getting Secrets from Secrets Manager")
        self.is_initialized = True
        session = boto3.session.Session()
        client = session.client(
            service_name="secretsmanager",
            region_name=REGION,
        )

        self.api_url = {
            "dev": "https://dev.ich-hab-plan.de",
            "prod": "https://ich-hab-plan.de",
        }[env]

        secret_value = json.loads(
            client.get_secret_value(SecretId="MetroplannerKeys")["SecretString"]
        )

        self.DB_USER = secret_value[f"DB_USER_{env.upper()}"]
        self.DB_PASSWORD = secret_value[f"DB_PASSWORD_{env.upper()}"]
        self.DB_ADDRESS = secret_value[f"DB_INSTANCE_URL_{env.upper()}"]
        self.DB_NAME = secret_value[f"DB_NAME_{env.upper()}"]

        print("Secrets received, DB Name:", self.DB_NAME)

        self.AUTH0_DOMAIN = secret_value[f"AUTH0_DOMAIN_{env.upper()}"]
        self.AUTH0_M2M_CLIENT_SECRET = secret_value[
            f"AUTH0_M2M_CLIENT_SECRET_{env.upper()}"
        ]
        self.AUTH0_M2M_CLIENT_ID = secret_value[f"AUTH0_M2M_CLIENT_ID_{env.upper()}"]
        self.API_AUDIENCE = secret_value[f"AUTH0_AUDIENCE_{env.upper()}"]
        self.ALGORITHMS = ["RS256"]

        # payload = f"grant_type=client_credentials&client_id=%7B{self.AUTH0_M2M_CLIENT_ID}%7D&client_secret=%7B{self.AUTH0_M2M_CLIENT_SECRET}%7D&audience=https%3A%2F%2F{self.AUTH0_DOMAIN}%2Fapi%2Fv2%2F"
        payload = {
            'grant_type': 'client_credentials',
            "client_id": self.AUTH0_M2M_CLIENT_ID,
            'client_secret': self.AUTH0_M2M_CLIENT_SECRET,
            'audience': "https://metroplanner-dev.eu.auth0.com/api/v2/",
        }
        # headers = {"content-type": "application/x-www-form-urlencoded"}

#           --header 'content-type: application/x-www-form-urlencoded' \
#   --data grant_type=client_credentials \
#   --data 'client_id={yourClientId}' \
#   --data 'client_secret={yourClientSecret}' \
#   --data 'audience=https://{yourDomain}/api/v2/'

        response = requests.post(
            f"https://{self.AUTH0_DOMAIN}/oauth/token",
            # headers=headers,
            data=payload,
        )

        print("Response:", response)
        print("status:", response.status_code)

        data = response.content
        print("Data:", data)

        self.MGMT_API_ACCESS_TOKEN = json.loads(data.decode("utf-8"))["access_token"]

        print("Connecting to MongoDB")

        client = MongoClient(
            f"mongodb+srv://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_ADDRESS}/{self.DB_NAME}?retryWrites=true&w=majority"
        )

        db = client[self.DB_NAME]

        self.database = db

        print("Connecting to SQS")
        self.sqs_client = boto3.client("sqs")
        self.SQS_URL = {
            "dev": "https://sqs.eu-central-1.amazonaws.com/891666753558/MetroplannerQueueDev",
            "prod": "https://sqs.eu-central-1.amazonaws.com/891666753558/MetroplannerQueueProd",
        }[env]
        print("Finished Connecting to services")


ENV = Environment()


# TODO: Move to class Environment
def check_auth(request: Request):
    auth_header = request.headers.get(
        "Authorization", request.headers.get("authorization", None)
    )

    if not auth_header or not isinstance(auth_header, str):
        raise HTTPException(
            status_code=400, detail="Missing authorization header or in invalid format"
        )

    try:
        token = auth_header.split(" ")[-1]

        jsonurl = urlopen("https://" + ENV.AUTH0_DOMAIN + "/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)

        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ENV.ALGORITHMS,
                    audience=ENV.API_AUDIENCE,
                    issuer="https://" + ENV.AUTH0_DOMAIN + "/",
                )
            except jwt.ExpiredSignatureError as e:
                print("Error: Expired Signature:", e)
                raise HTTPException(status_code=401, detail="Expired Signature")
            except jwt.JWTClaimsError as e:
                print("Error, JWT Claims Error")
                raise HTTPException(status_code=401, detail="Claims Error")
            except Exception as e:
                print("Error:", e)
                raise HTTPException(status_code=401, detail="Authentication Failure")

            if ENV.API_AUDIENCE in payload.get("aud", []):
                sub = payload["sub"]
                return sub
        raise Exception()
    except Exception as e:
        print("Error in check_auth:", e)
        raise e


def send_log_message(msg):
    response = ENV.sqs_client.send_message(
        QueueUrl=ENV.SQS_URL,
        MessageBody=msg,
    )
