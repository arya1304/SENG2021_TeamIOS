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
    
    country = params.get('country')
    if not country:
        return {
            "statusCode": 400,
            "message": "Bad Request - Country is not provided"
        }
    
    start_date = params.get('startDate')
    end_date = params.get('endDate')

    if not start_date or not end_date:
        return {
            "statusCode": 400,
            "message": "Bad Request - Either StartDate or EndDate is not provided"
        }

    response = table.scan(
        FilterExpression=Attr('ShipmentCountry').eq(country) &
                         Attr('EarliestDeliveryDate').eq(start_date) &
                         Attr('LatestDeliveryDate').eq(end_date)
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
        'despatchAdvices with same ShipmentCountry in same period': {
            "despatchAdvicesIDs": [f"ID: {id}" for id in ids]
        }
    }
   
