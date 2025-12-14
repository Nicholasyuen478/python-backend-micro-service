"""
Test configuration for Health Service
"""

import pytest
from unittest.mock import MagicMock
from common.databases.dynamoDB.interfaces import DynamoDBClientServiceInterface
from ..health_service import HealthService


@pytest.fixture
def mock_dynamodb_client():
    """Fixture for mocked DynamoDB resource."""
    mock_client = MagicMock()
    mock_client.meta.client.list_tables.return_value = {"TableNames": ["TestTable"]}
    return mock_client


@pytest.fixture
def mock_dynamodb_client_service(mock_dynamodb_client):
    """Fixture for mocked DynamoDB client service."""
    mock_service = MagicMock(spec=DynamoDBClientServiceInterface)
    mock_service.get_client.return_value = mock_dynamodb_client
    return mock_service


@pytest.fixture
def health_service(mock_dynamodb_client_service):
    """Fixture for HealthService with mocked DynamoDB client service."""
    return HealthService(dynamodb_client_service=mock_dynamodb_client_service)
