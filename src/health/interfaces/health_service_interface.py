from abc import ABC, abstractmethod


class HealthServiceInterface(ABC):
    @abstractmethod
    async def check_health(self) -> dict:
        """Perform health check logic."""
        pass
