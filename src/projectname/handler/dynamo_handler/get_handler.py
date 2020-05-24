"""
retrieve data from dynamo db
"""

import logging
from ...exceptionhelper.exception_handler import lambda_exception_handler
from ...awshelper.awswraper import DynamoDB

# disable pylint warning about unused 'context' argument
# pylint: disable=unused-argument


@lambda_exception_handler
def get(event, context):
    """
    get data from dynamo
    TODO: need proper error handling
    """
    logging.info(event["path"])
    key = event['path'].split("/")[-1]
    return DynamoDB().retrieve_from_dynamo(key)
