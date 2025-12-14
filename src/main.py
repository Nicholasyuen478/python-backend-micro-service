from fastapi import FastAPI
from contextlib import asynccontextmanager

from health import health_controller
from common.s3 import s3_controller
from common.config import settings
from common.loggers import logger
from common.databases.dynamoDB import (
    dynamodb_client_service,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup: Initialize DynamoDB client once
    logger.info("Starting application...")
    dynamodb_client_service.initialize()

    yield  # Application runs here

    # Shutdown: Clean up resources
    logger.info("Shutting down application...")
    dynamodb_client_service.close()


DOCS = f"""
This API is currently running in the **{settings.ENVIRONMENT}** environment.
This project is a fastAPI + uv + AWS boto3 backend python project.
"""

app = FastAPI(
    title="Python FastAPI Service", description=DOCS, version="1.0.0", lifespan=lifespan
)

app.include_router(
    health_controller.router,
    prefix=f"/v{settings.API_VERSION}",
)

app.include_router(
    s3_controller.router,
    prefix=f"/v{settings.API_VERSION}",
)
