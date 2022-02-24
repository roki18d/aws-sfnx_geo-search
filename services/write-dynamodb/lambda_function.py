# coding: utf-8
import os
import json
import pprint
import traceback

import boto3

client_id = os.environ["CLIENT_ID"]

class UnexpectedError(Exception):
    pass

def lambda_handler(event, context): 

    try: 
        response_body = {"report": None}
        return {'statusCode': 200, 'body': response_body}

    except Exception as e:
        traceback_message = traceback.format_exc()
        pprint.pprint(traceback_message)
        raise UnexpectedError(traceback_message)
