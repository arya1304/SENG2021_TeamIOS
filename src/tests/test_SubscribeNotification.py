import json, pytest
from unittest.mock import patch, Mock
from subscribeNotification import lambda_handler

@pytest.fixture
def mock_dynamodb():
    res   = Mock()
    table = Mock()
    res.Table.return_value = table
    return res, table

@patch("boto3.resource")
def test_subscribe_success(mock_boto_resource, mock_dynamodb):
    res, table = mock_dynamodb
    mock_boto_resource.return_value = res

    event = {
        "body": json.dumps({
            "email": "alice@example.com",
            "eventType": "CREATE"
        })
    }

    resp = lambda_handler(event, {})
    assert resp["statusCode"] == 201
    table.put_item.assert_called_once()

@patch("boto3.resource")
def test_subscribe_missing_fields(mock_boto_resource, mock_dynamodb):
    res, table = mock_dynamodb
    mock_boto_resource.return_value = res

    event = {"body": json.dumps({"email": "noType@example.com"})}
    resp  = lambda_handler(event, {})
    assert resp["statusCode"] == 400
    table.put_item.assert_not_called()
