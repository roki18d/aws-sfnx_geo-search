# coding: utf-8
import os
import json
import time
import pprint
import urllib
import requests
import traceback

client_id = os.environ["CLIENT_ID"]

class UnexpectedError(Exception):
    pass

def lambda_handler(event, context): 
    
    service_key = "placeinfo"
    threshold = 20
    
    if event.get("skip"): 
        response_body = {'statusCode': 200, 'body': {service_key: None}}
        return response_body

    if event.get("pause"): 
        time.sleep(int(event.get("pause")))

    try: 
        lat = str(urllib.parse.quote(event["coordinates"]["lat"]))
        lon = str(urllib.parse.quote(event["coordinates"]["lon"]))
        url = f"https://map.yahooapis.jp/placeinfo/V1/get?lat={lat}&lon={lon}&appid={client_id}&output=json"
        pprint.pprint(f"url: {url}")
        api_response = json.loads(requests.get(url).text)
        pprint.pprint(f"api_response.keys(): {api_response.keys()}")
        pprint.pprint(f"api_response: {api_response}")
        api_results = api_response["ResultSet"]["Result"]

        results = list()

        for result in api_results:
            uid = result["Uid"] 
            name = result["Name"]
            score = float(result["Score"])
            if score >= threshold: 
                result = {"Uid": uid, "Name": name, "Score": score}
                results.append(result)
        
        response_body = {service_key: results}
        return {'statusCode': 200, 'body': response_body}
        
    except Exception as e:
        traceback_message = traceback.format_exc()
        pprint.pprint(traceback_message)
        raise UnexpectedError(traceback_message)
