# coding: utf-8
import os
import json
import time
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

    service_key = "weather"
    api_config_past = str(1)
    api_config_interval = str(10)

    if event.get("skip"): 
        response_body = {'statusCode': 200, 'body': {service_key: None}}
        return response_body

    if event.get("pause"): 
        time.sleep(int(event.get("pause")))

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
        lat = str(urllib.parse.quote(event["coordinates"]["lat"]))
        lon = str(urllib.parse.quote(event["coordinates"]["lon"]))
        coordinates = ",".join([lon, lat])
        url = f"https://map.yahooapis.jp/weather/V1/place?" + \
            f"coordinates={coordinates}&" + \
            f"past={api_config_past}&" + \
            f"interval={api_config_interval}&" + \
            f"appid={client_id}&" + \
            "output=json"
        pprint.pprint(f"url: {url}")
        api_response = json.loads(requests.get(url).text)
        pprint.pprint(f"api_response.keys(): {api_response.keys()}")
        pprint.pprint(f"api_response: {api_response}")
        weather_records = api_response["Feature"][0]["Property"]["WeatherList"]["Weather"]
        
        weather = list()
        format_date_string = lambda yyyymmddhhmmss: f"{yyyymmddhhmmss[:4]}-{yyyymmddhhmmss[4:8]}-{yyyymmddhhmmss[8:]}"
        for record in weather_records:
            record_type = record["Type"]
            record_date = format_date_string(record['Date'])
            rainfall = record["Rainfall"]
            formatted_record = {"Type": record_type, "Date": record_date, "Rainfall": rainfall}
            weather.append(formatted_record)

        response_body = {service_key: weather}
        return {'statusCode': 200, 'body': response_body}

    except Exception as e:
        traceback_message = traceback.format_exc()
        pprint.pprint(traceback_message)
        raise UnexpectedError(traceback_message)
