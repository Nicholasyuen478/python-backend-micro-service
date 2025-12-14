from .client import (
    DynamoDBClientService,
    get_dynamodb_client_service,
    dynamodb_client_service,
)
from .interfaces import DynamoDBClientServiceInterface


__all__ = [
    "DynamoDBClientService",
    "get_dynamodb_client_service",
    "DynamoDBClientServiceInterface",
    "dynamodb_client_service",
]
