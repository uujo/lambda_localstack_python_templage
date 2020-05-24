"""
update data in dynamodb
"""

import json

from ...exceptionhelper.exception_handler import lambda_exception_handler, invalid_input_key_check
from ...awshelper.awswraper import DynamoDB

# disable pylint warning about unused 'context' argument
# pylint: disable=unused-argument


@lambda_exception_handler
def put(event, context):
    """
    updating data from REST input to dynamo
    """

    db_id = event['path'].split("/")[-1]
    input_data = json.loads(event['body'])

    response = invalid_input_key_check("id", input_data)
    if response:
        return response

    return DynamoDB().update_to_dynamo(db_id, input_data)
