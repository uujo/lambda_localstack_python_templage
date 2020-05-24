"""
This is just the somple code for accessing parameter store and secrets manager
and how to swich local env to aws env
"""

import os
import json
import logging

import boto3


EDGE_PORT = 4566
LOCALSTACK_ENDPOINT = f"http://localstack:{EDGE_PORT}"

LOCAL_TABLE_NAME = "TEST_TABLE"
LOCAL_BUCKET_NAME = "test-bucket"  # bucket name cannot contain uppercase or _.
LOCAL_QUEUE_NAME = "TEST_QUEUE"
# using local dynamo server
LOCAL_DYNAMO_SERVER_ENDPOINT = "http://dynamodb:8000"


def is_local_dynamo():
    """
    check whether local dynamodb is set up
    """
    # This is set on template-samp.yaml
    return os.getenv("TEST_ENV") == "LOCAL_DYNAMO_SERVER"


def is_local_env():
    """
    check whether it is local env which doesn't have real aws set up.
    This is set up on template-sam.yaml
    :return:
    """
    # This is set on template-samp.yaml
    logging.info(f"ENVIRONMENT: {os.getenv('TEST_ENV')}")
    return os.getenv("TEST_ENV") == "LOCAL" or is_local_dynamo()


def get_params_from_ssm(path_to_config=None):
    """
    :param path_to_config: path to the config in Parameter store
    :return: dictionary of parameters
    """

    config_path = "/need_to_change_to_correct_path"
    path_to_config = path_to_config or os.getenv("CONFIG_SSM_PARAMETER", config_path)

    ssm = boto3.Session(region_name='us-east-1').client('ssm')

    param = ssm.get_parameter(Name=path_to_config, WithDecryption=True)
    param_dict = {}
    if param and "Parameter" in param:
        param_dict = json.loads(param['Parameter']['Value'])

    return param_dict


def get_params_from_secretsmanager(path_to_config=None):
    """

    :param path_to_config: secrete location
    :return:
    """
    client = boto3.Session().client(service_name="secretsmanager", region_name="us-east-1")
    response = client.get_secret_value(SecretId=path_to_config)
    param_dict = json.loads(response.get('SecretString', "{}"))

    return param_dict


def dynamo_endpoint():
    """
    returns dynamodb endpoint
    """
    # check local dynamo first
    if is_local_dynamo():
        return LOCAL_DYNAMO_SERVER_ENDPOINT
    if is_local_env():
        return LOCALSTACK_ENDPOINT
    return None


def s3_endpoint():
    """
    returns s3 endpoint
    """
    return LOCALSTACK_ENDPOINT if is_local_env() else None


def sqs_endpoint():
    """
    returns sqs endpoint
    """
    return LOCALSTACK_ENDPOINT if is_local_env() else None


def dynamo_table_name():
    """
    returns table name from parameter store
    """
    if is_local_env():
        return LOCAL_TABLE_NAME

    # get data from parameter store with correct key
    # table_name = get_params_from_ssm()["CORRECT_KEY"]
    return "table_name"


def s3_bucket_name():
    """
    returns s3 bucket name from parameter store
    """
    if is_local_env():
        return LOCAL_BUCKET_NAME

    # get data from parameter store with correct key
    # bucket_name = get_params_from_ssm()["CORRECT_KEY"]
    return "bucket_name"


def sqs_name():
    """
    returns sqs name from parameter store
    """
    if is_local_env():
        return LOCAL_QUEUE_NAME

    # get data from parameter store with correct key
    # sqs_name = get_params_from_ssm()["CORRECT_KEY"]
    return "sqs_name"
