import boto3
from datetime import datetime,timedelta
import jwt

SECRET_KEY = "hello"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def createtoken(username:str):
    expire = datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "username": username,
        "expire": expire
    }
    encoded_token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_token

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DespacthAdviceUsers') 
    username = event['pathParameters']['username']
    password = event['pathParameters']['password']

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
    
    #generate a jwt token and store it in the username database
    token = createtoken(username)

    return {
        "statusCode": 200,
        "token" : token
    }