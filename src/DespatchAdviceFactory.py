
from typing import Type 
from pydanticModels import models2, models
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
import uuid
from datetime import datetime

class DespatchAdviceFactory :
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

    #create despatch supplier party
    #from the order advice use SellerSupplierParty
    def create_despatch_supplier_party(self, orderAdvice: models2.Order) -> models.CacDespatchSupplierParty:
        pass

    #create delivery customer party
    #from the order use Buyer customer Party
    def create_delivery_customer_party(self, orderAdvice: models2.Order) -> models.CacDeliveryCustomerParty:
        pass

    #create shipment
    #extract from the shipment json
    #what happens when we get an empty field?
    #create an optional field for requested delivery period 
    #determine what fields that can be
    def create_shipment(self, shipment: models.CacShipment) -> models.CacShipment:
        despatch_delivery = models.CacShipment(
            cbc_ID = shipment.cbc_ID,
            cac_Consignment = shipment.cac_Consignment,
            cac_Delivery = shipment.cac_Delivery
        )
        return despatch_delivery


    #create despatch line
    #map items, quantities and price details from the order advice
    #each item has its own despatch line 

    def create_despatch_line(self, orderAdvice: models2.Order) -> models.CacDespatchLine:
        order = orderAdvice.cac_OrderLine
        line_item_dict = orderAdvice.cac_OrderLine.cac_LineItem
        order_ref = self.create_order_reference(orderAdvice)

        despatch_line = models.CacDespatchLine(
            cbc_ID = line_item_dict.cbc_ID,
            cbc_Note = order.cbc_Note,
            cbc_LineStatusCode = line_item_dict.cbc_LineStatusCode,
            cbc_DeliveredQuantity = models.CbcDeliveredQuantity(
                field_unitCode = line_item_dict.cbc_Quantity.field_unitCode,
                text = '0'
            ),
            cbc_BackorderQuantity = models.CbcDeliveredQuantity(
                field_unitCode = line_item_dict.cbc_Quantity.field_unitCode,
                text = line_item_dict.cbc_Quantity.text
            ),
            cbc_BackorderReason = '',
            cac_OrderLineReference = models.CacOrderLineReference(
                cbc_LineID = '',
                cbc_SalesOrderLineID = '',
                cac_OrderReference = order_ref
            ),
            cac_Item = line_item_dict.cac_Item
        )
        return despatch_line

    #create despatch advice
    def create_despatch_advice(self, orderAdvice: models2.Order, shipment: models.CacShipment) -> models.DespatchAdvice:
        #will return a peydantic model of the despatch advice
        despatch_advice = models.DespatchAdvice(
            field_xmlns_cbc = orderAdvice.field_xmlns,
            field_xmlns_cac = orderAdvice.field_xmlns_cac,
            field_xmlns = orderAdvice.field_xmlns,
            cbc_UBLVersionID = orderAdvice.cbc_UBLVersionID,
            cbc_ProfileID = orderAdvice.cbc_ProfileID,
            cbc_ID = '',
            cbc_CopyIndicator = 'false',
            cbc_UUID = uuid.uuid4(), #generating a uuid
            cbc_IssueDate = datetime.today().strftime('%Y-%m-%d'),
            cbc_DocumentStatusCode = 'NoStatus',
            cbc_DespatchAdviceTypeCode = 'delivery',
            cbc_Note = '',
            order_ref = self.create_order_reference(orderAdvice), 
            supplier_party = self.create_despatch_supplier_party(orderAdvice),
            customer_party = self.create_delivery_customer_party(orderAdvice),
            shipment_details = self.create_shipment(shipment),
            despatch_line = self.create_despatch_line(orderAdvice)
        )
        return despatch_advice
    
    #convert it into xml format

    #https://docs.oasis-open.org/ubl/os-UBL-2.4/xml/UBL-DespatchAdvice-2.0-Example.xml 


    # the defs will return the despatch advice as a pydantic model and then we use ET to convert it into a xml
    # first we convert the xml into a dict