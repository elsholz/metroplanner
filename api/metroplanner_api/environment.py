"""
Loads data that is dependent on the environment like
the authorization and database connection secrets.
Connects to the database, creates a bearer token verifier
and exposes 
"""

from pymongo import MongoClient
import json
import boto3
from botocore.exceptions import ClientError
from urllib.request import urlopen
from typing import Optional
from dataclasses import dataclass
from jose import jwt


class BadRequestError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


DEV = "dev"
PROD = "prod"
REGION = "eu-central-1"


@dataclass
class Environment:
    is_initialized: bool = False
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_ADDRESS: Optional[str] = None
    DB_NAME: Optional[str] = None
    AUTH0_DOMAIN: Optional[str] = None
    API_AUDIENCE: Optional[str] = None
    ALGORITHMS: Optional[str] = None
    SQS_URL: Optional[str] = None

    database: Optional[object] = None
    sqs_client: Optional[object] = None


ENV = Environment()


def initialize_environment(env: str) -> None:
    print("Getting Secrets from Secrets Manager")
    ENV.is_initialized = True
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=REGION,
    )

    secret_value = json.loads(
        client.get_secret_value(SecretId="MetroplannerKeys")["SecretString"]
    )

    ENV.DB_USER = secret_value[f"DB_USER_{env.upper()}"]
    ENV.DB_PASSWORD = secret_value[f"DB_PASSWORD_{env.upper()}"]
    ENV.DB_ADDRESS = secret_value[f"DB_INSTANCE_URL_{env.upper()}"]
    ENV.DB_NAME = secret_value[f"DB_NAME_{env.upper()}"]

    print("Secrets received, DB Name:", ENV.DB_NAME)

    ENV.AUTH0_DOMAIN = secret_value[f"AUTH0_DOMAIN_{env.upper()}"]
    ENV.API_AUDIENCE = secret_value[f"AUTH0_AUDIENCE_{env.upper()}"]
    ENV.ALGORITHMS = ["RS256"]

    print("Connecting to MongoDB")

    client = MongoClient(
        f"mongodb+srv://{ENV.DB_USER}:{ENV.DB_PASSWORD}@"
        f"{ENV.DB_ADDRESS}/{ENV.DB_NAME}?retryWrites=true&w=majority"
    )

    db = client[ENV.DB_NAME]

    ENV.database = db

    # jwks_url = f"https://{self.AUTH0_DOMAIN}/.well-known/jwks.json"
    # issuer = f"https://{self.AUTH0_DOMAIN}/"

    # sv = AsymmetricSignatureVerifier(jwks_url)  # Reusable instance
    # self.verifier = TokenVerifier(
    #     signature_verifier=sv, issuer=issuer, audience=self.API_AUDIENCE
    # )

    print("Connecting to SQS")
    ENV.sqs_client = boto3.client("sqs")
    ENV.SQS_URL = {
        "dev": "https://sqs.eu-central-1.amazonaws.com/891666753558/MetroplannerQueueDev",
        "prod": "https://sqs.eu-central-1.amazonaws.com/891666753558/MetroplannerQueueProd",
    }[env]
    print("Finished Connecting to services")


def get_database():
    return ENV.database


def check_auth(event):
    headers = event.get("headers", {})
    auth_header = headers.get("Authorization", headers.get("authorization", None))

    if not auth_header or not isinstance(auth_header, str):
        raise BadRequestError("Missing auth header or in invalid format")

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
                raise e
            except jwt.JWTClaimsError as e:
                print("Error, JWT Claims Error")
                raise e
            except Exception as e:
                print("Error:", e)
                raise e

            if ENV.API_AUDIENCE in payload.get("aud", []):
                sub = payload["sub"]
                return sub.removeprefix("auth0|")
        raise Exception()
    except Exception as e:
        print("Error in check_auth:", e)
        raise e


def send_log_message(msg):
    response = ENV.sqs_client.send_message(
        QueueUrl=ENV.SQS_URL,
        MessageBody=msg,
    )
