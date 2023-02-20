import json
import boto3
from string import Template
from datetime import datetime


def lambda_handler(event, context):
    sns_client = boto3.client("sns")
    sqs_client = boto3.client("sqs")
    now = datetime.now()

    env = (
        "prod"
        if context.function_name == "MetroplannerLogFuncProd"
        else "dev"
        if context.function_name == "MetroplannerLogFuncDev"
        else print(context.function_name)
    )

    print("Environment: ", env)

    report = Template(open("report.template").read()).substitute(
        {
            "app": "Metroplanner",
            "env": env.upper(),
            "total": None,
            "successful": None,
            "clienterror": None,
            "servererror": None,
            "detailed": json.dumps({}, indent=4, ensure_ascii=False)
        }
    )

    print(report)

    response = sns_client.publish(
        TopicArn='arn:aws:sns:eu-central-1:891666753558:PROD_Metroplanner' if env == 'prod' else "arn:aws:sns:eu-central-1:891666753558:DEV_Metroplanner",
        Message=report,
        Subject=f"Metroplanner {env.upper()} - Statistics Report {now.isoformat()}",
    )

    print(response)
