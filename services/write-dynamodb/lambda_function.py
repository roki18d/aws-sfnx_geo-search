# coding: utf-8
import os
import json
import pprint
import traceback
import datetime as dt

import boto3

client_id = os.environ["CLIENT_ID"]
dynamodb_client = boto3.client("dynamodb")

class UnexpectedError(Exception):
    pass

def lambda_handler(event, context): 

    dynamodb_table_name = 'sfnx-DynamoDB-APIResultSets'
    keys = ["placeinfo", "altitude", "weather"]

    try:
        pprint.pprint(event)
        
        # Set Table Schema
        lon = str(event["coordinates"]["lon"])
        lat = str(event["coordinates"]["lat"])
        coordinates =  f"{lon},{lat}"
        created_time = dt.datetime.now().strftime("%Y-%m%d-%H%M%S")

        # Set Attributes
        states_execution_id = event["states_execution_id"]
        address_lv3 = event["result_set"]
        query = event["query"]
        result_set = event["result_set"]

        report = dict()
        for result in result_set:
            for key in keys: 
                if key in result.keys(): 
                    report[key] = result[key]["body"][key]

        # Write to DynamoDB
        response_writedb = dynamodb_client.put_item(
            TableName=dynamodb_table_name, 
            Item={
                "Coordinates": {"S": coordinates}, 
                "CreatedTime": {"S": created_time},
                "StatesExecutionId": {"S": states_execution_id},
                "Query": {"S": query}, 
                "AddressLv3": {"S": address_lv3}, 
                "Report": {"S": report}
            }, 
        )

        response_body = {
            "coordinates": coordinates, 
            "created_time": created_time, 
            "states_execution_id": states_execution_id, 
            "query": query, 
            "address_lv3": address_lv3, 
            "report": report, 
            "response_write_dynamodb": response_writedb, }
        
        return {'statusCode': 200, 'body': response_body}

    except Exception as e:
        traceback_message = traceback.format_exc()
        pprint.pprint(traceback_message)
        raise UnexpectedError(traceback_message)
