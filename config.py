import json
import logging
import os

import boto3
from botocore.exceptions import ClientError


def get_secret(secret_name: str):
    logging.info("Getting secret {}".format(secret_name))
    region_name = "eu-west-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    if os.getenv("ENV_MODE") == "TRUE":
        logging.debug("Using AWS credentials from env")
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name,
            aws_access_key_id=os.getenv("aws_access_key_id"),
            aws_secret_access_key=os.getenv("aws_secret_access_key")
        )
    else:
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

    try:
        response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e
    else:
        return response["SecretString"]


def get_backend() -> str:
    logging.info("Getting celery backend")
    if os.getenv("CELERY_DB", "FALSE").upper() in ("TRUE", "T", "1"):
        logging.debug("Using postgres backend")
        data = json.loads(get_secret("prod/celery/postgres"))
        return f"db+postgresql://{data['username']}:{data['password']}@{data['host']}/{data['db_name']}"
    else:
        logging.debug("Using redis backend")
        return os.getenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379")
