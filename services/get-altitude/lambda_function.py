# coding: utf-8
import os
import json
import time
import pprint
import urllib
import requests
import traceback

import boto3
lambda_client = boto3.client('lambda')

client_id = os.environ["CLIENT_ID"]
function_name_get_unirand = os.environ["FUNCTION_NAME_GET_UNIRAND"]

class UnexpectedError(Exception):
    pass

class IntentionalError(Exception):
    pass

def lambda_handler(event, context): 
    
    service_key = "altitude"

    if event.get("skip"): 
        response_body = {'statusCode': 200, 'body': {service_key: None}}
        return response_body

    if event.get("pause"): 
        time.sleep(int(event.get("pause")))

    ie_ratio = event.get("intentional_error_ratio")
    if ie_ratio: 
        response = lambda_client.invoke(
            FunctionName=function_name_get_unirand, )
        unirand = response['Payload']['body']['unirand']
        if unirand < ie_ratio: 
            msg = f'intentional_error_ratio: {ie_ratio}, unirand: {unirand}'
            raise IntentionalError(msg)

    try: 
        lat = str(urllib.parse.quote(event["coordinates"]["lat"]))
        lon = str(urllib.parse.quote(event["coordinates"]["lon"]))
        coordinates = ",".join([lon, lat])
        url = f"https://map.yahooapis.jp/alt/V1/getAltitude?" + \
            f"coordinates={coordinates}&" + \
            f"appid={client_id}&output=json"
        pprint.pprint(f"url: {url}")
        api_response = json.loads(requests.get(url).text)
        pprint.pprint(f"api_response.keys(): {api_response.keys()}")
        pprint.pprint(f"api_response: {api_response}")
        altitude = api_response["Feature"][0]["Property"]
        response_body = {service_key: altitude}
        return {'statusCode': 200, 'body': response_body}

    except Exception as e:
        traceback_message = traceback.format_exc()
        pprint.pprint(traceback_message)
        raise UnexpectedError(traceback_message)
