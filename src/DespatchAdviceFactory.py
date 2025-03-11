
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
    def create_despatch_supplier_party(orderAdvice: models2.Order):
        pass

    #create delivery customer party
    #from the order use Buyer customer Party
    def create_delivery_customer_party(orderAdvice: models2.Order):
        pass

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