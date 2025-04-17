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
    contact = event.get('body', {})

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
    despatch_dict["cac_DeliveryCustomerParty"]["cac_Party"]["cac_Contact"]["cbc_Name"] = contact.get("Name")
    despatch_dict["cac_DeliveryCustomerParty"]["cac_Party"]["cac_Contact"]["cbc_Telephone"] = contact.get("Telephone")
    despatch_dict["cac_DeliveryCustomerParty"]["cac_Party"]["cac_Contact"]["cbc_Telefax"] = contact.get("Telefax")
    despatch_dict["cac_DeliveryCustomerParty"]["cac_Party"]["cac_Contact"]["cbc_ElectronicMail"] = contact.get("ElectronicMail")
   
    # create a pydantic model of the updated advice
    advice = updateModel.DespatchAdvice(**despatch_dict)

    customer_json = advice.cac_DeliveryCustomerParty.cac_Party.cac_Contact.model_dump_json()
    customer_dict = json.loads(customer_json)
    customer_transformed = replace_specialchars(customer_dict)
    customer_xml = dict2xml(customer_transformed, wrap="CustomerContact", newlines=True)
  
    # make it in xml format
    advice_json = advice.model_dump_json()
    advice_dict = json.loads(advice_json)
    advice_transformed = replace_specialchars(advice_dict)
    advice_xml = dict2xml(advice_transformed, wrap="Advice", newlines=True)

    # store the updated dict and xml in the database
    response = table.update_item(
        Key={'ID': despatch_id},
        UpdateExpression="SET DespatchContent = :dc, DespatchAdviceXML = :da, CustomerContact = :cc",
        ExpressionAttributeValues={':dc': advice_dict, ':da': advice_xml, ':cc': customer_xml },
        ReturnValues="UPDATED_NEW"
    )
    return {
        "statusCode": 200,
        "despatchid": despatch_id,
        "Despatch Advice XML": advice_xml
    }