import boto3
from datetime import datetime,timedelta
import jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def createtoken(username:str):
    expire = datetime.now()+timedelta(hours=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "username": username,
        "expire": expire
    }
    encoded_token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_token

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users') # table name might change
    username = event['pathParameters']['Username']
    password = event['pathParameters']['Password']

    response = table.get_item(Key={'username' : username})
    if 'Item' not in response:
        return {
            "statusCode": 404,
            "body": "This user does not exist"
        }

    #check if the username and password is correct
    user_details = response['Item']
    password_from_database = user_details.get("password")
    if password_from_database != password:
        return {
            "statusCode": 404,
            "body": "You have entered an incorrect password"
        }
    
    #generate a jwt token
    token = createtoken(username)

    return {
        "statusCode": 200,
        "token" : token
    }