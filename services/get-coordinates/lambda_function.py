# coding: utf-8
import os
import json
import pprint
import urllib
import requests

def lambda_handler(event, context): 
    
    try: 
        query_encoded = urllib.parse.quote(event["QUERY_JA"])
        client_id = os.environ["CLIENT_ID"]
        url = f"https://map.yahooapis.jp/geocode/V1/geoCoder?appid={client_id}&output=json&query={query_encoded}"
        api_response = json.loads(requests.get(url).text)
        [lon, lat] = [float(x) for x in api_response["Feature"][0]["Geometry"]["Coordinates"].split(",")]
        response_body = {"lon": lon, "lat": lat}
        return {'statusCode': 200, 'body': response_body}

    except Exception as e:
        response_body = {"lon": None, "lat": None}
        return {'statusCode': 500, 'body': response_body}