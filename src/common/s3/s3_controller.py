from fastapi import APIRouter, status, Depends
from .schemas import GeneratePresignedUrlRequest, GeneratePresignedUrlResponse
from .s3_service import S3Service, get_s3_service

router = APIRouter(
    prefix="/s3",
    tags=["s3"],
)


@router.post(
    "/presigned-url",
    summary="Generated a pre-signed url for frontend to upload file, the default expiration time is 3 minutes",
    response_description="Return the pre-signed url to frontend",
    status_code=status.HTTP_200_OK,
    response_model=GeneratePresignedUrlResponse,
)
def generate_s3_file_upload_url(
    request: GeneratePresignedUrlRequest,
    s3_service: S3Service = Depends(get_s3_service),
):
    response = s3_service.generate_presigned_url(
        bucket_name=request.bucket_name,
        file_name=request.file_name,
        expiration=request.expiration,
    )
    return response
