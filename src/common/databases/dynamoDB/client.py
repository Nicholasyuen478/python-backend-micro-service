from typing import Optional, Any
import boto3
from botocore.client import Config

from common.config import settings
from common.loggers import logger
from .interfaces import DynamoDBClientServiceInterface


class DynamoDBClientService(DynamoDBClientServiceInterface):
    def __init__(self):
        self._client: Optional[Any] = None

    def initialize(self) -> None:
        """Initialize DynamoDB client once at startup"""
        if self._client is None:
            client_config = {
                "region_name": settings.AWS_REGION,
                "config": Config(retries={"max_attempts": 3}),
            }

            if settings.AWS_ACCESS_KEY_ID:
                client_config["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
                client_config["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY

            self._client = boto3.resource("dynamodb", **client_config)
            logger.info("DynamoDB client initialized")

    # FIXME: No static type suggested by AWS BOTO3, so use ANY
    def get_client(self) -> Any:
        """Get the initialized DynamoDB resource"""
        if self._client is None:
            self.initialize()
            return self._client
        return self._client

    def close(self) -> None:
        """Close DynamoDB connection"""
        if self._client is not None:
            self._client = None
            logger.info("DynamoDB client connection closed")


# Module-level singleton instance
dynamodb_client_service = DynamoDBClientService()


def get_dynamodb_client_service() -> DynamoDBClientService:
    return dynamodb_client_service
