import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DespatchAdviceTable')
    
    # Check if event contains the supplier name, if not return response: 400
    if 'Supplier' not in event.get('pathParameters', {}):
        return {
            "statusCode": 400,
            "body": "Bad Request - The despatch ID is not provided"
        }

    # Get the name of the supplier
    supplier_name = event['pathParameters']['Supplier']
    
    #Query the table 
    table_supplier = table.query(
        KeyCondtionExpression=Key('Supplier').eq(supplier_name)
    )

    #from the table, get all items with the same supplier
    ids = [item['ID']['N'] for item in table_supplier.get('Items', [])]
    if not ids:
        return {
            "statusCode": 204,
            "body": {"message": "No despatch advices found for this supplier"}
        }

    
    return {
        'statusCode': 200,
        'count': "There are " + ids.count() + "Despatch Advices from " + supplier_name,
        'despatchAdvices': {
            "despatchAdvicesIDs": [f"ID: {id}" for id in ids]
        }
    }