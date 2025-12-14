import pytest
from faker import Faker
from unittest.mock import MagicMock

from common.exceptions import InternalServiceError, ValidationError
from ..schemas.s3_schemas import GeneratePresignedUrlResponse


fake = Faker()


def test_generate_presigned_url_success(
    s3_service, mock_s3_client, bucket_name, file_name
):
    mock_url = fake.url()
    mock_s3_client.generate_presigned_url.return_value = mock_url

    response = s3_service.generate_presigned_url(bucket_name, file_name)

    mock_s3_client.generate_presigned_url.assert_called_once_with(
        ClientMethod="put_object",
        Params={"Bucket": bucket_name, "Key": file_name},
        ExpiresIn=180,
    )
    assert response == GeneratePresignedUrlResponse(presigned_url=mock_url)


def test_generate_presigned_url_missing_params(s3_service):
    with pytest.raises(ValidationError):
        s3_service.generate_presigned_url("", "file.txt")
    with pytest.raises(ValidationError):
        s3_service.generate_presigned_url("bucket", "")


def test_generate_presigned_url_failure(
    mock_s3_client, s3_service, bucket_name, file_name
):
    mock_s3_client.generate_presigned_url.side_effect = Exception("S3 error")
    with pytest.raises(InternalServiceError, match="Failed to generate pre-signed URL"):
        s3_service.generate_presigned_url(bucket_name, file_name)


def test_read_file_from_s3_success(
    s3_service, mock_s3_client, bucket_name, file_name, file_content
):
    mock_s3_client.get_object.return_value = {
        "Body": MagicMock(read=MagicMock(return_value=file_content))
    }

    result = s3_service.read_file_from_s3(bucket_name, file_name)

    mock_s3_client.get_object.assert_called_once_with(Bucket=bucket_name, Key=file_name)
    assert result == file_content


def test_read_file_from_s3_missing_params(s3_service):
    with pytest.raises(ValidationError):
        s3_service.read_file_from_s3("", "file.txt")
    with pytest.raises(ValidationError):
        s3_service.read_file_from_s3("bucket", "")


def test_read_file_from_s3_failure(
    mock_s3_client, s3_service, bucket_name, file_name
):
    mock_s3_client.get_object.side_effect = Exception("S3 error")
    with pytest.raises(InternalServiceError, match="Failed to read file from bucket"):
        s3_service.read_file_from_s3(bucket_name, file_name)


def test_generate_presigned_url_with_get_operation(
    s3_service, mock_s3_client, bucket_name, file_name, mock_presigned_url
):
    """Test generate_presigned_url with GET operation for downloading."""
    from ..schemas.s3_schemas import S3Operation

    mock_s3_client.generate_presigned_url.return_value = mock_presigned_url

    response = s3_service.generate_presigned_url(
        bucket_name, file_name, operation=S3Operation.GET_OBJECT
    )

    mock_s3_client.generate_presigned_url.assert_called_once_with(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": file_name},
        ExpiresIn=180,
    )
    assert response == GeneratePresignedUrlResponse(presigned_url=mock_presigned_url)


def test_generate_presigned_url_with_put_operation(
    s3_service, mock_s3_client, bucket_name, file_name, mock_presigned_url
):
    """Test generate_presigned_url with PUT operation for uploading."""
    from ..schemas.s3_schemas import S3Operation

    mock_s3_client.generate_presigned_url.return_value = mock_presigned_url

    response = s3_service.generate_presigned_url(
        bucket_name, file_name, operation=S3Operation.PUT_OBJECT
    )

    mock_s3_client.generate_presigned_url.assert_called_once_with(
        ClientMethod="put_object",
        Params={"Bucket": bucket_name, "Key": file_name},
        ExpiresIn=180,
    )
    assert response == GeneratePresignedUrlResponse(presigned_url=mock_presigned_url)


def test_generate_presigned_url_default_operation(
    s3_service, mock_s3_client, bucket_name, file_name, mock_presigned_url
):
    """Test generate_presigned_url defaults to PUT operation."""
    mock_s3_client.generate_presigned_url.return_value = mock_presigned_url

    response = s3_service.generate_presigned_url(bucket_name, file_name)

    # Should default to put_object
    mock_s3_client.generate_presigned_url.assert_called_once_with(
        ClientMethod="put_object",
        Params={"Bucket": bucket_name, "Key": file_name},
        ExpiresIn=180,
    )
    assert response == GeneratePresignedUrlResponse(presigned_url=mock_presigned_url)


def test_s3_operation_enum_action_name():
    """Test S3Operation enum action_name property."""
    from ..schemas.s3_schemas import S3Operation

    assert S3Operation.PUT_OBJECT.action_name == "upload"
    assert S3Operation.GET_OBJECT.action_name == "download"
