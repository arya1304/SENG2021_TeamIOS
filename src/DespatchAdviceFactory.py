
from typing import Type 
from pydanticModels import models2, models
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
import uuid

class DespatchAdviceFactory :
    #create each component of the despatch advice

    #create order reference
    def create_order_reference(self, orderAdvice: models2.Order) -> models.CacOrderReference:
        order_dict = orderAdvice.model_dump()
        lineItem_dict = orderAdvice.cac_OrderLine.cac_LineItem.model_dump()
        order_ref = models.CacOrderReference(
            cbc_ID = order_dict['cbc_ID'],
            cbc_SalesOrderID = lineItem_dict['cbc_SalesOrderID'],
            cbc_UUID = order_dict['cbc_UUID'],
            cbc_IssueDate = order_dict['cbc_IssueDate'],
        )
        return  order_ref

    #create despatch supplier party
    #from the order advice use SellerSupplierParty
    def create_despatch_supplier_party(self, orderAdvice: models2.Order) -> models.CacDespatchSupplierParty:
        seller_party = orderAdvice.cac_SellerSupplierParty
        party_name = models.CacPartyName(cbc_Name=seller_party.cac_Party.cac_PartyName.cbc_Name)

        postal_address = models.CacPostalAddress(
            cbc_StreetName=seller_party.cac_Party.cac_PostalAddress.cbc_StreetName,
            cbc_BuildingName=seller_party.cac_Party.cac_PostalAddress.cbc_BuildingName,
            cbc_BuildingNumber=seller_party.cac_Party.cac_PostalAddress.cbc_BuildingNumber,
            cbc_CityName=seller_party.cac_Party.cac_PostalAddress.cbc_CityName,
            cbc_PostalZone=seller_party.cac_Party.cac_PostalAddress.cbc_PostalZone,
            cbc_CountrySubentity=seller_party.cac_Party.cac_PostalAddress.cbc_CountrySubentity,
            cac_AddressLine=models.CacAddressLine(cbc_Line=seller_party.cac_Party.cac_PostalAddress.cac_AddressLine.cbc_Line),
            cac_Country=models.CacCountry(cbc_IdentificationCode=seller_party.cac_Party.cac_PostalAddress.cac_Country.cbc_IdentificationCode)
        )

        party_tax_scheme = models.CacPartyTaxScheme(
            cbc_RegistrationName=seller_party.cac_Party.cac_PartyTaxScheme.cbc_RegistrationName,
            cbc_CompanyID=seller_party.cac_Party.cac_PartyTaxScheme.cbc_CompanyID,
            cbc_ExemptionReason=seller_party.cac_Party.cac_PartyTaxScheme.cbc_ExemptionReason,
            cac_TaxScheme=models.CacTaxScheme(
                cbc_ID=seller_party.cac_Party.cac_PartyTaxScheme.cac_TaxScheme.cbc_ID,
                cbc_TaxTypeCode=seller_party.cac_Party.cac_PartyTaxScheme.cac_TaxScheme.cbc_TaxTypeCode
            )
        )

        contact = models.CacContact (
            cbc_Name=seller_party.cac_Party.cac_Contact.cbc_Name,
            cbc_Telephone=seller_party.cac_Party.cac_Contact.cbc_Telephone,
            cbc_Telefax=seller_party.cac_Party.cac_Contact.cbc_Telefax,
            cbc_ElectronicMail=seller_party.cac_Party.cac_Contact.cbc_ElectronicMail

        )

        party = models.CacParty(
            cac_PartyName=party_name,
            cac_PostalAddress=postal_address,
            cac_PartyTaxScheme=party_tax_scheme,
            cac_Contact=contact
        )

        despatch_supplier_party = models.CacDespatchSupplierParty(
            cbc_CustomerAssignedAccountID=seller_party.cbc_CustomerAssignedAccountID,
            cac_Party=party
        )

        return despatch_supplier_party

    #create delivery customer party
    #from the order use Buyer customer Party
    def create_delivery_customer_party(orderAdvice: models2.Order) -> models.CacDeliveryCustomerParty:
        buyer_party = orderAdvice.cac_BuyerCustomerParty
        party_details = buyer_party.cac_Party

        deliver_customer_party = models.CacDeliveryCustomerParty(
            cbc_CustomerAssignedAccountID=buyer_party.cbc_CustomerAssignedAccountID,
            cbc_SupplierAssignedAccountID=buyer_party.cbc_SupplierAssignedAccountID,
            cac_Party=models.CacParty1(
                cac_PartyName=party_details.cac_PartyName,
                cac_PostalAddress=party_details.cac_PostalAddress,
                cac_PartyTaxScheme=party_details.cac_PastryTaxScheme,
                cac_Contact=party_details.cac_Contact,
            )
        )

        return deliver_customer_party

    #create shipment
    #extract from the shipment json
    def create_shipment(shipment: models2.Order):
        pass

    #create despatch line
    #map items, quantities and price details from the order advice
    def despatch_line(orderAdvice: models2.Order):
        pass

    #create despatch advice
    def create_despatch_advice(self, orderAdivce: models2.Order, shipment: models.CacShipment) -> models.DespatchAdvice :
        #will return a peydantic model of the despatch advice
        order_ref = self.create_order_reference(orderAdivce) 
        return 
    #convert it into xml format

    #https://docs.oasis-open.org/ubl/os-UBL-2.4/xml/UBL-DespatchAdvice-2.0-Example.xml 


    # the defs will return the despatch advice as a pydantic model and then we use ET to convert it into a xml
    # first we convert the xml into a dict