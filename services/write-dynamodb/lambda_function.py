# coding: utf-8
import os
import json
import pprint
import traceback
from unittest import result

import boto3

client_id = os.environ["CLIENT_ID"]

class UnexpectedError(Exception):
    pass

def lambda_handler(event, context): 

    dynamodb_table_name = 'sfnx-DynamoDB-APIResultSets'
    keys = ["placeinfo", ""]
    api_result_sets = dict()

    try: 
        states_execution_id = event["states_execution_id"]
        query = event["query"]
        result_set = event["result_set"]
        for result in result_set:
            for key in keys: 
                if key in result.keys(): 
                    api_result_sets[key] = result[key]["body"]["results"]
        

        response_body = {"api_result_sets": api_result_sets}
        return {'statusCode': 200, 'body': response_body}

    except Exception as e:
        traceback_message = traceback.format_exc()
        pprint.pprint(traceback_message)
        raise UnexpectedError(traceback_message)
