
from pydanticModels import models2,  shipmentModel
from DespatchAdviceFactory import DespatchAdvice
from toXmlFormat import replace_specialchars
import uuid
from datetime import datetime
from dict2xml import dict2xml
import json

import boto3

DYNAMO_TABLE_NAME = "DespatchAdviceTable"
dynamodb = boto3.client('dynamodb')
table = dynamodb.Table('DespatchAdvice') # table name might change

def lambda_handler(event, context):
        body = json.loads(event["body"])
        order_document = body.get("order", {})
        shipment_details = body.get("shipment", {})

        # Convert JSON to Order and CacShipment objects
        order = models2.Order(**order_document)
        shipment = shipmentModel.CacShipment(**shipment_details)


        # Generate Despatch Advice
        factory = DespatchAdvice()
        despatch_advice = factory.create_despatch_advice(order, shipment)
        despatch_json_str = despatch_advice.model_dump_json()
        despatch_dict = json.loads(despatch_json_str)
        transformed_dict = replace_specialchars(despatch_dict)

        despatch_item = {
            'ID': despatch_advice.cbc_ID, 
            'IssueDate': despatch_advice.cbc_IssueDate,
            'CountrySubentity': despatch_advice.cac_Shipment.cac_Delivery.cac_DeliveryAddress.cac_Country,
            'DespatchContent': despatch_json_str
        }
        
        #need to store the despatch advice in the database
        #use model_dump_json to convert from the pydantic format back to json
        table.put_item(Item=despatch_item)

        return {
            "statusCode": 200,
            "body": dict2xml(transformed_dict, wrap="Despatch", newlines=True)
        }
