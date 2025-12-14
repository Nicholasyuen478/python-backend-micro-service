from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class S3Operation(Enum):
    """S3 operations for presigned URL generation."""

    PUT_OBJECT = "put_object"  # For uploading/writing files
    GET_OBJECT = "get_object"  # For downloading/reading files

    @property
    def action_name(self) -> str:
        """Return a user-friendly action name for logging."""
        return "upload" if self == S3Operation.PUT_OBJECT else "download"


class GeneratePresignedUrlRequest(BaseModel):
    bucket_name: str = Field(
        default="stg-poc-python-template-service",
        description="The name of the S3 bucket (default: 'stg-poc-python-template-service')",
    )
    file_name: str
    expiration: Optional[int] = Field(
        default=180, description="Expiration time in seconds for the presigned URL"
    )


class GeneratePresignedUrlResponse(BaseModel):
    presigned_url: str
