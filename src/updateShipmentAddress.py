import boto3
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class UpdateAddressRequest(BaseModel):
    shipment_id: str
    new_address: str

@router.patch("/shipment/update-address/")
def update_shipment_address(request):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DespatchAdviceTable')

    if isinstance(request, dict):
        if not request.get("shipment_id") or not request.get("new_address"):
            return {
                "statusCode": 400,
                "body": "Bad Request - The shipment ID or new address is not provided"
            }
        
        shipment_id = request["shipment_id"]
        new_address = request["new_address"]
    else:
        shipment_id = request.shipment_id
        new_address = request.new_address

    if new_address.strip() == "":
        return {
            "statusCode": 400,
            "body": "Bad Request - The new address is invalid"
        }

    response = table.get_item(Key={"ID": shipment_id})
 
    if "Item" not in response:
        if isinstance(request, dict):
            return {
                "statusCode": 404,
                "body": "Not Found - The shipment ID is invalid"
            }
        else:
            raise HTTPException(status_code=404, detail="Shipment not found")
    
    table.update_item(
        Key={"ID": shipment_id},
        UpdateExpression="set ShipmentAddress = :new_address",
        ExpressionAttributeValues={":new_address": new_address},
    )
    
    if isinstance(request, dict):
        return {
            "statusCode": 200,
            "message": "Shipment address updated successfully"
        }
    else:
        return {"message": "Shipment address updated", "shipment_id": shipment_id}