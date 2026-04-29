"""Database models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Enum as SQLEnum
import uuid
import enum
from app.db.session import Base


class SeverityLevel(str, enum.Enum):
    """Severity levels for incidents."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IncidentStatus(str, enum.Enum):
    """Status of incidents."""
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class Log(Base):
    """Logs table for storing application logs."""
    __tablename__ = "logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    message = Column(String(2048), nullable=False, index=True)
    level = Column(String(20), nullable=False, index=True)
    service = Column(String(255), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True, default=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Log {self.id} - {self.level} - {self.service}>"


class Incident(Base):
    """Incidents table for storing incident records."""
    __tablename__ = "incidents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False, index=True)
    service = Column(String(255), nullable=False, index=True)
    severity = Column(
        SQLEnum(SeverityLevel),
        nullable=False,
        default=SeverityLevel.MEDIUM,
        index=True
    )
    status = Column(
        SQLEnum(IncidentStatus),
        nullable=False,
        default=IncidentStatus.OPEN,
        index=True
    )
    cluster_id = Column(String(255), nullable=True, index=True)
    anomaly_score = Column(Float, nullable=True)
    log_count = Column(Integer, default=1)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Incident {self.id} - {self.title} - {self.severity}>"
