# coding: utf-8
import os
import json
import pprint
import urllib
import requests
import traceback

client_id = os.environ["CLIENT_ID"]

def lambda_handler(event, context): 
    
    try: 
        lat = str(urllib.parse.quote(event["coordinates"]["lat"]))
        lon = str(urllib.parse.quote(event["coordinates"]["lon"]))

        url = f"https://map.yahooapis.jp/geoapi/V1/reverseGeoCoder?lat={lat}&lon={lon}&appid={client_id}&output=json"
        print(url)
        api_response = json.loads(requests.get(url).text)
        address_reversed = api_response["Feature"][0]["Property"]["Address"]
        response_body = {"address": address_reversed}
        return {'statusCode': 200, 'body': response_body}

    except Exception as e:
        pprint.pprint(traceback.format_exc())
        response_body = {"address": None, "traceback": traceback.format_exc()}
        return {'statusCode': 500, 'body': response_body}
