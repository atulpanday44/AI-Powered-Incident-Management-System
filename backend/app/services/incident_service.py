"""
Business logic services for log and incident management.
"""

from typing import Dict, Any, List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Log, Incident, SeverityLevel, IncidentStatus
from app.core import get_logger
from app.kafka import get_producer

logger = get_logger("services.log_service")


class LogService:
    """Service for managing logs."""

    @staticmethod
    def ingest_log(db: Session, log_data: Dict[str, Any]) -> Optional[Log]:
        """
        Ingest and store log.

        Args:
            db: Database session
            log_data: Log data dictionary

        Returns:
            Created Log object or None if failed
        """
        try:
            log = Log(
                message=log_data.get("message", ""),
                level=log_data.get("level", "INFO"),
                service=log_data.get("service", "unknown"),
                timestamp=log_data.get("timestamp", datetime.utcnow()),
            )
            db.add(log)
            db.commit()
            db.refresh(log)

            logger.info(
                "Log ingested successfully",
                extra={
                    "log_id": str(log.id),
                    "service": log.service,
                    "level": log.level,
                }
            )
            return log
        except Exception as e:
            logger.error(f"Failed to ingest log: {str(e)}")
            db.rollback()
            return None

    @staticmethod
    def get_logs(
        db: Session,
        service: Optional[str] = None,
        level: Optional[str] = None,
        limit: int = 100,
    ) -> List[Log]:
        """
        Retrieve logs with optional filtering.

        Args:
            db: Database session
            service: Filter by service name
            level: Filter by log level
            limit: Maximum number of logs to return

        Returns:
            List of Log objects
        """
        query = db.query(Log)

        if service:
            query = query.filter(Log.service == service)
        if level:
            query = query.filter(Log.level == level)

        return query.order_by(Log.timestamp.desc()).limit(limit).all()

    @staticmethod
    def get_log_by_id(db: Session, log_id: UUID) -> Optional[Log]:
        """Get log by ID."""
        return db.query(Log).filter(Log.id == log_id).first()


class IncidentService:
    """Service for managing incidents."""

    @staticmethod
    def create_incident(db: Session, incident_data: Dict[str, Any]) -> Optional[Incident]:
        """
        Create new incident.

        Args:
            db: Database session
            incident_data: Incident data dictionary

        Returns:
            Created Incident object or None if failed
        """
        try:
            incident = Incident(
                title=incident_data.get("title", ""),
                service=incident_data.get("service", "unknown"),
                severity=incident_data.get("severity", SeverityLevel.MEDIUM),
                status=incident_data.get("status", IncidentStatus.OPEN),
                cluster_id=incident_data.get("cluster_id"),
                anomaly_score=incident_data.get("anomaly_score"),
            )
            db.add(incident)
            db.commit()
            db.refresh(incident)

            logger.info(
                "Incident created",
                extra={
                    "incident_id": str(incident.id),
                    "title": incident.title,
                    "severity": incident.severity,
                }
            )
            return incident
        except Exception as e:
            logger.error(f"Failed to create incident: {str(e)}")
            db.rollback()
            return None

    @staticmethod
    def get_incident_by_id(db: Session, incident_id: UUID) -> Optional[Incident]:
        """Get incident by ID."""
        return db.query(Incident).filter(Incident.id == incident_id).first()

    @staticmethod
    def get_incidents(
        db: Session,
        service: Optional[str] = None,
        status: Optional[str] = None,
        severity: Optional[str] = None,
        limit: int = 100,
    ) -> List[Incident]:
        """
        Retrieve incidents with optional filtering.

        Args:
            db: Database session
            service: Filter by service name
            status: Filter by status
            severity: Filter by severity
            limit: Maximum number of incidents to return

        Returns:
            List of Incident objects
        """
        query = db.query(Incident)

        if service:
            query = query.filter(Incident.service == service)
        if status:
            query = query.filter(Incident.status == status)
        if severity:
            query = query.filter(Incident.severity == severity)

        return query.order_by(Incident.created_at.desc()).limit(limit).all()

    @staticmethod
    def update_incident(
        db: Session,
        incident_id: UUID,
        update_data: Dict[str, Any]
    ) -> Optional[Incident]:
        """
        Update existing incident.

        Args:
            db: Database session
            incident_id: Incident ID to update
            update_data: Dictionary with fields to update

        Returns:
            Updated Incident object or None if not found
        """
        try:
            incident = db.query(Incident).filter(Incident.id == incident_id).first()
            if not incident:
                return None

            for field, value in update_data.items():
                if hasattr(incident, field) and value is not None:
                    setattr(incident, field, value)

            incident.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(incident)

            logger.info(
                "Incident updated",
                extra={
                    "incident_id": str(incident.id),
                    "update_data": update_data,
                }
            )
            return incident
        except Exception as e:
            logger.error(f"Failed to update incident: {str(e)}")
            db.rollback()
            return None

    @staticmethod
    def get_open_incidents(db: Session, limit: int = 100) -> List[Incident]:
        """Get all open incidents."""
        return (
            db.query(Incident)
            .filter(Incident.status.in_([IncidentStatus.OPEN, IncidentStatus.IN_PROGRESS]))
            .order_by(Incident.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_statistics(db: Session) -> Dict[str, Any]:
        """Get incident statistics."""
        try:
            total_incidents = db.query(Incident).count()
            open_incidents = db.query(Incident).filter(
                Incident.status.in_([IncidentStatus.OPEN, IncidentStatus.IN_PROGRESS])
            ).count()
            critical_incidents = db.query(Incident).filter(
                Incident.severity == SeverityLevel.CRITICAL
            ).count()
            high_incidents = db.query(Incident).filter(
                Incident.severity == SeverityLevel.HIGH
            ).count()

            return {
                "total_incidents": total_incidents,
                "open_incidents": open_incidents,
                "critical_incidents": critical_incidents,
                "high_incidents": high_incidents,
            }
        except Exception as e:
            logger.error(f"Failed to get statistics: {str(e)}")
            return {}
