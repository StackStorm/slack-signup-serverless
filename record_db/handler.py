import json
import logging
import os

import boto3
dynamodb = boto3.resource('dynamodb')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def endpoint(event, context):
    logger.info("Event received: {}".format(json.dumps(event)))
    try:
        item = {k: event[k].replace("%27", "'") for k in ['email', 'first_name', 'last_name'] if len(str(event[k]))}
    except KeyError as e:
        logger.error("ERROR: Can not parse `event`: '{}'\n{}".format(str(event), str(e)))
        raise
    try:
        table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    except KeyError:
        logger.error("ERROR: Environment variable DYNAMODB_TABLE must be set.")
        raise

    table.put_item(Item=item)
    return {
        "statusCode": 200,
        "body": json.dumps(item)
    }
