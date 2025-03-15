import sys
import json
from rich import print
from pydanticModels import models2, shipmentModel
from DespatchAdviceFactory import DespatchAdvice

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


        # Generate Despatch Advice
        factory = DespatchAdvice()
        despatch_advice = factory.create_despatch_advice(order, shipment)

        # Print the result
        print("Generated Despatch Advice:")
        print(despatch_advice)

    except json.JSONDecodeError:
        print("Invalid JSON format. Please enter valid JSON.")

if __name__ == "__main__":
    main()
