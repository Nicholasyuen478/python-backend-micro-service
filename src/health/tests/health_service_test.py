import pytest
from common.exceptions import InternalServiceError


@pytest.mark.asyncio
async def test_check_health_success(health_service):
    """Test successful health check"""
    result = await health_service.check_health()

    assert result == {"status": "OK"}
    assert health_service.dynamodb_client.meta.client.list_tables.called


@pytest.mark.asyncio
async def test_check_health_no_tables(health_service, mock_dynamodb_client):
    """Test health check with no tables"""
    # Override the return value for this specific test
    mock_dynamodb_client.meta.client.list_tables.return_value = {}

    result = await health_service.check_health()

    assert result == {"status": "unhealthy"}


@pytest.mark.asyncio
async def test_check_health_exception(health_service, mock_dynamodb_client):
    """Test health check with exception"""
    # Make list_tables raise an exception
    mock_dynamodb_client.meta.client.list_tables.side_effect = Exception(
        "Connection failed"
    )

    with pytest.raises(InternalServiceError) as exc_info:
        await health_service.check_health()

    assert "DynamoDB health check failed" in str(exc_info.value)


@pytest.mark.asyncio
async def test_check_health_verifies_table_names(health_service, mock_dynamodb_client):
    """Test that health check verifies TableNames key exists"""
    # Test with different table names
    mock_dynamodb_client.meta.client.list_tables.return_value = {
        "TableNames": ["Table1", "Table2"]
    }

    result = await health_service.check_health()

    assert result == {"status": "OK"}
    mock_dynamodb_client.meta.client.list_tables.assert_called_once_with(Limit=1)
