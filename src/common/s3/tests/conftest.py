import pytest
from unittest.mock import patch, MagicMock
from faker import Faker
from common.s3.s3_service import S3Service  # Adjust import as necessary
from ..schemas.s3_schemas import GeneratePresignedUrlResponse

fake = Faker()


@pytest.fixture
def s3_service():
    with patch("boto3.Session") as mock_session:
        mock_s3_client = MagicMock()
        mock_session.return_value.client.return_value = mock_s3_client
        yield S3Service()


@pytest.fixture
def mock_s3_client(s3_service):
    return s3_service.s3_client


@pytest.fixture
def bucket_name():
    return fake.word()  # Generate a random bucket name


@pytest.fixture
def file_name():
    return fake.file_name()  # Generate a random file name


@pytest.fixture
def file_content():
    return fake.text().encode("utf-8")  # Mock file content as bytes


@pytest.fixture
def valid_presigned_url_response():
    return GeneratePresignedUrlResponse(presigned_url=fake.url())


@pytest.fixture
def mock_presigned_url():
    """Generate a mock presigned URL."""
    return fake.url()


@pytest.fixture
def expiration_seconds():
    """Generate a random expiration time in seconds."""
    return fake.random_int(min=60, max=3600)
