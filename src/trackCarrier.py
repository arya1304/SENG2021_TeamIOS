import json, os, boto3, requests
from datetime import datetime

TABLE_NAME = "DespatchAdviceTable"

CARRIER_URL = {
    "UPS":   "https://api.mockups.com/track/",
    "FedEx": "https://api.mockfedex.com/track/"
}


def lambda_handler(event, context):
    despatch_id = event.get("pathParameters", {}).get("despatchId")
    if not despatch_id:
        return _resp(400, "Bad Request – despatchId not provided")

    dynamodb = boto3.resource("dynamodb")
    table    = dynamodb.Table(TABLE_NAME)

    item = table.get_item(Key={"ID": despatch_id}).get("Item")
    if not item:
        return _resp(404, "Not Found – invalid despatchId")

    carrier = item.get("Carrier")
    tracking_no = item.get("TrackingNumber")
    if not carrier or not tracking_no:
        return _resp(400, "Bad Request – Carrier / TrackingNumber missing")

    # call external carrier API (mocked in unit‑tests)
    api_url = f"{CARRIER_URL.get(carrier, '')}{tracking_no}"
    try:
        r = requests.get(api_url, timeout=5)
        if r.status_code != 200:
            return _resp(502, "Bad Gateway – carrier API error")
        # expected keys: status, location, eta
        data = r.json()
    except requests.RequestException:
        return _resp(502, "Bad Gateway – carrier API unreachable")

    # persist latest status back to DynamoDB
    table.update_item(
        Key={"ID": despatch_id},
        UpdateExpression="SET TrackingStatus = :s, TrackingLastUpdated = :t",
        ExpressionAttributeValues={
            ":s": json.dumps(data),
            ":t": datetime.utcnow().isoformat()
        }
    )

    return {
        "statusCode": 200,
        "tracking": data,
        "despatchId": despatch_id
    }


def _resp(code, msg):
    return {"statusCode": code, "body": msg}
