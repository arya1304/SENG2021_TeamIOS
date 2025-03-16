import sys
import json
from rich import print
from pydanticModels import models2, shipmentModel
from DespatchAdviceFactory import DespatchAdvice
from dict2xml import dict2xml
from collections import OrderedDict



def replace_specialchars(d):
    if isinstance(d, dict):
        return OrderedDict((k.replace("-", ":").replace("_", ":"), replace_specialchars(v)) for k, v in d.items())
    elif isinstance(d, list):
        return [replace_specialchars(i) for i in d]
    else:
        return d
    



def main():
    # Read JSON input from the terminal
    try:
        print("Enter JSON input for order and shipment:")
        # Open and read input.json
        with open("input.json", "r") as file:
            data = json.load(file)
        
        #print(data)
        # Extract order and shipment details
        order_data = data.get("Order")
        shipment_data = data.get("cac:Shipment")

        if not order_data or not shipment_data:
            print("Invalid input: Both 'order' and 'shipment' JSON objects are required.")
            return

        # Convert JSON to Order and CacShipment objects
        order = models2.Order(**order_data)
        shipment = shipmentModel.CacShipment(**shipment_data)
        factory = DespatchAdvice()
        despatch_advice = factory.create_despatch_advice(order, shipment)
        transformed_dict = factory.pydantic_to_xml(despatch_advice)


     

        # Print the result
        print("Generated Despatch Advice:")
        print(transformed_dict)
        #print(despatch_json_str)


    except json.JSONDecodeError:
        print("Invalid JSON format. Please enter valid JSON.")





if __name__ == "__main__":
    main()
