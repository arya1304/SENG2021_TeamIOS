import pytest
import json
from unittest.mock import patch, Mock
from updateBackorderDelivered import lambda_handler

@pytest.fixture
def mock_dynamodb():
    mock_resource = Mock()
    mock_table = Mock()
    mock_resource.Table.return_value = mock_table
    return mock_resource, mock_table

@patch("boto3.resource")
def test_update_success(mock_boto_resource, mock_dynamodb):
    mock_resource, mock_table = mock_dynamodb
    mock_boto_resource.return_value = mock_resource

    # Mock existing item
    mock_table.get_item.return_value = {
        "Item": {
            "ID": "123"
        }
    }

    event = {
        "pathParameters": {
            "despatchId": "123"
        },
        "body": json.dumps({
            "deliveredQuantity": 10,
            "backorderQuantity": 90
        })
    }

    response = lambda_handler(event, {})

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["DeliveredQuantity"] == 10
    assert body["BackorderQuantity"] == 90
    assert "Successfully updated Despatch Advice 123" in body["message"]

    mock_table.get_item.assert_called_once_with(Key={"ID": "123"})
    mock_table.update_item.assert_called_once()

@patch("boto3.resource")
def test_no_despatch_id(mock_boto_resource, mock_dynamodb):
    mock_resource, mock_table = mock_dynamodb
    mock_boto_resource.return_value = mock_resource

    event = {
        "pathParameters": {},
        "body": json.dumps({
            "deliveredQuantity": 0,
            "backorderQuantity": 100
        })
    }

    response = lambda_handler(event, {})

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "despatch ID is not provided" in body["message"]

    mock_table.get_item.assert_not_called()
    mock_table.update_item.assert_not_called()

@patch("boto3.resource")
def test_invalid_despatch_id(mock_boto_resource, mock_dynamodb):
    mock_resource, mock_table = mock_dynamodb
    mock_boto_resource.return_value = mock_resource

    # Mock that we do NOT find the item in DB
    mock_table.get_item.return_value = {}

    event = {
        "pathParameters": {
            "despatchId": "doesnotexist"
        },
        "body": json.dumps({
            "deliveredQuantity": 0,
            "backorderQuantity": 100
        })
    }

    response = lambda_handler(event, {})

    assert response["statusCode"] == 404
    body = json.loads(response["body"])
    assert "Not Found - The despatch ID is invalid" in body["message"]
    
    mock_table.get_item.assert_called_once_with(Key={"ID": "doesnotexist"})
    mock_table.update_item.assert_not_called()

@patch("boto3.resource")
def test_missing_body_values(mock_boto_resource, mock_dynamodb):
    mock_resource, mock_table = mock_dynamodb
    mock_boto_resource.return_value = mock_resource

    # Mock existing item
    mock_table.get_item.return_value = {
        "Item": {
            "ID": "123"
        }
    }

    event = {
        "pathParameters": {
            "despatchId": "123"
        },
        # No deliveredQuantity/backorderQuantity
        "body": json.dumps({})
    }

    response = lambda_handler(event, {})
    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "Must include deliveredQuantity and backorderQuantity" in body["message"]

    mock_table.get_item.assert_not_called()
    mock_table.update_item.assert_not_called()
