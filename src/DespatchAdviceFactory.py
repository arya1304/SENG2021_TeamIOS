
from typing import Type 
from schemas import OrderAdvice, Shipment
from abc import ABC, abstractmethod

class DespatchAdviceFactory :
    #create despatch advice
    @abstractmethod
    def create_despatch_advice(orderAdivce: OrderAdvice, shipment: Shipment):
        pass

#create each component of the despatch advice

#create order reference

#create despatch supplier party
    #from the order advice use SellerSupplierParty

#create delivery customer party
    #from the order use Buyer customer Party

#create shipment
    #extract from the shipment json

#create despatch line
    #map items, quantities and price details from the order advice

#https://docs.oasis-open.org/ubl/os-UBL-2.4/xml/UBL-DespatchAdvice-2.0-Example.xml 