from pydanticModels import models2,  shipmentModel
from DespatchAdviceFactory import DespatchAdvice
from dict2xml import dict2xml
from toXmlFormat import replace_specialchars
import json

import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DespatchAdviceTable') # table name might change

def lambda_handler(event, context):
        order_document = event.get("Order", {})
        shipment_details = event.get("cac:Shipment", {})

        # Convert JSON to Order and CacShipment objects
        order = models2.Order(order_document)
        shipment = shipmentModel.CacShipment(shipment_details)

        # Generate Despatch Advice
        factory = DespatchAdvice()
        despatch_advice = factory.create_despatch_advice(order, shipment)
        despatch_xml = factory.pydantic_to_xml(despatch_advice)

        item_json = despatch_advice.cac_despatchLine.cac_Item.model_dump_json()
        item_dict = json.loads(item_json)
        item_transformed = replace_specialchars(item_dict)
        item_xml = dict2xml(item_transformed, wrap="Item", newlines=True)


        despatch_item = {
            'ID': despatch_advice.cbc_ID, 
            'IssueDate': despatch_advice.cbc_IssueDate,
            'CountrySubentity': despatch_advice.cac_Shipment.cac_Delivery.cac_DeliveryAddress.cac_Country.cbc_IdentificationCode,
            'Items': item_xml,
            'DespatchContent': despatch_xml
        }

        #need to store the despatch advice in the database
        #use model_dump_json to convert from the pydantic format back to json
        table.put_item(Item=despatch_item)

        return {
            "statusCode": 200,
            "body": despatch_xml
        }