import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DespatchAdviceUsers')
def lambda_handler(event, context):
    # Retrieve the database 

    # Check if event contains the despatch ID, if not return response: 400
    if 'username' not in event.get('pathParameters', {}):
        return {
            "statusCode": 400,
            "message": "Bad Request - The username is not provided"
        }
    
    # get the user from event
    user = event['pathParameters']['username']
    # get the corresponding item from the db
    item_to_delete = table.get_item(Key={'username': user})
    
    # if item doesn't exist, return response: 404
    if 'Item' not in item_to_delete:
        return {
            "statusCode": 404,
            "message": "No content - The username is invalid"
        }

    # continue to delete the item associated with the ID
    table.delete_item(Key={'username': user})
    
    #return success response: 200
    return {
        "statusCode": 200
    }


