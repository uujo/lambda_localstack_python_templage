"""
This is just the somple code for accessing parameter store and secrets manager
and how to swich local env to aws env 
"""

import os
import json
import boto3

LOCAL_TABLE_NAME = "TEST_TABLE"
LOCAL_DYNAMO_ENDPOINT = "http://localstack:4569"
LOCAL_BUCKET_NAME = "TEST_BUCKET"
LOCAL_S3_ENDPOINT = "http://localstack:4572"
LOCAL_QUEUE_NAME = "TEST_QUEUE"
LOCAL_SQS_ENDPOINT = "http://localstack:4576"


def is_local_env():
    """
    check whether it is local env which doesn't have real aws set up.
    This is set up on template-sam.yaml
    :return:
    """
    # This is set on template-samp.yaml
    return os.getenv("TEST_ENV") == "LOCAL"


def get_params_from_ssm(path_to_config=None):
    """
    :param path_to_config: path to the config in Parameter store
    :return: dictionary of parameters
    """

    config_path = "/need_to_change_to_correct_path"
    path_to_config = path_to_config or os.getenv("CONFIG_SSM_PARAMETER", config_path)

    ssm = boto3.Session(region_name='us-east-1').client('ssm')

    param = ssm.get_parameter(Name=path_to_config, WithDecryption=True)
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


@property
def dynamo_endpoint():
    """
    returns dynamodb endpoint
    """
    return LOCAL_DYNAMO_ENDPOINT if is_local_env() else None


@property
def s3_endpoint():
    """
    returns s3 endpoint
    """
    return LOCAL_S3_ENDPOINT if is_local_env() else None


@property
def sqs_endpoint():
    """
    returns sqs endpoint
    """
    return LOCAL_SQS_ENDPOINT if is_local_env() else None


@property
def dynamo_table_name():
    """
    returns table name from parameter store
    """
    if is_local_env():
        return LOCAL_TABLE_NAME
    else:
        # get data from parameter store with correct key
        # table_name = get_params_from_ssm()["CORRECT_KEY"]
        return "table_name"


@property
def s3_bucket_name():
    """
    returns s3 bucket name from parameter store
    """
    if is_local_env():
        return LOCAL_BUCKET_NAME
    else:
        # get data from parameter store with correct key
        # bucket_name = get_params_from_ssm()["CORRECT_KEY"]
        return "bucket_name"


@property
def sqs_name():
    """
    returns sqs name from parameter store
    """
    if is_local_env():
        return LOCAL_QUEUE_NAME
    else:
        # get data from parameter store with correct key
        # sqs_name = get_params_from_ssm()["CORRECT_KEY"]
        return "sqs_name"
