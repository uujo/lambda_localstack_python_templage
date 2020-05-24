"""
Wrapper for AWS services
"""
import time
import boto3
from .awsenv import dynamo_endpoint, dynamo_table_name

# pylint: disable=no-member

class DynamoDB:
    """
    wrapper class for dynamo db
    """

    def __init__(self):
        """
        initializing dynamo table
        """
        dynamo = boto3.resource("dynamodb", endpoint_url=dynamo_endpoint())
        self.dynamo_table = dynamo.Table(dynamo_table_name())

    def retrieve_from_dynamo(self, key):
        """
        retrieve data to dynamodb
        """
        result = self.dynamo_table.get_item(Key={"id": key})
        return result.get("Item", {})

    def insert_to_dynamo(self, data):
        """
        insert data to dynamodb
        """

        item = {"created": int(time.time()), "last_updated": int(time.time())}
        item.update(data)
        return self.dynamo_table.put_item(Item=item)

    def delete_from_dynamo(self, key):
        """
        delete data from dynamodb
        """
        return self.dynamo_table.delete_item(Key={"id": key})

    def update_to_dynamo(self, key, data):
        """
        update data to dynamodb
        """

        result = self.dynamo_table.update_item(
            Key={"id": key},
            UpdateExpression="SET test_data = :r, last_updated = :n",
            ExpressionAttributeValues={':r': data['test_data'], ':n': int(time.time())},
        )
        return result
