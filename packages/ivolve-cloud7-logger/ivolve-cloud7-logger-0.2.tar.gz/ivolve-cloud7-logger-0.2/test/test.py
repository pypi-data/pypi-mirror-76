from index import Console
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