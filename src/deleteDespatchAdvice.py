import boto3
import json

def lambda_handler(event, context):
    # Retrieve the database 
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DespatchAdviceTable')

    # Check if event contains the despatch ID, if not return response: 400
    if 'despatchId' not in event.get('pathParameters', {}):
        return {
            "statusCode": 400,
            "body": "Bad Request - The despatch ID is not provided"
        }
    
    # Get the ID from the event json
    despatch_id = event['pathParameters']['despatchId']
    # Grab the corresponding item from the table
    item_to_delete = table.get_item(Key={'ID': despatch_id})
    
    # if item doesn't exist in the response, return response: 404
    if 'Item' not in item_to_delete:
        return {
            "statusCode": 404,
            "body": "Not Found - The despatch ID is invalid"
        }

    # If the item exists, continue to delete the item associated with the ID
    table.delete_item(Key={'ID': despatch_id})
    
    # return success response: 200
    return {
        "statusCode": 200,
        "body": f"Success - Despatch advice {despatch_id} deleted successfully"
    }