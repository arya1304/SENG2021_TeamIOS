from __future__ import annotations

from pydantic import BaseModel, Field

class CacAddressLine(BaseModel):
    cbc_Line: str = Field(..., alias='cbc:Line')

class CacConsignment(BaseModel):
    cbc_ID: str = Field(..., alias='cbc:ID')

class CacCountry(BaseModel):
    cbc_IdentificationCode: str = Field(..., alias='cbc:IdentificationCode')

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

class CacShipment(BaseModel):
    cbc_ID: str = Field(..., alias='cbc:ID')
    cac_Consignment: CacConsignment = Field(..., alias='cac:Consignment')
    cac_Delivery: CacDelivery = Field(..., alias='cac:Delivery')
