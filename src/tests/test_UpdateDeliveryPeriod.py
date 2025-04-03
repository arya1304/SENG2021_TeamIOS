import pytest
from unittest.mock import patch, Mock
from ..updateDeliveryPeriod import update_delivery_period

TABLE_NAME = "ShipmentTable"

@pytest.fixture
def mock_dynamodb():
    mock_resource = Mock()
    mock_table = Mock()
    mock_resource.Table.return_value = mock_table

    return mock_resource, mock_table


@patch("boto3.resource")
def test_update_delivery_period_success(mock_boto_resource, mock_dynamodb):
    mock_resource, mock_table = mock_dynamodb
    mock_boto_resource.return_value = mock_resource

    mock_table.get_item.return_value = {
        "Item": {"ID": "123", "DeliveryPeriod": "2025-03-01 to 2025-03-05"}
    }

    request = {"shipment_id": "123", "new_delivery_period": "2025-04-01 to 2025-04-05"}

    response = update_delivery_period(request)

    assert response["statusCode"] == 200
    assert response["message"] == "Shipment delivery period updated successfully"
    mock_table.get_item.assert_called_once_with(Key={"ID": "123"})
    mock_table.update_item.assert_called_once_with(
        Key={"ID": "123"},
        UpdateExpression="set DeliveryPeriod = :new_delivery_period",
        ExpressionAttributeValues={":new_delivery_period": "2025-04-01 to 2025-04-05"}
    )


@patch("boto3.resource")
def test_update_delivery_period_invalid_id(mock_boto_resource, mock_dynamodb):
    mock_resource, mock_table = mock_dynamodb
    mock_boto_resource.return_value = mock_resource

    mock_table.get_item.return_value = {}

    request = {"shipment_id": "999", "new_delivery_period": "2025-04-01 to 2025-04-05"}

    response = update_delivery_period(request)

    assert response["statusCode"] == 404
    assert response["message"] == "Shipment not found"
    mock_table.get_item.assert_called_once_with(Key={"ID": "999"})
    mock_table.update_item.assert_not_called()


@patch("boto3.resource")
def test_update_delivery_period_empty_parameters(mock_boto_resource, mock_dynamodb):
    mock_resource, mock_table = mock_dynamodb
    mock_boto_resource.return_value = mock_resource

    request = {}

    response = update_delivery_period(request)

    assert response["statusCode"] == 400
    assert response["message"] == "Invalid input parameters"
    mock_table.get_item.assert_not_called()
    mock_table.update_item.assert_not_called()


@patch("boto3.resource")
def test_update_delivery_period_missing_shipment_id(mock_boto_resource, mock_dynamodb):
    mock_resource, mock_table = mock_dynamodb
    mock_boto_resource.return_value = mock_resource

    request = {"new_delivery_period": "2025-04-01 to 2025-04-05"}

    response = update_delivery_period(request)

    assert response["statusCode"] == 400
    assert response["message"] == "Invalid input parameters"
    mock_table.get_item.assert_not_called()
    mock_table.update_item.assert_not_called()


@patch("boto3.resource")
def test_update_delivery_period_missing_new_delivery_period(mock_boto_resource, mock_dynamodb):
    mock_resource, mock_table = mock_dynamodb
    mock_boto_resource.return_value = mock_resource

    request = {"shipment_id": "123"}

    response = update_delivery_period(request)

    assert response["statusCode"] == 400
    assert response["message"] == "Invalid input parameters"
    mock_table.get_item.assert_not_called()
    mock_table.update_item.assert_not_called()

@patch("boto3.resource")
def test_update_delivery_period_invalid_date_format(mock_boto_resource):
    mock_table = Mock()
    mock_boto_resource.return_value.Table.return_value = mock_table
    
    request = {"shipment_id": "123", "start_date": "April 1", "end_date": "April 5"}
    response = update_delivery_period(request)
    
    assert response["statusCode"] == 400
    assert response["message"] == "Invalid input parameters"
    mock_table.get_item.assert_not_called()
    mock_table.update_item.assert_not_called()