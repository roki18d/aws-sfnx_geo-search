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
    pprint.pprint(f'intentional_error_ratio: {ie_ratio_str}')
    if ie_ratio_str: 
        ie_ratio = float(ie_ratio_str)
        import boto3; lambda_client = boto3.client('lambda')
        response = lambda_client.invoke(
            FunctionName=function_name_get_unirand, 
            InvocationType='RequestResponse', )
        pprint.pprint(f'response: {response}')
        unirand = response['Payload']['body']['unirand']
        if unirand < ie_ratio: 
            msg = f'intentional_error_ratio: {ie_ratio}, unirand: {unirand}'
            raise IntentionalError(msg)
    
    try:
        pprint.pprint(event)

        lat = str(urllib.parse.quote(event["coordinates"]["lat"]))
        lon = str(urllib.parse.quote(event["coordinates"]["lon"]))
        url = f"https://map.yahooapis.jp/geoapi/V1/reverseGeoCoder?lat={lat}&lon={lon}&appid={client_id}&output=json"
        pprint.pprint(f"url: {url}")
        
        api_response = json.loads(requests.get(url).text)
        pprint.pprint(f"api_response.keys(): {api_response.keys()}")
        pprint.pprint(f"api_response: {api_response}")
        address_reversed = api_response["Feature"][0]["Property"]["Address"]
        address_elements = api_response["Feature"][0]["Property"]["AddressElement"]
        
        address_lv3_dict = dict()
        for element in address_elements: 
            address_lv3_dict[element["Level"]] = element["Name"]
        
        address_lv3 = \
            address_lv3_dict["prefecture"] + \
            address_lv3_dict["city"] + \
            address_lv3_dict["oaza"]

        response_body = {
            "address": address_reversed, 
            "address_lv3": address_lv3, }

        return {'statusCode': 200, 'body': response_body}

    except Exception as e:
        traceback_message = traceback.format_exc()
        pprint.pprint(traceback_message)
        raise UnexpectedError(traceback_message)
