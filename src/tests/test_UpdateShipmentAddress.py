import pytest
from unittest.mock import patch, Mock
from ..updateShipmentAddress import update_shipment_address

@patch("boto3.resource")
def test_update_shipment_address_success(mock_boto3_resource):
    mock_table = Mock()
    mock_boto3_resource.return_value.Table.return_value = mock_table
    
    mock_table.get_item.return_value = {
        "Item": {"ID": "123", "ShipmentAddress": "Old Address"}
    }

    mock_table.update_item.return_value = {}

    request = {"shipment_id": "123", "new_address": "New Address"}

    response = update_shipment_address(request)

    assert response["statusCode"] == 200
    assert response["message"] == "Shipment address updated successfully"
    mock_table.get_item.assert_called_once_with(Key={"ID": "123"})
    mock_table.update_item.assert_called_once_with(
        Key={"ID": "123"},
        UpdateExpression="set ShipmentAddress = :new_address",
        ExpressionAttributeValues={":new_address": "New Address"}
    )
    mock_boto3_resource.assert_called_once_with('dynamodb')
    mock_boto3_resource.return_value.Table.assert_called_once_with('DespatchAdviceTable')

@patch("boto3.resource")
def test_update_shipment_address_invalid_id(mock_boto3_resource):
    mock_table = Mock()
    mock_boto3_resource.return_value.Table.return_value = mock_table
 
    mock_table.get_item.return_value = {}
    
    request = {"shipment_id": "999", "new_address": "New Address"}

    response = update_shipment_address(request)
 
    assert response["statusCode"] == 404
    assert response["body"] == "Not Found - The shipment ID is invalid"
    mock_table.get_item.assert_called_once_with(Key={"ID": "999"})
    mock_table.update_item.assert_not_called()

@patch("boto3.resource")
def test_update_shipment_address_missing_parameters(mock_boto3_resource):
    mock_table = Mock()
    mock_boto3_resource.return_value.Table.return_value = mock_table
 
    request = {}

    response = update_shipment_address(request)
 
    assert response["statusCode"] == 400
    assert response["body"] == "Bad Request - The shipment ID or new address is not provided"
    mock_table.get_item.assert_not_called()
    mock_table.update_item.assert_not_called()

@patch("boto3.resource")
def test_update_shipment_address_missing_shipment_id(mock_boto3_resource):
    mock_table = Mock()
    mock_boto3_resource.return_value.Table.return_value = mock_table

    request = {"new_address": "New Address"}
    
    response = update_shipment_address(request)
    
    assert response["statusCode"] == 400
    assert response["body"] == "Bad Request - The shipment ID or new address is not provided"
    mock_table.get_item.assert_not_called()
    mock_table.update_item.assert_not_called()

@patch("boto3.resource")
def test_update_shipment_address_missing_new_address(mock_boto3_resource):
    mock_table = Mock()
    mock_boto3_resource.return_value.Table.return_value = mock_table

    request = {"shipment_id": "123"}
    
    response = update_shipment_address(request)
 
    assert response["statusCode"] == 400
    assert response["body"] == "Bad Request - The shipment ID or new address is not provided"
    mock_table.get_item.assert_not_called()
    mock_table.update_item.assert_not_called()

@patch("boto3.resource")
def test_update_shipment_address_invalid_address(mock_boto3_resource):
    mock_table = Mock()
    mock_boto3_resource.return_value.Table.return_value = mock_table

    request = {"shipment_id": "123", "new_address": "    "}  
    
    response = update_shipment_address(request)
    
    assert  response["statusCode"] == 400
    assert response["body"] == "Bad Request - The new address is invalid"
    mock_table.get_item.assert_not_called()
    mock_table.update_item.assert_not_called()


