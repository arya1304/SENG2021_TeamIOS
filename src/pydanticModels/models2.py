# generated by datamodel-codegen:
# pip3 install datamodel-code-generator
# took in order json and made a base pydantic model
#   filename:  order_advice.json
#   timestamp: 2025-03-10T05:21:36+00:00

from __future__ import annotations

from pydantic import BaseModel, Field


class CacPartyName(BaseModel):
    cbc_Name: str = Field(..., alias='cbc:Name')


class CacAddressLine(BaseModel):
    cbc_Line: str = Field(..., alias='cbc:Line')


class CacCountry(BaseModel):
    cbc_IdentificationCode: str = Field(..., alias='cbc:IdentificationCode')


class CacPostalAddress(BaseModel):
    cbc_StreetName: str = Field(..., alias='cbc:StreetName')
    cbc_BuildingName: str = Field(..., alias='cbc:BuildingName')
    cbc_BuildingNumber: str = Field(..., alias='cbc:BuildingNumber')
    cbc_CityName: str = Field(..., alias='cbc:CityName')
    cbc_PostalZone: str = Field(..., alias='cbc:PostalZone')
    cbc_CountrySubentity: str = Field(..., alias='cbc:CountrySubentity')
    cac_AddressLine: CacAddressLine = Field(..., alias='cac:AddressLine')
    cac_Country: CacCountry = Field(..., alias='cac:Country')


class CacContact(BaseModel):
    cbc_Name: str = Field(..., alias='cbc:Name')
    cbc_Telephone: str = Field(..., alias='cbc:Telephone')
    cbc_Telefax: str = Field(..., alias='cbc:Telefax')
    cbc_ElectronicMail: str = Field(..., alias='cbc:ElectronicMail')


class CacParty(BaseModel):
    cac_PartyName: CacPartyName = Field(..., alias='cac:PartyName')
    cac_PostalAddress: CacPostalAddress = Field(..., alias='cac:PostalAddress')
    cac_Contact: CacContact = Field(..., alias='cac:Contact')


class CacBuyerCustomerParty(BaseModel):
    cbc_CustomerAssignedAccountID: str = Field(
        ..., alias='cbc:CustomerAssignedAccountID'
    )
    cbc_SupplierAssignedAccountID: str = Field(
        ..., alias='cbc:SupplierAssignedAccountID'
    )
    cac_Party: CacParty = Field(..., alias='cac:Party')


class CacPostalAddress1(BaseModel):
    cbc_StreetName: str = Field(..., alias='cbc:StreetName')
    cbc_BuildingName: str = Field(..., alias='cbc:BuildingName')
    cbc_BuildingNumber: str = Field(..., alias='cbc:BuildingNumber')
    cbc_CityName: str = Field(..., alias='cbc:CityName')
    cbc_PostalZone: str = Field(..., alias='cbc:PostalZone')
    cbc_CountrySubentity: str = Field(..., alias='cbc:CountrySubentity')
    cbc_CountrySubentityCode: str = Field(..., alias='cbc:CountrySubentityCode')
    cac_Country: CacCountry = Field(..., alias='cac:Country')


class CacParty1(BaseModel):
    cac_PartyName: CacPartyName = Field(..., alias='cac:PartyName')
    cac_PostalAddress: CacPostalAddress1 = Field(..., alias='cac:PostalAddress')
    cac_Contact: CacContact = Field(..., alias='cac:Contact')


class CacSellerSupplierParty(BaseModel):
    cbc_CustomerAssignedAccountID: str = Field(
        ..., alias='cbc:CustomerAssignedAccountID'
    )
    cac_Party: CacParty1 = Field(..., alias='cac:Party')


class CacPostalAddress2(BaseModel):
    cbc_StreetName: str = Field(..., alias='cbc:StreetName')
    cbc_BuildingName: str = Field(..., alias='cbc:BuildingName')
    cbc_BuildingNumber: str = Field(..., alias='cbc:BuildingNumber')
    cbc_CityName: str = Field(..., alias='cbc:CityName')
    cbc_PostalZone: str = Field(..., alias='cbc:PostalZone')
    cbc_CountrySubentity: str = Field(..., alias='cbc:CountrySubentity')
    cac_AddressLine: CacAddressLine = Field(..., alias='cac:AddressLine')
    cac_Country: CacCountry = Field(..., alias='cac:Country')


class CacTaxScheme(BaseModel):
    cbc_ID: str = Field(..., alias='cbc:ID')
    cbc_TaxTypeCode: str = Field(..., alias='cbc:TaxTypeCode')


class CacPartyTaxScheme(BaseModel):
    cbc_RegistrationName: str = Field(..., alias='cbc:RegistrationName')
    cbc_CompanyID: str = Field(..., alias='cbc:CompanyID')
    cbc_ExemptionReason: str = Field(..., alias='cbc:ExemptionReason')
    cac_TaxScheme: CacTaxScheme = Field(..., alias='cac:TaxScheme')


class CacParty2(BaseModel):
    cac_PartyName: CacPartyName = Field(..., alias='cac:PartyName')
    cac_PostalAddress: CacPostalAddress2 = Field(..., alias='cac:PostalAddress')
    cac_PartyTaxScheme: CacPartyTaxScheme = Field(..., alias='cac:PartyTaxScheme')
    cac_Contact: CacContact = Field(..., alias='cac:Contact')


class CacOriginatorCustomerParty(BaseModel):
    cac_Party: CacParty2 = Field(..., alias='cac:Party')


class CacDeliveryAddress(BaseModel):
    cbc_StreetName: str = Field(..., alias='cbc:StreetName')
    cbc_BuildingName: str = Field(..., alias='cbc:BuildingName')
    cbc_BuildingNumber: str = Field(..., alias='cbc:BuildingNumber')
    cbc_CityName: str = Field(..., alias='cbc:CityName')
    cbc_PostalZone: str = Field(..., alias='cbc:PostalZone')
    cbc_CountrySubentity: str = Field(..., alias='cbc:CountrySubentity')
    cac_AddressLine: CacAddressLine = Field(..., alias='cac:AddressLine')
    cac_Country: CacCountry = Field(..., alias='cac:Country')


class CacRequestedDeliveryPeriod(BaseModel):
    cbc_StartDate: str = Field(..., alias='cbc:StartDate')
    cbc_StartTime: str = Field(..., alias='cbc:StartTime')
    cbc_EndDate: str = Field(..., alias='cbc:EndDate')
    cbc_EndTime: str = Field(..., alias='cbc:EndTime')


class CacDelivery(BaseModel):
    cac_DeliveryAddress: CacDeliveryAddress = Field(..., alias='cac:DeliveryAddress')
    cac_RequestedDeliveryPeriod: CacRequestedDeliveryPeriod = Field(
        ..., alias='cac:RequestedDeliveryPeriod'
    )


class CacDeliveryLocation(BaseModel):
    cbc_ID: str = Field(..., alias='cbc:ID')
    cbc_Description: str = Field(..., alias='cbc:Description')


class CacDeliveryTerms(BaseModel):
    cbc_ID: str = Field(..., alias='cbc:ID')
    cac_DeliveryLocation: CacDeliveryLocation = Field(..., alias='cac:DeliveryLocation')


class CacTransactionConditions(BaseModel):
    cbc_Description: str = Field(..., alias='cbc:Description')


class CbcLineExtensionAmount(BaseModel):
    field_currencyID: str = Field(..., alias='@currencyID')
    text: str = Field(..., alias='#text')


class CbcPayableAmount(BaseModel):
    field_currencyID: str = Field(..., alias='@currencyID')
    text: str = Field(..., alias='#text')


class CacAnticipatedMonetaryTotal(BaseModel):
    cbc_LineExtensionAmount: CbcLineExtensionAmount = Field(
        ..., alias='cbc:LineExtensionAmount'
    )
    cbc_PayableAmount: CbcPayableAmount = Field(..., alias='cbc:PayableAmount')


class CbcQuantity(BaseModel):
    field_unitCode: str = Field(..., alias='@unitCode')
    text: str = Field(..., alias='#text')


class CbcPriceAmount(BaseModel):
    field_currencyID: str = Field(..., alias='@currencyID')
    text: str = Field(..., alias='#text')


class CbcBaseQuantity(BaseModel):
    field_unitCode: str = Field(..., alias='@unitCode')
    text: str = Field(..., alias='#text')


class CacPrice(BaseModel):
    cbc_PriceAmount: CbcPriceAmount = Field(..., alias='cbc:PriceAmount')
    cbc_BaseQuantity: CbcBaseQuantity = Field(..., alias='cbc:BaseQuantity')


class CacBuyersItemIdentification(BaseModel):
    cbc_ID: str = Field(..., alias='cbc:ID')


class CacSellersItemIdentification(BaseModel):
    cbc_ID: str = Field(..., alias='cbc:ID')


class CacItem(BaseModel):
    cbc_Description: str = Field(..., alias='cbc:Description')
    cbc_Name: str = Field(..., alias='cbc:Name')
    cac_BuyersItemIdentification: CacBuyersItemIdentification = Field(
        ..., alias='cac:BuyersItemIdentification'
    )
    cac_SellersItemIdentification: CacSellersItemIdentification = Field(
        ..., alias='cac:SellersItemIdentification'
    )


class CacLineItem(BaseModel):
    cbc_ID: str = Field(..., alias='cbc:ID')
    cbc_SalesOrderID: str = Field(..., alias='cbc:SalesOrderID')
    cbc_LineStatusCode: str = Field(..., alias='cbc:LineStatusCode')
    cbc_Quantity: CbcQuantity = Field(..., alias='cbc:Quantity')
    cbc_LineExtensionAmount: CbcLineExtensionAmount = Field(
        ..., alias='cbc:LineExtensionAmount'
    )
    cac_Price: CacPrice = Field(..., alias='cac:Price')
    cac_Item: CacItem = Field(..., alias='cac:Item')


class CacOrderLine(BaseModel):
    cbc_Note: str = Field(..., alias='cbc:Note')
    cac_LineItem: CacLineItem = Field(..., alias='cac:LineItem')


class Order(BaseModel):
    field_xmlns: str = Field(..., alias='@xmlns')
    field_xmlns_cac: str = Field(..., alias='@xmlns:cac')
    field_xmlns_cbc: str = Field(..., alias='@xmlns:cbc')
    cbc_UBLVersionID: str = Field(..., alias='cbc:UBLVersionID')
    cbc_CustomizationID: str = Field(..., alias='cbc:CustomizationID')
    cbc_ProfileID: str = Field(..., alias='cbc:ProfileID')
    cbc_ID: str = Field(..., alias='cbc:ID')
    cbc_CopyIndicator: str = Field(..., alias='cbc:CopyIndicator')
    cbc_UUID: str = Field(..., alias='cbc:UUID')
    cbc_IssueDate: str = Field(..., alias='cbc:IssueDate')
    cbc_Note: str = Field(..., alias='cbc:Note')
    cac_BuyerCustomerParty: CacBuyerCustomerParty = Field(
        ..., alias='cac:BuyerCustomerParty'
    )
    cac_SellerSupplierParty: CacSellerSupplierParty = Field(
        ..., alias='cac:SellerSupplierParty'
    )
    cac_OriginatorCustomerParty: CacOriginatorCustomerParty = Field(
        ..., alias='cac:OriginatorCustomerParty'
    )
    cac_Delivery: CacDelivery = Field(..., alias='cac:Delivery')
    cac_DeliveryTerms: CacDeliveryTerms = Field(..., alias='cac:DeliveryTerms')
    cac_TransactionConditions: CacTransactionConditions = Field(
        ..., alias='cac:TransactionConditions'
    )
    cac_AnticipatedMonetaryTotal: CacAnticipatedMonetaryTotal = Field(
        ..., alias='cac:AnticipatedMonetaryTotal'
    )
    cac_OrderLine: CacOrderLine = Field(..., alias='cac:OrderLine')


class Model(BaseModel):
    Order: Order