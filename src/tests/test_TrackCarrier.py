import json, pytest
from unittest.mock import patch, Mock
from trackCarrier import lambda_handler

@pytest.fixture
def mock_dynamodb():
    resource = Mock()
    table    = Mock()
    resource.Table.return_value = table
    return resource, table


@patch("requests.get")
@patch("boto3.resource")
def test_track_success(mock_boto_resource, mock_requests_get, mock_dynamodb):
    resource, table = mock_dynamodb
    mock_boto_resource.return_value = resource

    # DynamoDB item with carrier + tracking number
    table.get_item.return_value = {
        "Item": {"ID": "123", "Carrier": "UPS", "TrackingNumber": "1Z999"}
    }

    # Mock carrier API JSON response
    mock_resp = Mock(status_code=200)
    mock_resp.json.return_value = {"status": "In Transit", "location": "NY", "eta": "2025-04-10"}
    mock_requests_get.return_value = mock_resp

    event = {"pathParameters": {"despatchId": "123"}}
    resp  = lambda_handler(event, {})

    assert resp["statusCode"] == 200
    assert resp["tracking"]["status"] == "In Transit"
    table.update_item.assert_called_once()


@patch("requests.get")
@patch("boto3.resource")
def test_missing_tracking_fields(mock_boto_resource, mock_requests_get, mock_dynamodb):
    resource, table = mock_dynamodb
    mock_boto_resource.return_value = resource

    # no Carrier / TrackingNumber
    table.get_item.return_value = {"Item": {"ID": "123"}}

    event = {"pathParameters": {"despatchId": "123"}}
    resp  = lambda_handler(event, {})

    assert resp["statusCode"] == 400
    table.update_item.assert_not_called()
    mock_requests_get.assert_not_called()


@patch("requests.get")
@patch("boto3.resource")
def test_invalid_despatch_id(mock_boto_resource, mock_requests_get, mock_dynamodb):
    resource, table = mock_dynamodb
    mock_boto_resource.return_value = resource

    # no Item
    table.get_item.return_value = {}

    event = {"pathParameters": {"despatchId": "doesNotExist"}}
    resp  = lambda_handler(event, {})

    assert resp["statusCode"] == 404
    mock_requests_get.assert_not_called()
