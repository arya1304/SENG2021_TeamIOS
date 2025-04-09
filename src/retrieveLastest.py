import json
import boto3
from datetime import datetime

def lambda_handler(event, context):

    client = boto3.client('dynamodb')
    response = client.scan(TableName='DespatchAdviceTable')
    items = response.get('Items', [])

    items.sort(key=lambda x: x['LatestDeliveryDate']['S'], reverse=True)
    latest_delivery_date = items[0]['LatestDeliveryDate']['S']

    latest_items = [item for item in items if item['LatestDeliveryDate']['S'] == latest_delivery_date]
    
    ids = [item['ID']['S'] for item in latest_items]
    
    return {
        'statusCode': 200,
        'count': f"There are {len(ids)} despatch advices with the latest delivery date: {latest_delivery_date}",
        'despatchAdvices': {
            "despatchAdvicesIDs": [f"ID: {id}" for id in ids]
        }
    }