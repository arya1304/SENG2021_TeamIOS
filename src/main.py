from fastapi import FastAPI
from pydantic import BaseModel
from pydanticModels import models2,models,shipmentModel

app = FastAPI()

class Create_Request(BaseModel):
    Order: dict
    cac_Shipment:dict

@app.patch('/v1/despatchAdvice/')
def create_despatch_advice(req: Create_Request):
    #the request body will be in the format of json
    order = req.Order
    shipment = req.cac_Shipment
