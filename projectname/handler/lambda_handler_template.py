"""
This is the sample code waiting event from SQS,
then read the data from S3 then insert data to dynamodb
It is just a sample. It doesn't include proper error handling codes

"""
import json
import logging
import time

import boto3

from ..awshelper.awsenv import dynamo_endpoint, s3_endpoint, dynamo_table_name, s3_bucket_name


def get_s3_data(key):
    """
    getting s3 data
    """
    s3 = boto3.resource("s3", endpoint_url=s3_endpoint)
    s3_obj = s3.Object(s3_bucket_name, key=key)
    data = s3_obj.get(ResponseContentType="application/json")
    body = json.loads(data["Body"].read())
    return body


def insert_to_dynamo(key, data):
    """
    insert data to dynamodb
    :param key:
    :param data:
    :return:
    """
    dynamo = boto3.resource("dynamodb", endpoint_url=dynamo_endpoint)
    dynamo_table = dynamo.Table(dynamo_table_name)

    item = {
        "key_id": key,
        "data": data,
        "created": int(time.time()),
        "updated": int(time.time()),
    }
    result = dynamo_table.put_item(Item=item)
    return result


def populate_dynamo(event, context):
    """
    :param event: aws event
    :param context:  aws context
    :return:
    """

    # events are triggered when new records are in the queue
    if "Records" not in event:
        logging.warning("Records are not in events")

    for record in event.get('Records', []):
        # getting message from sqs
        if record.get("eventSource") == "aws:sqs" and "body" in record:
            sqs_data = json.loads(record["body"])
            # assume sqs contains s3 bucket name and key
            data = get_s3_data(sqs_data["key"])
            insert_to_dynamo(sqs_data["key"], data)
