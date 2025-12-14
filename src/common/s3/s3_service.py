import boto3
from botocore import client

from common.config import settings
from common.loggers import logger
from common.exceptions import InternalServiceError, ValidationError

from .interfaces import S3ServiceInterface
from .schemas import GeneratePresignedUrlResponse, S3Operation


class S3Service(S3ServiceInterface):
    def __init__(self):
        try:
            self.session = boto3.Session(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION,
            )
            self.s3_client = self.session.client(
                "s3", config=client.Config(signature_version="s3v4")
            )
            logger.info("S3 Client initialized")
        except Exception as e:
            message = f"Failed to create s3 Client : {str(e)}"
            logger.error(message)
            raise InternalServiceError("Failed to create s3 Client ") from e

    def generate_presigned_url(
        self,
        bucket_name: str,
        file_name: str,
        expiration: int | None = 180,
        operation: S3Operation = S3Operation.PUT_OBJECT,
    ) -> GeneratePresignedUrlResponse:
        """
        Generate a pre-signed URL for accessing a file in S3. Default expiry 3 minutes (180 seconds).

        Args:
            bucket_name: The name of the S3 bucket
            file_name: The key (file name) of the file
            expiration: URL expiration time in seconds (default: 180)
            operation: S3 operation - PUT_OBJECT for upload, GET_OBJECT for download (default: PUT_OBJECT)

        Returns:
            GeneratePresignedUrlResponse containing the pre-signed URL
        """
        if not bucket_name or not file_name:
            raise ValidationError(
                field="Bucket name and file name",
                message="Bucket name and file name must be provided",
            )
        try:
            url: str = self.s3_client.generate_presigned_url(
                ClientMethod=operation.value,
                Params={
                    "Bucket": bucket_name,
                    "Key": file_name,
                },
                ExpiresIn=expiration,
            )
            logger.info({url})

            message = f"Generated pre-signed URL for {operation.action_name} of file {file_name} in bucket {bucket_name}"
            logger.info(message)

            return GeneratePresignedUrlResponse(presigned_url=url)
        except Exception as e:
            message = f"Failed to generate pre-signed URL for bucket '{bucket_name}', file '{file_name}'"
            logger.error(f"{message}: {e}")
            raise InternalServiceError(message) from e

    def read_file_from_s3(self, bucket_name: str, file_name: str) -> bytes:  # type: ignore
        """
        Read the file bytes from an S3 bucket.

        Args:
            bucket_name (str): The name of the S3 bucket containing the file.
            file_name (str): The key (file name) of the file to read.

        Returns:
            bytes: The content of the file as bytes.
        """
        if not bucket_name or not file_name:
            raise ValidationError(
                field="Bucket name and file name",
                message="Bucket name and file name must be provided",
            )
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=file_name)
            file_bytes = response["Body"].read()
            logger.info(f"Successfully read file {file_name} from bucket {bucket_name}")
            return file_bytes

        except Exception as e:
            message = (
                f"Failed to read file from bucket '{bucket_name}', file '{file_name}'"
            )
            logger.error(f"{message}: {e}")
            raise InternalServiceError(message) from e


async def get_s3_service() -> S3Service:
    return S3Service()
