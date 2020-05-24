"""
This is the sample code waiting event from SQS,
then read the data from S3 then insert data to dynamodb
It is just a sample. It doesn't include proper error handling codes

"""
import json

from ...exceptionhelper.exception_handler import lambda_exception_handler
from ...awshelper.awswraper import DynamoDB


# disable pylint warning about unused 'context' argument
# pylint: disable=unused-argument


@lambda_exception_handler
def post(event, context):
    """
    inserting the data from REST input to dynamo
    """

    input_data = json.loads(event['body'])

    return DynamoDB().insert_to_dynamo(input_data)
