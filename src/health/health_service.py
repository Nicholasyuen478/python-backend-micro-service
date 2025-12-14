from fastapi import Depends
from common.loggers import logger
from .interfaces import HealthServiceInterface

from common.exceptions import InternalServiceError
from common.databases.dynamoDB import (
    DynamoDBClientServiceInterface,
    get_dynamodb_client_service,
)


class HealthService(HealthServiceInterface):
    def __init__(self, dynamodb_client_service: DynamoDBClientServiceInterface):
        self.dynamodb_client = dynamodb_client_service.get_client()

    async def check_health(self) -> dict:
        logger.info("Perform health check")

        try:
            # Lightweight operation to verify connection
            response = self.dynamodb_client.meta.client.list_tables(Limit=1)
            logger.info({"dynamodb_list_table_response": response})
            if "TableNames" in response:
                return {"status": "OK"}
            else:
                return {"status": "unhealthy"}
        except Exception as e:
            message = "DynamoDB health check failed"
            logger.error(f"{message}: {e}")
            raise InternalServiceError(message) from e


def get_health_service(
    dynamodb_client_service: DynamoDBClientServiceInterface = Depends(
        get_dynamodb_client_service
    ),
) -> HealthService:
    return HealthService(dynamodb_client_service)
