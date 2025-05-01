import pytest, json
from unittest.mock import patch, Mock
from publishNotification import lambda_handler

@pytest.fixture
def mock_dynamodb():
    res   = Mock()
    table = Mock()
    res.Table.return_value = table
    return res, table

@patch("boto3.client")
@patch("boto3.resource")
def test_publish_success(mock_boto_resource, mock_boto_client, mock_dynamodb):
    res, table = mock_dynamodb
    mock_boto_resource.return_value = res
    sns_client = Mock()
    mock_boto_client.return_value = sns_client

    # pretend we found two subscribers
    table.scan.return_value = {"Items": [{"SubscriptionID": "1"}, {"SubscriptionID": "2"}]}

    event = {"eventType": "UPDATE",
             "despatchId": "123",
             "message": "Order 123 updated."}

    resp = lambda_handler(event, {})
    assert resp["statusCode"] == 200
    assert resp["notified"] == 2
    sns_client.publish.assert_called()
    assert sns_client.publish.call_count == 2

@patch("boto3.client")
@patch("boto3.resource")
def test_publish_no_subscribers(mock_boto_resource, mock_boto_client, mock_dynamodb):
    res, table = mock_dynamodb
    mock_boto_resource.return_value = res
    mock_boto_client.return_value = Mock()

    table.scan.return_value = {"Items": []}
    event = {"eventType": "DELETE", "message": "Something happened"}

    resp = lambda_handler(event, {})
    assert resp["statusCode"] == 200
    assert resp["notified"] == 0
