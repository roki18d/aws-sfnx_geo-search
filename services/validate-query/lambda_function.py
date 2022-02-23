# coding: utf-8
import os
import re
import json
import pprint
import urllib
import requests
import traceback

client_id = os.environ["CLIENT_ID"]

class UnexpectedError(Exception):
    pass

def lambda_handler(event, context): 

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
