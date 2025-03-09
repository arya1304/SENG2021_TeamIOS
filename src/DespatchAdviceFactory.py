
from typing import Type 
from schemas import OrderAdvice, Shipment
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET

class DespatchAdviceFactory :
    #create despatch advice
    @abstractmethod
    def create_despatch_advice(orderAdivce: OrderAdvice, shipment: Shipment):
        #will return a peydantic model of the despatch advice
        pass

#create each component of the despatch advice

#create order reference
    def create_order_reference(orderAdvice: OrderAdvice):
        pass

#create despatch supplier party
    #from the order advice use SellerSupplierParty
    def create_despatch_supplier_party(orderAdvice: OrderAdvice):
        pass

#create delivery customer party
    #from the order use Buyer customer Party
    def create_delivery_customer_party(orderAdvice: OrderAdvice):
        pass

#create shipment
    #extract from the shipment json
    def create_shipment(shipment: Shipment):
        pass

#create despatch line
    #map items, quantities and price details from the order advice
    def despatch_line(orderAdvice: OrderAdvice):
        pass

#convert it into xml format

#https://docs.oasis-open.org/ubl/os-UBL-2.4/xml/UBL-DespatchAdvice-2.0-Example.xml 


# the defs will return the despatch advice as a pydantic model and then we use ET to convert it into a xml
# first we convert the xml into a dict