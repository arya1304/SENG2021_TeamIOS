import json
import boto3
from datetime import datetime

def lambda_handler(event, context):

    client = boto3.client('dynamodb')
    response = client.scan(TableName='DespatchAdviceTable')
    items = response.get('Items', [])

    items.sort(key=lambda x: x['EarliestDeliveryDate']['S'])
    earliest_delivery_date = items[0]['EarliestDeliveryDate']['S']

    earliest_items = [item for item in items if item['EarliestDeliveryDate']['S'] == earliest_delivery_date]
    
    ids = [item['ID']['S'] for item in earliest_items]
    
    return {
        'statusCode': 200,
        'count': f"There are {len(ids)} despatch advices with the earliest delivery date: {earliest_delivery_date}",
        'despatchAdvices': {
            "despatchAdvicesIDs": [f"ID: {id}" for id in ids]
        }
    }
