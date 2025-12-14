from abc import ABC, abstractmethod
from ..schemas import GeneratePresignedUrlResponse, S3Operation


class S3ServiceInterface(ABC):
    @abstractmethod
    def generate_presigned_url(
        self,
        bucket_name: str,
        file_name: str,
        expiration: int | None = 180,
        operation: S3Operation = S3Operation.PUT_OBJECT,
    ) -> GeneratePresignedUrlResponse:
        """Generate a pre-signed URL for accessing a file in S3. Supports both upload (PUT_OBJECT) and download (GET_OBJECT)."""
        pass

    @abstractmethod
    def read_file_from_s3(self, bucket_name: str, file_name: str) -> bytes:
        """Read bytes of a file from S3."""
        pass
