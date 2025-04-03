import boto3
from fastapi import APIRouter, HTTPException

router = APIRouter()

def update_delivery_period(request):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("ShipmentTable")
    
    if not isinstance(request, dict):
        return {"statusCode": 400, "message": "Invalid input parameters"}
    
    if "shipment_id" not in request or "new_delivery_period" not in request:
        return {"statusCode": 400, "message": "Invalid input parameters"}
        
    shipment_id = request["shipment_id"]
    new_delivery_period = request["new_delivery_period"]
    
    response = table.get_item(Key={"ID": shipment_id})
    if "Item" not in response:
        return {"statusCode": 404, "message": "Shipment not found"}
    
    table.update_item(
        Key={"ID": shipment_id},
        UpdateExpression="set DeliveryPeriod = :new_delivery_period",
        ExpressionAttributeValues={":new_delivery_period": new_delivery_period},
    )
    
    return {
        "statusCode": 200,
        "message": "Shipment delivery period updated successfully",
        "shipment_id": shipment_id
    }