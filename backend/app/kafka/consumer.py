"""
Kafka consumer for processing logs and creating incidents.
"""

import json
import time
from typing import Dict, Any, Optional
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from sqlalchemy.orm import Session
from app.core import get_logger, get_settings
from app.db import SessionLocal, engine, init_db
from app.models import Log, Incident, SeverityLevel, IncidentStatus
from app.ai.anomaly_detection import AnomalyDetector
from app.ai.clustering import LogClusterer
from app.incident.deduplication import DeduplicationEngine
from app.incident.severity import SeverityClassifier
from datetime import datetime, timedelta

logger = get_logger("kafka.consumer")
settings = get_settings()


class LogConsumer:
    """Kafka consumer for processing logs and creating incidents."""

    def __init__(self):
        """Initialize Kafka consumer."""
        self.db_session: Optional[Session] = None
        self.anomaly_detector = AnomalyDetector()
        self.clusterer = LogClusterer()
        self.deduplication_engine = DeduplicationEngine()
        self.severity_classifier = SeverityClassifier()

        try:
            self.consumer = KafkaConsumer(
                settings.KAFKA_LOGS_TOPIC,
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS.split(","),
                group_id=settings.KAFKA_CONSUMER_GROUP,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                max_poll_records=100,
                session_timeout_ms=30000,
            )
            logger.info(
                "Kafka consumer initialized",
                extra={
                    "bootstrap_servers": settings.KAFKA_BOOTSTRAP_SERVERS,
                    "topic": settings.KAFKA_LOGS_TOPIC,
                    "group_id": settings.KAFKA_CONSUMER_GROUP,
                }
            )
        except Exception as e:
            logger.error(f"Failed to initialize Kafka consumer: {str(e)}")
            raise

    def process_log(self, log_data: Dict[str, Any]) -> bool:
        """
        Process a single log message.

        Args:
            log_data: Dictionary containing log information

        Returns:
            True if processing succeeded, False otherwise
        """
        try:
            # Create database session
            self.db_session = SessionLocal()

            # Step 1: Store log in database
            log = self._store_log(log_data)
            if not log:
                return False

            # Step 2: Run anomaly detection
            anomaly_result = None
            if settings.ENABLE_ANOMALY_DETECTION:
                anomaly_result = self.anomaly_detector.detect(log_data)

            # Step 3: Run clustering
            cluster_id = None
            if settings.ENABLE_CLUSTERING:
                cluster_result = self.clusterer.cluster(log_data)
                cluster_id = cluster_result.get("cluster_id")

            # Step 4: Check for existing incident (deduplication)
            existing_incident = self._check_deduplication(
                log_data, cluster_id, anomaly_result
            )

            if existing_incident:
                # Update existing incident
                self._update_incident(existing_incident)
                logger.info(
                    "Updated existing incident",
                    extra={
                        "incident_id": str(existing_incident.id),
                        "service": log_data.get("service"),
                    }
                )
            else:
                # Create new incident
                severity = self.severity_classifier.classify(
                    log_data, anomaly_result
                )
                self._create_incident(log_data, cluster_id, anomaly_result, severity)

            self.db_session.commit()
            return True

        except Exception as e:
            logger.error(
                f"Error processing log: {str(e)}",
                extra={"log_data": log_data}
            )
            if self.db_session:
                self.db_session.rollback()
            return False
        finally:
            if self.db_session:
                self.db_session.close()

    def _store_log(self, log_data: Dict[str, Any]) -> Optional[Log]:
        """Store log in database."""
        try:
            log = Log(
                message=log_data.get("message", ""),
                level=log_data.get("level", "INFO"),
                service=log_data.get("service", "unknown"),
                timestamp=log_data.get("timestamp", datetime.utcnow()),
            )
            self.db_session.add(log)
            self.db_session.flush()
            logger.debug(
                "Log stored in database",
                extra={
                    "log_id": str(log.id),
                    "service": log_data.get("service"),
                    "level": log_data.get("level"),
                }
            )
            return log
        except Exception as e:
            logger.error(f"Failed to store log: {str(e)}")
            return None

    def _check_deduplication(
        self,
        log_data: Dict[str, Any],
        cluster_id: Optional[str],
        anomaly_result: Optional[Dict[str, Any]],
    ) -> Optional[Incident]:
        """Check if log matches existing incident for deduplication."""
        try:
            service = log_data.get("service")
            level = log_data.get("level")

            # Query for recent incidents
            cutoff_time = datetime.utcnow() - timedelta(
                seconds=settings.DEDUPLICATION_TIME_WINDOW
            )

            query = self.db_session.query(Incident).filter(
                Incident.service == service,
                Incident.status.in_([IncidentStatus.OPEN, IncidentStatus.IN_PROGRESS]),
                Incident.created_at >= cutoff_time,
            )

            # Filter by cluster if available
            if cluster_id:
                query = query.filter(Incident.cluster_id == cluster_id)

            existing_incident = query.first()
            return existing_incident

        except Exception as e:
            logger.error(f"Error checking deduplication: {str(e)}")
            return None

    def _create_incident(
        self,
        log_data: Dict[str, Any],
        cluster_id: Optional[str],
        anomaly_result: Optional[Dict[str, Any]],
        severity: str,
    ):
        """Create new incident."""
        try:
            incident = Incident(
                title=f"{log_data.get('level')} - {log_data.get('service')}",
                service=log_data.get("service", "unknown"),
                severity=severity,
                status=IncidentStatus.OPEN,
                cluster_id=cluster_id,
                anomaly_score=anomaly_result.get("anomaly_score") if anomaly_result else None,
            )
            self.db_session.add(incident)
            logger.info(
                "Incident created",
                extra={
                    "incident_id": str(incident.id),
                    "service": log_data.get("service"),
                    "severity": severity,
                    "cluster_id": cluster_id,
                }
            )
        except Exception as e:
            logger.error(f"Failed to create incident: {str(e)}")

    def _update_incident(self, incident: Incident):
        """Update existing incident."""
        try:
            incident.log_count += 1
            incident.updated_at = datetime.utcnow()
            self.db_session.merge(incident)
        except Exception as e:
            logger.error(f"Failed to update incident: {str(e)}")

    def start(self):
        """Start consuming logs from Kafka."""
        logger.info("Starting Kafka consumer...")
        try:
            for message in self.consumer:
                if message.value:
                    self.process_log(message.value)
        except KeyboardInterrupt:
            logger.info("Kafka consumer interrupted")
        except Exception as e:
            logger.error(f"Kafka consumer error: {str(e)}")
        finally:
            self.close()

    def close(self):
        """Close consumer connection."""
        self.consumer.close()
        logger.info("Kafka consumer closed")


def start_consumer():
    """Initialize database and start consumer."""
    init_db()
    consumer = LogConsumer()
    consumer.start()
