import boto3
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DespatchAdviceProducts')

    # Check if event contains the despatch ID, if not return response: 400
    if 'Name' not in event.get('pathParameters', {}):
        return {
            "statusCode": 400,
            "body": "Bad Request - The Name of the product is not provided"
        }


    product_name = event['pathParameters']['Name']

    response = table.scan(
        FilterExpression=Attr('Name').eq(product_name)
    )
    
    # if item doesn't exist in the response, return response: 404
    if not response.get('Items', []):
        return {
            "statusCode": 404,
            "message": "Product with this name does not exist"
        }

    # Get the CustomerContactDetails attribute string from the Item associated with ID
    product_details = response['Items'][0]

    details = {
        'Description': product_details['Description'],
        'Quantity': product_details['Quantity'],
        'LotNumber': product_details['LotNumber'],
    }
    return {
        'statusCode': 200,
        'body': details
    }
