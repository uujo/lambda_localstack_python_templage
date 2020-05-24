"""
lambda function handling delete
"""

from ...exceptionhelper.exception_handler import lambda_exception_handler
from ...awshelper.awswraper import DynamoDB

# disable pylint warning about unused 'context' argument
# pylint: disable=unused-argument


@lambda_exception_handler
def delete(event, context):
    """
    get data from dynamo
    TODO: need proper error handling
    """

    key = event['path'].split("/")[-1]

    return DynamoDB().delete_from_dynamo(key)
