"""
FastAPI routes for log ingestion.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.db import get_db
from app.schemas import (
    LogIngestRequest,
    LogResponse,
    HealthResponse,
)
from app.services import LogService
from app.kafka import get_producer
from app.core import get_settings
from datetime import datetime

router = APIRouter(prefix="/api/v1", tags=["logs"])
settings = get_settings()


@router.post("/logs", response_model=LogResponse, status_code=status.HTTP_201_CREATED)
async def ingest_logs(
    log_request: LogIngestRequest,
    db: Session = Depends(get_db),
) -> LogResponse:
    """
    Ingest application logs.

    Validates input and publishes to Kafka for processing.

    Args:
        log_request: Log data request
        db: Database session

    Returns:
        Created log object

    Raises:
        HTTPException: If ingestion fails
    """
    try:
        # Prepare log data
        log_data = {
            "service": log_request.service,
            "level": log_request.level.value,
            "message": log_request.message,
            "timestamp": log_request.timestamp or datetime.utcnow(),
        }

        # Store in database
        log = LogService.ingest_log(db, log_data)
        if not log:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to store log"
            )

        # Add UUID and ingestion time
        log_data["log_id"] = str(log.id)
        log_data["ingestion_time"] = datetime.utcnow().isoformat()

        # Publish to Kafka
        producer = get_producer()
        kafka_success = producer.send_log(log_data)

        if not kafka_success:
            # Log warning but don't fail the request
            import logging
            logging.warning(f"Failed to publish log to Kafka: {log.id}")

        return LogResponse.model_validate(log)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ingest log: {str(e)}"
        )


@router.get("/logs", response_model=List[LogResponse])
async def get_logs(
    service: str | None = None,
    level: str | None = None,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[LogResponse]:
    """
    Retrieve logs with optional filtering.

    Args:
        service: Filter by service name
        level: Filter by log level
        limit: Maximum number of logs to return
        db: Database session

    Returns:
        List of logs
    """
    try:
        logs = LogService.get_logs(db, service=service, level=level, limit=limit)
        return [LogResponse.model_validate(log) for log in logs]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve logs: {str(e)}"
        )


@router.get("/logs/{log_id}", response_model=LogResponse)
async def get_log(
    log_id: UUID,
    db: Session = Depends(get_db),
) -> LogResponse:
    """
    Get specific log by ID.

    Args:
        log_id: Log ID
        db: Database session

    Returns:
        Log object

    Raises:
        HTTPException: If log not found
    """
    try:
        log = LogService.get_log_by_id(db, log_id)
        if not log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Log {log_id} not found"
            )
        return LogResponse.model_validate(log)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve log: {str(e)}"
        )


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns:
        Health status
    """
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow()
    )
