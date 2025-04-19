import json
import uuid
import boto3
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DespatchAdviceProducts')


    # Get product information from json body
    product_details = event.get('body', {})

    # Check if a product with this name exists, if it does, return an error
    # make name a global index
    
    response = table.scan(
        FilterExpression=Attr('Name').eq(product_details.get('Name'))
    )
    
    # if item doesn't exist in the response, return response: 404
    if response.get('Items', []):
        return {
            "statusCode": 404,
            "message": "A product with this name already exists"
        }

    product = {
        'ID' : str(uuid.uuid4()),
        'Name' : product_details.get('Name'),
        'Quantity' : product_details.get('Quantity'),
        'Description' : product_details.get('Description'),
        'LotNumber' : product_details.get('LotNumber')
    }

    table.put_item(Item=product)

    return {
        'statusCode': 200,
        'body': product
    }
