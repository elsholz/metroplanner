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
from auth0.authentication.token_verifier import (
    TokenVerifier,
    AsymmetricSignatureVerifier,
)


class BadRequestError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


DEV = "dev"
PROD = "prod"
REGION = "eu-central-1"


class Environment:
    def __init__(self, env: str) -> None:
        session = boto3.session.Session()
        client = session.client(
            service_name="secretsmanager",
            region_name=globals.REGION,
        )

        secret_value = json.loads(
            client.get_secret_value(SecretId="MetroplannerKeys")["SecretString"]
        )

        self.__DB_USER = secret_value[f"DB_USER_{env.upper()}"]
        self.__DB_PASSWORD = secret_value[f"DB_PASSWORD_{env.upper()}"]
        self.__DB_ADDRESS = secret_value[f"DB_INSTANCE_URL_{env.upper()}"]
        self.__DB_NAME = secret_value[f"DB_NAME_{env.upper()}"]

        self.__AUTH0_DOMAIN = secret_value[f"AUTH0_DOMAIN_{env.upper()}"]
        self.__API_AUDIENCE = secret_value[f"AUTH0_AUDIENCE_{env.upper()}"]

        client = MongoClient(
            f"mongodb+srv://{self.__DB_USER}:{self.__DB_PASSWORD}@"
            f"{self.__DB_ADDRESS}/{self.__DB_NAME}?retryWrites=true&w=majority"
        )

        db = client[self.__DB_NAME]

        self.__database = db

        jwks_url = f"https://{self.__AUTH0_DOMAIN}/.well-known/jwks.json"
        issuer = f"https://{self.__AUTH0_DOMAIN}/"

        sv = AsymmetricSignatureVerifier(jwks_url)  # Reusable instance
        self.__verifier = TokenVerifier(
            signature_verifier=sv, issuer=issuer, audience=self.__API_AUDIENCE
        )

        self.sqs_client = boto3.client("sqs")
        self.__SQS_URL = {
            "dev": "https://sqs.eu-central-1.amazonaws.com/891666753558/MetroplannerQueueDev",
            "prod": "https://sqs.eu-central-1.amazonaws.com/891666753558/MetroplannerQueueProd",
        }[env]

    def get_database(self):
        return self.__database

    def check_auth(self, event):
        headers = event.get("headers", {})
        auth_header = headers.get("Authorization", headers.get("authorization", None))

        if not auth_header or not isinstance(auth_header, str):
            raise BadRequestError("Missing auth header or in invalid format")

        try:
            token = auth_header.split(" ")[-1]
            try:
                verified = self.__verifier.verify(token)
            except Exception as e:
                raise InvalidTokenError("Error validating token")

            try:
                assert verified["aud"] == self.__API_AUDIENCE
                assert "sub" in verified
                assert isinstance(verified["sub"], str)
                assert all([x in "|@" or x.isalnum() for x in verified["sub"]])
            except AssertionError as e:
                raise InvalidTokenError("Token missing sub or aud is incorrect")

            userid = verified["sub"]

            return userid

        except Exception as e:
            print("Error in check_auth:", e)
            raise e

    def send_log_message(self, msg):
        response = self.sqs_client.send_message(
            QueueUrl=self.__SQS_URL,
            MessageBody=msg,
        )


environments = {}


def get_environment(env=DEV):
    if env in [DEV, PROD] and env not in environments:
        environments[env] = Environment(env)
    elif env not in environments:
        raise Exception(f"Unknown Environment {env}")
    return environments[env]
