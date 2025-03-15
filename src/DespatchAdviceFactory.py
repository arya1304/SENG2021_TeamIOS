
from typing import Type 
from pydanticModels import models2, models, shipmentModel
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
import uuid
from datetime import datetime
import json
from rich import print

import boto3

#DYNAMO_TABLE_NAME = "DespatchAdviceTable"
#dynamodb = boto3.client('dynamodb')
#table = dynamodb.Table('DespatchAdvice') # table name might change


class DespatchAdvice :
    def __init__(self):
        pass
    #create order reference
    def create_order_reference(self, orderAdvice: models2.Order) -> models.CacOrderReference:
        lineItem_dict = orderAdvice.cac_OrderLine.cac_LineItem
        order_ref = models.CacOrderReference(
            cbc_ID = orderAdvice.cbc_ID,
            cbc_SalesOrderID = lineItem_dict.cbc_SalesOrderID,
            cbc_UUID = orderAdvice.cbc_UUID,
            cbc_IssueDate = orderAdvice.cbc_IssueDate,
        )
        return  order_ref

    def create_despatch_supplier_party(self, orderAdvice: models2.Order) -> models.CacDespatchSupplierParty:

        originator_party = orderAdvice.cac_OriginatorCustomerParty

        party_name = models.CacPartyName(cbc_Name=originator_party.cac_Party.cac_PartyName.cbc_Name)

        postal_address = models.CacPostalAddress(
            cbc_StreetName=originator_party.cac_Party.cac_PostalAddress.cbc_StreetName,
            cbc_BuildingName=originator_party.cac_Party.cac_PostalAddress.cbc_BuildingName,
            cbc_BuildingNumber=originator_party.cac_Party.cac_PostalAddress.cbc_BuildingNumber,
            cbc_CityName=originator_party.cac_Party.cac_PostalAddress.cbc_CityName,
            cbc_PostalZone=originator_party.cac_Party.cac_PostalAddress.cbc_PostalZone,
            cbc_CountrySubentity=originator_party.cac_Party.cac_PostalAddress.cbc_CountrySubentity,
            cac_AddressLine=models.CacAddressLine(cbc_Line=originator_party.cac_Party.cac_PostalAddress.cac_AddressLine.cbc_Line),
            cac_Country=models.CacCountry(cbc_IdentificationCode=originator_party.cac_Party.cac_PostalAddress.cac_Country.cbc_IdentificationCode)
        )

        party_tax_scheme = models.CacPartyTaxScheme(
            cbc_RegistrationName=originator_party.cac_Party.cac_PartyTaxScheme.cbc_RegistrationName,
            cbc_CompanyID=originator_party.cac_Party.cac_PartyTaxScheme.cbc_CompanyID,
            cbc_ExemptionReason=originator_party.cac_Party.cac_PartyTaxScheme.cbc_ExemptionReason,
            cac_TaxScheme=models.CacTaxScheme(
                cbc_ID=originator_party.cac_Party.cac_PartyTaxScheme.cac_TaxScheme.cbc_ID,
                cbc_TaxTypeCode=originator_party.cac_Party.cac_PartyTaxScheme.cac_TaxScheme.cbc_TaxTypeCode
            )
        )

        contact = models.CacContact(
            cbc_Name=originator_party.cac_Party.cac_Contact.cbc_Name,
            cbc_Telephone=originator_party.cac_Party.cac_Contact.cbc_Telephone,
            cbc_Telefax=originator_party.cac_Party.cac_Contact.cbc_Telefax,
            cbc_ElectronicMail=originator_party.cac_Party.cac_Contact.cbc_ElectronicMail
        )

        party = models.CacParty(
            cac_PartyName=party_name,
            cac_PostalAddress=postal_address,
            cac_PartyTaxScheme=party_tax_scheme,
            cac_Contact=contact
        )

        despatch_supplier_party = models.CacDespatchSupplierParty(
            cbc_CustomerAssignedAccountID=orderAdvice.cac_SellerSupplierParty.cbc_CustomerAssignedAccountID,
            cac_Party=party
        )

        return despatch_supplier_party

    #create delivery customer party
    #from the order use Buyer customer Party
    def create_delivery_customer_party(self, orderAdvice: models2.Order) -> models.CacDeliveryCustomerParty:
        buyer_party = orderAdvice.cac_BuyerCustomerParty
        party_details = buyer_party.cac_Party

        postal = party_details.cac_PostalAddress

        address_line = models.CacAddressLine(
            cbc_Line=postal.cac_AddressLine.cbc_Line
        )
    
        country = models.CacCountry(
            cbc_IdentificationCode=postal.cac_Country.cbc_IdentificationCode
        )

        customer_postal = models.CacPostalAddress1(
            cbc_StreetName=postal.cbc_StreetName,
            cbc_BuildingName=postal.cbc_BuildingName,
            cbc_BuildingNumber=postal.cbc_BuildingNumber,
            cbc_CityName=postal.cbc_CityName,
            cbc_PostalZone= postal.cbc_PostalZone,
            cbc_CountrySubentity=postal.cbc_CountrySubentity,
            cac_AddressLine= address_line,
            cac_Country=country
        )

        original_contact = party_details.cac_Contact
        contact = models.CacContact(
            cbc_Name=original_contact.cbc_Name,
            cbc_Telephone=original_contact.cbc_Telephone,
            cbc_Telefax=original_contact.cbc_Telefax,
            cbc_ElectronicMail=original_contact.cbc_ElectronicMail
        )

        tax_scheme = models.CacPartyTaxScheme1(
            cbc_RegistrationName="Hello",
            cbc_CompanyID="299292",
            cbc_ExemptionReason="N/A",
            cac_TaxScheme=models.CacTaxScheme(
                cbc_ID="213",
                cbc_TaxTypeCode="3131441"
            )
        )

        party_name = models.CacPartyName(
            cbc_Name=party_details.cac_PartyName.cbc_Name
        )

        party = models.CacParty1(
            cac_PartyName=party_name,
            cac_PostalAddress=customer_postal,
            cac_Contact=contact,
            cac_PartyTaxScheme = tax_scheme
        )

        customer_details = models.CacDeliveryCustomerParty(
            cbc_CustomerAssignedAccountID=buyer_party.cbc_CustomerAssignedAccountID,
            cbc_SupplierAssignedAccountID=buyer_party.cbc_SupplierAssignedAccountID,
            cac_Party=party
        )
        return customer_details

    #create shipment
    #extract from the shipment json
    #what happens when we get an empty field?
    #create an optional field for requested delivery period 
    #determine what fields that can be
    def create_shipment(self, shipment: models.CacShipment) -> models.CacShipment:
        
        consignment = shipment.cac_Consignment
        delivery = shipment.cac_Delivery.cac_DeliveryAddress
        requested = shipment.cac_Delivery.cac_RequestedDeliveryPeriod
        consignment_details = models.CacConsignment(
            cbc_ID=consignment.cbc_ID
        )

        address_line = models.CacAddressLine(
           cbc_Line=delivery.cac_AddressLine.cbc_Line
        )
    
        country = models.CacCountry(
           cbc_IdentificationCode=delivery.cac_Country.cbc_IdentificationCode
        )

        deliveryAddress = models.CacDeliveryAddress(
            cbc_StreetName=delivery.cbc_StreetName,
            cbc_BuildingName=delivery.cbc_BuildingName,
            cbc_BuildingNumber=delivery.cbc_BuildingNumber,
            cbc_CityName=delivery.cbc_CityName,
            cbc_PostalZone= delivery.cbc_PostalZone,
            cbc_CountrySubentity=delivery.cbc_CountrySubentity,
            cac_AddressLine= address_line,
            cac_Country=country
        )

        requested_period = models.CacRequestedDeliveryPeriod(
            cbc_StartDate=requested.cbc_StartDate,
            cbc_StartTime=requested.cbc_StartTime,
            cbc_EndDate=requested.cbc_EndDate,
            cbc_EndTime=requested.cbc_EndTime
        )

        delivery_details = models.CacDelivery(
            cac_DeliveryAddress=deliveryAddress,
            cac_RequestedDeliveryPeriod=requested_period
        )

        despatch_delivery = models.CacShipment(
            cbc_ID = shipment.cbc_ID,
            cac_Consignment =  consignment_details,
            cac_Delivery = delivery_details
        )
        return despatch_delivery


    #create despatch line
    #each item has its own despatch line 
    def create_despatch_line(self, orderAdvice: models2.Order) -> models.CacDespatchLine:
        order = orderAdvice.cac_OrderLine
        line_item_dict = orderAdvice.cac_OrderLine.cac_LineItem
        original_item = line_item_dict.cac_Item
        order_ref = self.create_order_reference(orderAdvice)

        quantity = line_item_dict.cbc_Quantity
        delivered_quantity = models.CbcDeliveredQuantity(
            field_unitCode=quantity.field_unitCode,
            text=quantity.text
        )

        backorder_quantity = models.CbcBackorderQuantity(
            field_unitCode=quantity.field_unitCode,
            text="0"
        )

        item_identification = models.CacBuyersItemIdentification(
            cbc_ID=original_item.cac_BuyersItemIdentification.cbc_ID
        )

        sellers_identification = models.CacSellersItemIdentification(
            cbc_ID=original_item.cac_SellersItemIdentification.cbc_ID
        )

        #lot identification, randomise
        lot_identity = models.CacLotIdentification(
            cbc_ExpiryDate="000",
            cbc_LotNumberID="0000"
        )

        instance_item = models.CacItemInstance(
            cac_LotIdentification=lot_identity
        )

        item = models.CacItem(
            cbc_Description=original_item.cbc_Description,
            cbc_Name=original_item.cbc_Name,
            cac_BuyersItemIdentification=item_identification,
            cac_SellersItemIdentification=sellers_identification,
            cac_ItemInstance=instance_item
        )

        despatch_line = models.CacDespatchLine(
            cbc_ID = line_item_dict.cbc_ID,
            cbc_Note = order.cbc_Note,
            cbc_LineStatusCode = line_item_dict.cbc_LineStatusCode,
            cbc_DeliveredQuantity = delivered_quantity,
            cbc_BackorderQuantity = backorder_quantity,
            cbc_BackorderReason = '',
            cac_OrderLineReference = models.CacOrderLineReference(
                cbc_LineID = '',
                cbc_SalesOrderLineID = '',
                cac_OrderReference = order_ref
            ),
            cac_Item = item
        )
        return despatch_line

    #create despatch advice
    def create_despatch_advice(self, orderAdvice: models2.Order, shipment: shipmentModel.CacShipment) -> models.DespatchAdvice:
        #will return a peydantic model of the despatch advice
        order_ref = self.create_order_reference(orderAdvice), 
        supplier_party = self.create_despatch_supplier_party(orderAdvice),
        customer_party = self.create_delivery_customer_party(orderAdvice),
        shipment_details = self.create_shipment(shipment),
        despatch_line = self.create_despatch_line(orderAdvice)

        print("Hello create func")
        #print(order_ref)
        #print(supplier_party)
        #print(customer_party)
        #print(shipment_details)
        #print(despatch_line)
        order_ref_ = self.create_order_reference(orderAdvice)
        despatch_advice = models.DespatchAdvice(
            field_xmlns_cbc = orderAdvice.field_xmlns,
            field_xmlns_cac = orderAdvice.field_xmlns_cac,
            field_xmlns = orderAdvice.field_xmlns,
            cbc_UBLVersionID = orderAdvice.cbc_UBLVersionID,
            cbc_CustomizationID="000",
            cbc_ProfileID = orderAdvice.cbc_ProfileID,
            cbc_ID = '',
            cbc_CopyIndicator = 'false',
            cbc_UUID = str(uuid.uuid4()), #generating a uuid
            cbc_IssueDate = datetime.today().strftime('%Y-%m-%d'),
            cbc_DocumentStatusCode = 'NoStatus',
            cbc_DespatchAdviceTypeCode = 'delivery',
            cbc_Note = 'ajjffj',
            order_ref =  order_ref_, 
            cac_OrderReference = self.create_order_reference(orderAdvice),
            cac_DespatchSupplierParty = self.create_despatch_supplier_party(orderAdvice),
            cac_DeliveryCustomerParty = self.create_delivery_customer_party(orderAdvice),
            cac_Shipment = self.create_shipment(shipment),
            cac_DespatchLine = self.create_despatch_line(orderAdvice)
        )
        return despatch_advice

