from pydantic import BaseModel, EmailStr
from typing import List

class Customer(BaseModel):
    CustomerId: int
    CustName: str
    CustEmail: EmailStr
    CustAddress: str

class OrderLineReference(BaseModel):
    OrderLineId: int
    SalesOrderLineId: int
    OrderReferenceId: int
    SalesOrderId: int
    UUID: int
    IssueDate: int

class Item(BaseModel):
    ItemId: int
    ItemName: int
    ItemDescription: int
    BuyersItemId: int
    SellersItemId: int

class Shipment(BaseModel):
    shipmentId: int

class OrderAdvice(BaseModel):
    order_line_ref : OrderLineReference
    customer_details : Customer
    list_of_items : List[Item]

#create a pydantic model for the despatch advice and all 