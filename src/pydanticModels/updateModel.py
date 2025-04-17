# generated by datamodel-codegen:
#   filename:  updateDespatchAdvice.json
#   timestamp: 2025-04-16T01:46:35+00:00

from __future__ import annotations

from pydantic import BaseModel


class CacOrderReference(BaseModel):
    cbc_ID: str
    cbc_SalesOrderID: str
    cbc_UUID: str
    cbc_IssueDate: str


class CacPartyName(BaseModel):
    cbc_Name: str


class CacAddressLine(BaseModel):
    cbc_Line: str


class CacCountry(BaseModel):
    cbc_IdentificationCode: str


class CacPostalAddress(BaseModel):
    cbc_StreetName: str
    cbc_BuildingName: str
    cbc_BuildingNumber: str
    cbc_CityName: str
    cbc_PostalZone: str
    cbc_CountrySubentity: str
    cac_AddressLine: CacAddressLine
    cac_Country: CacCountry


class CacTaxScheme(BaseModel):
    cbc_ID: str
    cbc_TaxTypeCode: str


class CacPartyTaxScheme(BaseModel):
    cbc_RegistrationName: str
    cbc_CompanyID: str
    cbc_ExemptionReason: str
    cac_TaxScheme: CacTaxScheme


class CacContact(BaseModel):
    cbc_Name: str
    cbc_Telephone: str
    cbc_Telefax: str
    cbc_ElectronicMail: str


class CacParty(BaseModel):
    cac_PartyName: CacPartyName
    cac_PostalAddress: CacPostalAddress
    cac_PartyTaxScheme: CacPartyTaxScheme
    cac_Contact: CacContact


class CacDespatchSupplierParty(BaseModel):
    cbc_CustomerAssignedAccountID: str
    cac_Party: CacParty


class CacPostalAddress1(BaseModel):
    cbc_StreetName: str
    cbc_BuildingName: str
    cbc_BuildingNumber: str
    cbc_CityName: str
    cbc_PostalZone: str
    cbc_CountrySubentity: str
    cac_AddressLine: CacAddressLine
    cac_Country: CacCountry


class CacPartyTaxScheme1(BaseModel):
    cbc_RegistrationName: str
    cbc_CompanyID: str
    cbc_ExemptionReason: str
    cac_TaxScheme: CacTaxScheme


class CacParty1(BaseModel):
    cac_PartyName: CacPartyName
    cac_PostalAddress: CacPostalAddress1
    cac_PartyTaxScheme: CacPartyTaxScheme1
    cac_Contact: CacContact


class CacDeliveryCustomerParty(BaseModel):
    cbc_CustomerAssignedAccountID: str
    cbc_SupplierAssignedAccountID: str
    cac_Party: CacParty1


class CacConsignment(BaseModel):
    cbc_ID: str


class CacDeliveryAddress(BaseModel):
    cbc_StreetName: str
    cbc_BuildingName: str
    cbc_BuildingNumber: str
    cbc_CityName: str
    cbc_PostalZone: str
    cbc_CountrySubentity: str
    cac_AddressLine: CacAddressLine
    cac_Country: CacCountry


class CacRequestedDeliveryPeriod(BaseModel):
    cbc_StartDate: str
    cbc_StartTime: str
    cbc_EndDate: str
    cbc_EndTime: str


class CacDelivery(BaseModel):
    cac_DeliveryAddress: CacDeliveryAddress
    cac_RequestedDeliveryPeriod: CacRequestedDeliveryPeriod


class CacShipment(BaseModel):
    cbc_ID: str
    cac_Consignment: CacConsignment
    cac_Delivery: CacDelivery


class CbcDeliveredQuantity(BaseModel):
    field_unitCode: str
    text: str


class CbcBackorderQuantity(BaseModel):
    field_unitCode: str
    text: str


class CacOrderLineReference(BaseModel):
    cbc_LineID: str
    cbc_SalesOrderLineID: str
    cac_OrderReference: CacOrderReference


class CacBuyersItemIdentification(BaseModel):
    cbc_ID: str


class CacSellersItemIdentification(BaseModel):
    cbc_ID: str


class CacLotIdentification(BaseModel):
    cbc_LotNumberID: str
    cbc_ExpiryDate: str


class CacItemInstance(BaseModel):
    cac_LotIdentification: CacLotIdentification


class CacItem(BaseModel):
    cbc_Description: str
    cbc_Name: str
    cac_BuyersItemIdentification: CacBuyersItemIdentification
    cac_SellersItemIdentification: CacSellersItemIdentification
    cac_ItemInstance: CacItemInstance


class CacDespatchLine(BaseModel):
    cbc_ID: str
    cbc_Note: str
    cbc_LineStatusCode: str
    cbc_DeliveredQuantity: CbcDeliveredQuantity
    cbc_BackorderQuantity: CbcBackorderQuantity
    cbc_BackorderReason: str
    cac_OrderLineReference: CacOrderLineReference
    cac_Item: CacItem


class DespatchAdvice(BaseModel):
    field_xmlns_cbc: str
    field_xmlns_cac: str
    field_xmlns: str
    cbc_UBLVersionID: str
    cbc_CustomizationID: str
    cbc_ProfileID: str
    cbc_ID: str
    cbc_CopyIndicator: str
    cbc_UUID: str
    cbc_IssueDate: str
    cbc_DocumentStatusCode: str
    cbc_DespatchAdviceTypeCode: str
    cbc_Note: str
    cac_OrderReference: CacOrderReference
    cac_DespatchSupplierParty: CacDespatchSupplierParty
    cac_DeliveryCustomerParty: CacDeliveryCustomerParty
    cac_Shipment: CacShipment
    cac_DespatchLine: CacDespatchLine


class Model(BaseModel):
    DespatchAdvice: DespatchAdvice
