"""
This is just the somple code for accessing parameter store and secrets manager
"""

import os
import json
import boto3


def is_local_env():
    """
    check whether it is local env which doesn't have real aws set up.
    :return:
    """
    # This is set on template-samp.yaml
    return os.getenv("TEST_ENV")


def get_params_from_ssm(path_to_config=None):
    """
    :param path_to_config: path to the config in Parameter store
    :return: dictionary of parameters
    """

    if is_local_env():
        # TODO: this need to proper test data corresponding the parameter store data
        return {}

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

    if is_local_env():
        # TODO: this need to proper test data corresponding the secrets manager data
        return {}

    client = boto3.Session().client(service_name="secretsmanager", region_name="us-east-1")
    response = client.get_secret_value(SecretId=path_to_config)
    param_dict = json.loads(response.get('SecretString', "{}"))

    return param_dict
