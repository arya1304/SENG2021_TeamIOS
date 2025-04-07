import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('dynamodb')

    # Scan the table to retrieve all items
    response = client.scan(TableName='DespatchAdviceUsers')

    # Extract only the 'ID' field from all items
    users = [item['username']['S'] for item in response.get('Items', [])]
    if not users:
        return {
            "statusCode": 204,
            "body": {"message": "No users found"}
        }

    return {
        'statusCode': 200,
        'users': {
            "users": [f"username: {id}" for id in users]
        }
    }