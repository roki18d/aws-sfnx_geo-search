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
