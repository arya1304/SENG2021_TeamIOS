import json
import boto3

def lambda_handler(event, context):
    # 1) Parse path parameter for despatchId
    path_params = event.get('pathParameters', {})
    despatch_id = path_params.get('despatchId', None)

    if not despatch_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Bad Request - The despatch ID is not provided"})
        }

    # 2) Parse the body for deliveredQuantity and backorderQuantity
    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Bad Request - Malformed JSON in request body"})
        }

    delivered_quantity = body.get("deliveredQuantity", None)
    backorder_quantity = body.get("backorderQuantity", None)

    if delivered_quantity is None or backorder_quantity is None:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Bad Request - Must include deliveredQuantity and backorderQuantity in body"})
        }

    # 3) Retrieve the database/table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DespatchAdviceTable')

    # 4) Check if item exists
    existing_item = table.get_item(Key={'ID': despatch_id})
    if 'Item' not in existing_item:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Not Found - The despatch ID is invalid"})
        }

    # 5) Update the deliveredQuantity and backorderQuantity
    #    in your DynamoDB table. For simplicity, we store them
    #    as top-level attributes named 'DeliveredQuantity' and 'BackorderQuantity'.
    table.update_item(
        Key={'ID': despatch_id},
        UpdateExpression="SET DeliveredQuantity = :d, BackorderQuantity = :b",
        ExpressionAttributeValues={
            ':d': str(delivered_quantity),
            ':b': str(backorder_quantity)
        }
    )

    # Return success
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Successfully updated Despatch Advice {despatch_id}",
            "DeliveredQuantity": delivered_quantity,
            "BackorderQuantity": backorder_quantity
        })
    }
