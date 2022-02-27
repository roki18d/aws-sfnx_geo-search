# coding: utf-8
import os
import json
import pprint
import hashlib
import traceback
import datetime as dt


class UnexpectedError(Exception):
    pass

def lambda_handler(event, context): 
    
    precision = 4
    base = 10**precision

    try:
        now = dt.datetime.now()
        timestamp = now.strftime('%Y%m%d%H%M%S%f')
        hash16 = hashlib.md5(timestamp.encode()).hexdigest()
        unirand = (int(hash16, 16)%base)/base

        response_body = {'unirand': unirand}
        return {'statusCode': 200, 'body': response_body}

    except Exception as e:
        traceback_message = traceback.format_exc()
        pprint.pprint(traceback_message)
        raise UnexpectedError(traceback_message)
