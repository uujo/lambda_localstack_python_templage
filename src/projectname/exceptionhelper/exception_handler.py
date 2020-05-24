"""
 Handles various exceptions for validation and db exceptoin
 Convert exception to lamdba response
"""

import json
import traceback
from functools import wraps

# disable pylint exception warning
# pylint: disable=broad-except


def lambda_exception_handler(lambda_func):
    """

    This decorator will handle the exceptions occurred during the lambda processing
    by providing responsed depending on the exceptions handinged
    :param lambda_func: aws lambda function
    :return: wrapped function
    """

    @wraps(lambda_func)
    def wrapper(event, context):
        """
        :param event: aws event
        :param context: aws context
        :return: aws lambda response i.e. {"statusCode": 200, "body": results, "header": {} }
        """
        try:
            data = lambda_func(event, context)

            response = {
                "statusCode": 200,
                "body": json.dumps(data, default=float),  # assuming we have only Decimal encoding problem
                "headers": {"Content-Type": "application/json"},
            }
            return response

        except (json.JSONDecodeError, TypeError) as ex:
            return {
                "statusCode": 400,
                "body": json.dumps({"input_error": f"Input JSON error: {str(ex)}: {event['body']}"}),
                "headers": {"Content-Type": "application/json"},
            }

        except Exception as ex:
            response = {"statusCode": 500, "body": "Server error. {}".format(traceback.format_exc())}
            return response

    return wrapper


def invalid_input_key_check(key, input_data):
    """
    :param key:
    :param input_data:
    :return:
    """
    if key in input_data:
        return {
            "statusCode": 400,
            "body": json.dumps({"input_error": "id field cannot be updated"}),
            "headers": {"Content-Type": "application/json"},
        }

    return {}
