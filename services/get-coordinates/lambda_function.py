# coding: utf-8
import os
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
    print(f'intentional_error_ratio: {ie_ratio_str}')
    if ie_ratio_str: 
        ie_ratio = float(ie_ratio_str)
        import boto3; lambda_client = boto3.client('lambda')
        response = lambda_client.invoke(
            FunctionName=function_name_get_unirand, 
            InvocationType='RequestResponse', )
        payload = response['Payload']
        print(payload)
        try: 
            unirand = payload['body']['unirand']
        except: 
            payload = json.loads(payload.read())
            unirand = payload['body']['unirand']
        if unirand < ie_ratio: 
            msg = f'intentional_error_ratio: {ie_ratio}, unirand: {unirand}'
            raise IntentionalError(msg)

    try: 
        query_encoded = urllib.parse.quote(event["query"])
        url = f"https://map.yahooapis.jp/geocode/V1/geoCoder?appid={client_id}&output=json&query={query_encoded}"
        pprint.pprint(f"url: {url}")
        api_response = json.loads(requests.get(url).text)
        pprint.pprint(f"api_response.keys(): {api_response.keys()}")
        pprint.pprint(f"api_response: {api_response}")
        [lon, lat] = api_response["Feature"][0]["Geometry"]["Coordinates"].split(",")
        coordinates = {"lat": lat, "lon": lon}
        response_body = {"coordinates": coordinates}
        return {'statusCode': 200, 'body': response_body}

    except Exception as e:
        traceback_message = traceback.format_exc()
        pprint.pprint(traceback_message)
        raise UnexpectedError(traceback_message)
