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

    messages = []

    while True:
        try:
            res = sqs_client.receive_message(
                QueueUrl={
                    "dev": "https://sqs.eu-central-1.amazonaws.com/891666753558/MetroplannerQueueDev",
                    "prod": "https://sqs.eu-central-1.amazonaws.com/891666753558/MetroplannerQueueProd",
                }[env]
            )
            msg = res['Messages']
            print(msg)
            if not msg: break
            for m in msg:
                messages.append(m['Body'])
        except Exception as e:
            break

    response_codes = {}
    for m in messages:
        data = json.loads(m)
        x = response_codes[data['code']] = response_codes.get(data['code'], [])
        x.append(data)

    print(response_codes)

    def get_codes_starting_with(x):
        res = []
        for code in response_codes:
            if code.startswith(x):
                res.extend(response_codes[code])
        return res

    report = Template(open("report.template").read()).substitute(
        {
            "app": "Metroplanner",
            "env": env.upper(),
            "total": len(list(x for l in response_codes.values() for x in l)),
            "successful": get_codes_starting_with('2'),
            "clienterror": get_codes_starting_with('4'),
            "servererror": get_codes_starting_with('5'),
            "detailed": json.dumps(response_codes, indent=4, ensure_ascii=False),
        }
    )

    print(report)

    response = sns_client.publish(
        TopicArn="arn:aws:sns:eu-central-1:891666753558:PROD_Metroplanner"
        if env == "prod"
        else "arn:aws:sns:eu-central-1:891666753558:DEV_Metroplanner",
        Message=report,
        Subject=f"Metroplanner {env.upper()} - Statistics Report {now.isoformat()}",
    )

    print(response)
