import pytest
from unittest.mock import patch, Mock
from retrieveEarliest import lambda_handler

TABLE_NAME = "DespatchAdviceTable"

# will run before each test function
@pytest.fixture
def mock_dynamodb():
    mock_client = Mock()
    
    mock_client.scan.return_value = {
        "Items": [
            {
                "ID": {"S": "1"},
                "EarliestDeliveryDate": {"S": "2025-04-08"}
            },
            {
                "ID": {"S": "2"},
                "EarliestDeliveryDate": {"S": "2025-04-07"}
            },
            {
                "ID": {"S": "3"},
                "EarliestDeliveryDate": {"S": "2025-04-06"}
            }
        ]
    }

    return mock_client

@patch("boto3.client")
def test_retrieve_success(mock_boto_client, mock_dynamodb):
    # test correct response
    mock_boto_client.return_value = mock_dynamodb

    response = lambda_handler({}, {})

    assert response["statusCode"] == 200
    assert response["count"] == "There are 1 despatch advices with the earliest delivery date: 2025-04-06"
    assert response["despatchAdvices"] == {
        "despatchAdvicesIDs": ["ID: 3"]
    }
