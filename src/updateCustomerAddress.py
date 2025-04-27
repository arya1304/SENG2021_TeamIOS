import json
import boto3
from pydanticModels import updateModel
from dict2xml import dict2xml
from toXmlFormat import replace_specialchars

def lambda_handler(event, context):
    
    # Retrieve the database 
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DespatchAdviceTable')

    # Check if event contains the despatch ID, if not return response: 400
    if 'despatchId' not in event.get('pathParameters', {}):
        return {
            "statusCode": 400,
            "body": "Bad Request - The despatch ID is not provided"
        }

    despatch_id = event['pathParameters']['despatchId']
    address = event.get('body', {})

    response = table.get_item(Key={'ID': despatch_id})
    # if item doesn't exist in the response, return response: 404
    if 'Item' not in response:
        return {
            "statusCode": 404,
            "body": despatch_id
        }

    # Get the DespatchXML attribute string from the Item associated with ID
    despatch_advice = response['Item']
    despatch_dict = despatch_advice.get('DespatchContent')

    # update the customer postal address within the dictionary
    despatch_dict["cac_DeliveryCustomerParty"]["cac_Party"]["cac_PostalAddress"]["cbc_StreetName"] = address.get("StreetName")
    despatch_dict["cac_DeliveryCustomerParty"]["cac_Party"]["cac_PostalAddress"]["cbc_BuildingName"] = address.get("BuildingName")
    despatch_dict["cac_DeliveryCustomerParty"]["cac_Party"]["cac_PostalAddress"]["cbc_BuildingNumber"] = address.get("BuildingNumber")
    despatch_dict["cac_DeliveryCustomerParty"]["cac_Party"]["cac_PostalAddress"]["cbc_CityName"] = address.get("CityName")
    despatch_dict["cac_DeliveryCustomerParty"]["cac_Party"]["cac_PostalAddress"]["cbc_PostalZone"] = address.get("PostalZone")
    despatch_dict["cac_DeliveryCustomerParty"]["cac_Party"]["cac_PostalAddress"]["cbc_CountrySubentity"] = address.get("CountrySubentity")
    despatch_dict["cac_DeliveryCustomerParty"]["cac_Party"]["cac_PostalAddress"]["cac_AddressLine"]["cbc_Line"] = address.get("AddressLine")
    despatch_dict["cac_DeliveryCustomerParty"]["cac_Party"]["cac_PostalAddress"]["cac_Country"]["cbc_IdentificationCode"] = address.get("Country")
    
    # create a pydantic model of the updated advice
    advice = updateModel.DespatchAdvice(**despatch_dict)
  
    # make it in xml format
    advice_json = advice.model_dump_json()
    advice_dict = json.loads(advice_json)
    advice_transformed = replace_specialchars(advice_dict)
    advice_xml = dict2xml(advice_transformed, wrap="Advice", newlines=True)

    # store the updated dict and xml in the database
    response = table.update_item(
        Key={'ID': despatch_id},
        UpdateExpression="SET DespatchContent = :dc, DespatchAdviceXML = :da",
        ExpressionAttributeValues={':dc': advice_dict, ':da': advice_xml},
        ReturnValues="UPDATED_NEW"
    )
    return {
        "statusCode": 200,
        "despatchid": despatch_id,
        "Despatch Advice XML": advice_xml
    }