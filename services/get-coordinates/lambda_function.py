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
        query_encoded = urllib.parse.quote(event["query"])
        url = f"https://map.yahooapis.jp/geocode/V1/geoCoder?appid={client_id}&output=json&query={query_encoded}"
        api_response = json.loads(requests.get(url).text)
        [lon, lat] = api_response["Feature"][0]["Geometry"]["Coordinates"].split(",")
        coordinates = {"lat": lat, "lon": lon}
        response_body = {"coordinates": coordinates}
        return {'statusCode': 200, 'body': response_body}

    except Exception as e:
        pprint.pprint(traceback.format_exc())
        response_body = {"coordinates": None, "traceback": traceback.format_exc()}
        return {'statusCode': 500, 'body': response_body}