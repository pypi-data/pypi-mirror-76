from dotenv import load_dotenv
import os
import requests
import json
from ivolve_cloud7_logger import Console
load_dotenv()
data={
        "type_": "log",
        "message": "success",
        "url": 'my url',
        "messageType": {
            "request_payload": {},
            "response_payload": {},
        },        
        "project_id": 'my project id',
        "user_id": 'my user id',
        "domain_id": "default",
        }
Console.log(data)