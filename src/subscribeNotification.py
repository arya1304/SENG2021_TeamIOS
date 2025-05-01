import json, uuid, boto3

#  DynamoDB table to store subscriptions
TABLE_NAME = "SubscriptionTable"

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return {"statusCode": 400,
                "body": "Bad Request – malformed JSON in body"}

    # could also be sms / webhookUrl
    email       = body.get("email")
    # CREATE | UPDATE | DELETE
    event_type  = body.get("eventType")
    # “ALL” = global subscription
    despatch_id = body.get("despatchId", "ALL")

    if not email or not event_type:
        return {"statusCode": 400,
                "body": "Bad Request – email and eventType are required"}

    subscription_id = str(uuid.uuid4())

    dynamodb = boto3.resource("dynamodb")
    table    = dynamodb.Table(TABLE_NAME)
    table.put_item(Item={
        "SubscriptionID": subscription_id,
        "Email":          email,
        "EventType":      event_type,
        "DespatchId":     despatch_id,
    })

    return {"statusCode": 201,
            "subscriptionId": subscription_id}
