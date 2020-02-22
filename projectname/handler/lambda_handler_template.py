"""
This is the sample code waiting event from SQS,
then read the data from S3 then insert data to dynamodb
It is just a sample. It doesn't include proper error handling codes

"""
import os
import json
import logging
import boto3
import time


def get_s3_data(bucket_name, key):
    """
    getting s3 data
    """
    endpoint_url = os.environ.get("LOCAL_S3_ENDPOINT")
    s3 = boto3.resource("s3", endpoint_url=endpoint_url)
    s3_obj = s3.Object(bucket_name, key=key)
    data = s3_obj.get(ResponseContentType="application/json")
    body = json.loads(data["Body"].read())
    return body


def inset_to_dynamo(key, data):
    """
    insert data to dynamodb
    :param key:
    :param data:
    :return:
    """
    endpoint_url = os.environ.get("LOCAL_DYNAMODB")
    dynamo = boto3.resource("dynamodb", endpoint_url=endpoint_url)
    table_name = os.environ.get("TEST_TABLE_NAME")
    dynamo_table = dynamo.Table(table_name)

    item = {
        "key_id": key,
        "data": data,
        "created": int(time.time()),
        "updated": int(time.time()),
    }
    result = dynamo_table.put_item(Item=item)
    return result


def populate_dyanmo(event, context):
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
            data = get_s3_data(sqs_data["bucket_name"], sqs_data["key"])
            inset_to_dynamo(sqs_data["key"], data)


