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
    
    start_date_str = params.get('startDate')
    end_date_str = params.get('endDate')

    if not start_date_str or not end_date_str:
        return {
            "statusCode": 400,
            "message": "Bad Request - Either StartDate or EndDate is not provided"
        }
    
    try:
        start_date = datetime.strptime(start_date_str, '%d-%m-%Y')
        end_date = datetime.strptime(end_date_str, '%d-%m-%Y')
    except ValueError:
        return {
            "statusCode": 400,
            "message": "Bad Request - Invalid date format. Use DD-MM-YYYY"
        }

    response = table.scan(
        FilterExpression=Attr('ShipmentCountry').eq(country)
    )

    # if item doesn't exist in the response, return response: 404
    if not response.get('Items', []):
        return {
            "statusCode": 404,
            "message": "Not Found - The country is invalid"
        }
    
    items = []
    for item in response.get('Items', []):
        if 'ShipmentDate' in item:
            try:
                ship_date_str = item['ShipmentDate']
                ship_date = datetime.strptime(ship_date_str, '%d-%m-%Y')
                
                # Check if within date range
                if start_date <= ship_date <= end_date:
                    items.append(item)
            except ValueError:
                continue

    #get only the 'ID' field from all items
    ids = [item['ID'] for item in items]

    return {
        'statusCode': 200,
        'despatchAdvices with same ShipmentCountry in same period': {
            "despatchAdvicesIDs": [f"ID: {id}" for id in ids]
        }
    }
   