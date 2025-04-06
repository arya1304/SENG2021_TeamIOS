import boto3
import jwt

SECRET_KEY = "hello"
ALGORITHM = "HS256"

def lambda_handler(event, context):
    encoded_token = event['authorizationToken'] 
    #this decode and verifies our token
    try:
        jwt.decode(jwt=encoded_token, key=SECRET_KEY, algorithms=["HS512"])
        auth_status = "Allow"
    except jwt.ExpiredSignatureError:
        auth_status = "Deny"
    except jwt.InvalidTokenError:
        auth_status="Deny"
    except jwt.InvalidSignatureError:
        auth_status="Deny"
    
    authResponse = {
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
        }
    }
    return authResponse
