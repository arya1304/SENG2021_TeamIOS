import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    
    # Retrieve the database 
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DespatchAdviceTable')

    # Check if event contains the despatch ID, if not return response: 400
    supplier_name = event.get('queryStringParameters', {}).get('Supplier')
   
    if not supplier_name:
        return {
            "statusCode": 400,
            "message": "Bad Request - Supplier is not provided"
        }

    response = table.query(
            IndexName="Supplier",
            KeyConditionExpression=Key('Supplier').eq(supplier_name)
    )

    # if item doesn't exist in the response, return response: 404
    if not response.get('Items', []):
        return {
            "statusCode": 404,
            "message": "Not Found - The supplier name is not found"
        }
    
    items = response.get('Items', [])
    #get only the 'ID' field from all items
    ids = [item['ID'] for item in items]

    return {
        'statusCode': 200,
        'count': "There are " + str(len(ids)) + " " + "Despatch Advices from " + supplier_name,
        'despatchAdvices': {
            "despatchAdvicesIDs": [f"ID: {id}" for id in ids]
        }
    }