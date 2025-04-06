import boto3
import jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

def lambda_handler(event, context):
    header_token = event['authorizationToken']
    encoded_token = header_token.split(" ")[1] 

    try:
        decoded_token = jwt.decode(encoded_token, SECRET_KEY, algorithms=[ALGORITHM])
        authResponse = {
            "principalId": decoded_token["email"],
            'policyDocument': { 
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Action': 'execute-api:Invoke',
                        'Resource': [
                            event['methodArn']
                        ], 
                        'Effect': 'Allow'
                    }
                ]
            }
        }        
        return authResponse
    except jwt.ExpiredSignatureError:
        authResponse = {
            'policyDocument': { 
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Action': 'execute-api:Invoke',
                        'Resource': [
                            event['methodArn']
                        ], 
                        'Effect': 'Deny'
                    }
                ]
            }
        }
        return  authResponse
    except jwt.InvalidTokenError:
        authResponse = {
            'policyDocument': { 
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Action': 'execute-api:Invoke',
                        'Resource': [
                            event['methodArn']
                        ], 
                        'Effect': 'Deny'
                    }
                ]
            }
        }

        return authResponse
    

