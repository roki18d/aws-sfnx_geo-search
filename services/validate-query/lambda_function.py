# coding: utf-8
import os
import re
import json
import pprint
import urllib
import requests
import traceback

client_id = os.environ["CLIENT_ID"]
function_name_get_unirand = os.environ["FUNCTION_NAME_GET_UNIRAND"]

class IntentionalError(Exception):
    pass

class UnexpectedError(Exception):
    pass

def lambda_handler(event, context): 

    ie_ratio_str = event.get("intentional_error_ratio")
    pprint.pprint(f'intentional_error_ratio: {ie_ratio_str}')
    if ie_ratio_str: 
        ie_ratio = float(ie_ratio_str)
        import boto3; lambda_client = boto3.client('lambda')
        response = lambda_client.invoke(
            FunctionName=function_name_get_unirand, )
        unirand = response['Payload']['body']['unirand']
        if unirand < ie_ratio: 
            msg = f'intentional_error_ratio: {ie_ratio}, unirand: {unirand}'
            raise IntentionalError(msg)
            
    try: 
        address_query = event["address_query"]
        address_reversed = event["address_reversed"]

        query_isvalid = False
        if address_reversed.startswith(address_query):
            query_isvalid = True

        response_body = {"query_isvalid": query_isvalid}
        return {'statusCode': 200, 'body': response_body}

    except Exception as e:
        traceback_message = traceback.format_exc()
        pprint.pprint(traceback_message)
        raise UnexpectedError(traceback_message)
