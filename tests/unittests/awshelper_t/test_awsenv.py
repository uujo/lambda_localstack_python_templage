"""
Test aws_env module. mocking aws ssm access
"""
import json
from unittest.mock import patch
from botocore.exceptions import ClientError
from projectname.awshelper.awsenv import get_params_from_ssm, get_params_from_secretsmanager


@patch("projectname.awshelper.awsenv.boto3.Session")
def test_get_ssm_success(boto3_session):
    """
    Test successful case when get_params_from_ssm returns param
    :param boto_session:
    :return: None
    """
    PARAM = {'Parameter': {'Value': json.dumps({"TEST_TABLE": "AnnotationTable"})}}
    boto3_session().client().get_parameter.return_value = PARAM

    response = get_params_from_ssm("/test/config")
    assert response == json.loads(PARAM['Parameter']['Value'])

    # When param doesn't exists
    boto3_session().client().get_parameter.return_value = {}
    response = get_params_from_ssm("/test/config")
    assert response == {}


@patch("projectname.awshelper.awsenv.boto3.Session")
def test_get_param_success(boto3_session):
    """
    Test successful case when get_params_from_ssm returns param
    :param boto_session:
    :return: None
    """
    PARAM = {'SecretString': json.dumps({'CosmicSecrete': "abc"})}
    boto3_session().client().get_secret_value.return_value = PARAM

    response = get_params_from_secretsmanager("/test/config")
    assert response == json.loads(PARAM['SecretString'])

    # When param doesn't exists
    boto3_session().client().get_secret_value.return_value = {}
    response = get_params_from_secretsmanager("/test/config")
    assert response == {}
