"""
Pydantic schemas for API request/response validation.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, validator
from uuid import UUID
from enum import Enum


class LogLevel(str, Enum):
    """Log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogIngestRequest(BaseModel):
    """Schema for log ingestion API request."""
    service: str = Field(..., min_length=1, max_length=255)
    level: LogLevel = Field(...)
    message: str = Field(..., min_length=1, max_length=2048)
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "service": "auth-service",
                "level": "ERROR",
                "message": "Database connection failed",
                "timestamp": "2024-04-25T10:30:00"
            }
        }


class LogResponse(BaseModel):
    """Schema for log response."""
    id: UUID
    service: str
    level: str
    message: str
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class SeverityLevel(str, Enum):
    """Severity levels."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IncidentStatus(str, Enum):
    """Incident status."""
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class IncidentCreate(BaseModel):
    """Schema for creating incidents."""
    title: str = Field(..., min_length=1, max_length=255)
    service: str = Field(..., min_length=1, max_length=255)
    severity: SeverityLevel = Field(...)
    cluster_id: Optional[str] = None
    anomaly_score: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "High Error Rate in Auth Service",
                "service": "auth-service",
                "severity": "HIGH",
                "cluster_id": "cluster_1",
                "anomaly_score": 3.2
            }
        }


class IncidentResponse(BaseModel):
    """Schema for incident response."""
    id: UUID
    title: str
    service: str
    severity: str
    status: str
    cluster_id: Optional[str]
    anomaly_score: Optional[float]
    log_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IncidentUpdate(BaseModel):
    """Schema for updating incidents."""
    status: Optional[IncidentStatus] = None
    severity: Optional[SeverityLevel] = None

    class Config:
        json_schema_extra = {
            "example": {
                "status": "RESOLVED",
                "severity": "MEDIUM"
            }
        }


class AnomalyDetectionResult(BaseModel):
    """Schema for anomaly detection results."""
    log_id: UUID
    is_anomaly: bool
    anomaly_score: float
    message: str = ""


class ClusteringResult(BaseModel):
    """Schema for clustering results."""
    log_id: UUID
    cluster_id: str
    similarity_score: float


class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str = "healthy"
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
