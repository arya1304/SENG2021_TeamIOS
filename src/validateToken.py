import boto3
import jwt

SECRET_KEY = "hello"
ALGORITHM = "HS256"


# https://www.youtube.com/watch?v=5kI2wZWp4NU&ab_channel=RahulNath

def lambda_handler(event, context):
    encoded_token = event['authorizationToken'] 
    #this decode and verifies our token
    try:
        decoded = jwt.decode(jwt=encoded_token, key=SECRET_KEY, algorithms=["HS256"])
        auth_status = "Allow"
    except jwt.ExpiredSignatureError:
        auth_status = "Deny"
        print("Expired token1")
    except jwt.InvalidTokenError:
        auth_status="Deny"
        print("Expired token2")
    except jwt.InvalidSignatureError:
        auth_status="Deny"
        print("Expired token3")
    
    authResponse = {
        'principalId': decoded['username'],
        'policyDocument': { 
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Resource': [
                        event['methodArn']
                    ], 
                    'Effect': auth_status
                }
            ]
        },
        "context":{
            "username": decoded['username']
        }
    }
    return authResponse