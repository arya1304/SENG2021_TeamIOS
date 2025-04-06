import boto3, json
from boto3.dynamodb.conditions import Attr

TABLE_NAME = "SubscriptionTable"
TOPIC_ARN  = "arn:aws:sns:us-east-1:123456789012:DespatchAdviceNotifications"

def lambda_handler(event, context):
    event_type  = event.get("eventType")
    message     = event.get("message")
    despatch_id = event.get("despatchId")

    if not event_type or not message:
        return {"statusCode": 400,
                "body": "Bad Request – eventType and message required"}

    dynamodb = boto3.resource("dynamodb")
    table    = dynamodb.Table(TABLE_NAME)

    if despatch_id:
        filt = (Attr("EventType").eq(event_type) &
                (Attr("DespatchId").eq(despatch_id) |
                 Attr("DespatchId").eq("ALL")))
    else:
        filt = Attr("EventType").eq(event_type)

    subs = table.scan(FilterExpression=filt).get("Items", [])

    sns = boto3.client("sns")
    for sub in subs:
        sns.publish(
            TopicArn = TOPIC_ARN,
            Message  = message,
            Subject  = f"Despatch Advice {event_type}"
        )

    return {"statusCode": 200,
            "notified": len(subs)}
