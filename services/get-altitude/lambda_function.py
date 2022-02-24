# coding: utf-8
import os
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
        response_body = {"altitude": altitude}
        return {'statusCode': 200, 'body': response_body}

    except Exception as e:
        traceback_message = traceback.format_exc()
        pprint.pprint(traceback_message)
        raise UnexpectedError(traceback_message)
