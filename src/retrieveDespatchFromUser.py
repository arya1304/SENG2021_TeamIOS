import json
import boto3
from boto3.dynamodb.conditions import Attr
from datetime import datetime

def lambda_handler(event, context):
    
    # Retrieve the database 
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DespatchAdviceTable')

    # Check if event contains the despatch ID, if not return response: 400
    params = event.get('queryStringParameters', {})
    
    user = params.get('username')
    if not user:
        return {
            "statusCode": 400,
            "message": "Bad Request - user is not provided"
        }

    response = table.scan(
        FilterExpression=Attr('username').eq(user)
    )

    # if item doesn't exist in the response, return response: 404
    if not response.get('Items', []):
        return {
            "statusCode": 404,
            "message": "Not Found"
        }
    
    items = response.get('Items', [])

    #get only the 'ID' field from all items
    ids = [item['ID'] for item in items]

    return {
        'statusCode': 200,
        'despatchAdvices from the same user': {
            "despatchAdvicesIDs": [f"ID: {id}" for id in ids]
        }
    }
   
