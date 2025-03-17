from pydanticModels import models2,  shipmentModel
from pydantic import ValidationError
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
        try:
            order = models2.Order(**order_document)
            shipment = shipmentModel.CacShipment(**shipment_details)
        except ValidationError as e:
              return {
                    "statusCode": 400,
                    "message": "Bad Request: Inputs are not in the correct format"
              }

        # Generate Despatch Advice
        factory = DespatchAdvice()
        despatch_advice = factory.create_despatch_advice(order, shipment)
        despatch_xml = factory.pydantic_to_xml(despatch_advice)

        item_json = despatch_advice.cac_DespatchLine.cac_Item.model_dump_json()
        item_dict = json.loads(item_json)
        item_transformed = replace_specialchars(item_dict)
        item_xml = dict2xml(item_transformed, wrap="Item", newlines=True)

        requested_delivery_json = despatch_advice.cac_Shipment.cac_Delivery.cac_RequestedDeliveryPeriod.model_dump_json()
        requested_delivery_dict = json.loads(requested_delivery_json)
        requested_delivery_transformed = replace_specialchars(requested_delivery_dict)
        requested_delivery_xml = dict2xml(requested_delivery_transformed, wrap="RequestedDeliveryPeriod", newlines=True)

        shipment_details_json = despatch_advice.cac_Shipment.model_dump_json()
        shipment_details_dict = json.loads(shipment_details_json)
        shipment_details_transformed = replace_specialchars(shipment_details_dict)
        shipment_details_xml = dict2xml(shipment_details_transformed, wrap="ShipmentDetails", newlines=True)

        order_reference_json = despatch_advice.cac_OrderReference.model_dump_json()
        order_reference_dict = json.loads(order_reference_json)
        order_reference_transformed = replace_specialchars(order_reference_dict)
        order_reference_xml = dict2xml(order_reference_transformed, wrap="OrderReference", newlines=True)


        despatch_item = {
            'ID': despatch_advice.cbc_ID, 
            'IssueDate': despatch_advice.cbc_IssueDate,
            'ShipmentCountry': despatch_advice.cac_Shipment.cac_Delivery.cac_DeliveryAddress.cac_Country.cbc_IdentificationCode,
            'Items': item_xml,
            'DespatchContent': despatch_xml,
            'RequestedDeliveryPeriod': requested_delivery_xml,
            'ShipmentDetails': shipment_details_xml,
            'OrderReference': order_reference_xml
        }

        #need to store the despatch advice in the database
        #use model_dump_json to convert from the pydantic format back to json
        table.put_item(Item=despatch_item)

        return {
            "statusCode": 200,
            "DespatchAdvice": despatch_xml
        }