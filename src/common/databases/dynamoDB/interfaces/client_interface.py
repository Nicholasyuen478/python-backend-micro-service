from abc import ABC, abstractmethod
from typing import Any


class DynamoDBClientServiceInterface(ABC):
    """Abstract interface for DynamoDB client"""

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize DynamoDB client once at startup

        Raises:
            InternalServiceError: If initialization fails
        """
        pass

    @abstractmethod
    def get_client(self) -> Any:
        """
        Get the initialized DynamoDB resource

        Returns:
            Any: DynamoDB resource object
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Close DynamoDB connection and clean up resources
        """
        pass
