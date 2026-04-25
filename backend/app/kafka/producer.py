"""
Kafka producer for publishing logs to Kafka topics.
"""

import json
from typing import Dict, Any
from kafka import KafkaProducer
from kafka.errors import KafkaError
from app.core import get_logger, get_settings

logger = get_logger("kafka.producer")
settings = get_settings()


class LogProducer:
    """Kafka producer for publishing logs."""

    def __init__(self):
        """Initialize Kafka producer."""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS.split(","),
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                acks="all",
                retries=3,
                max_in_flight_requests_per_connection=5,
            )
            logger.info(
                "Kafka producer initialized",
                extra={
                    "bootstrap_servers": settings.KAFKA_BOOTSTRAP_SERVERS,
                    "topic": settings.KAFKA_LOGS_TOPIC,
                }
            )
        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {str(e)}")
            raise

    def send_log(self, log_data: Dict[str, Any]) -> bool:
        """
        Send log to Kafka topic.

        Args:
            log_data: Dictionary containing log information

        Returns:
            True if successful, False otherwise
        """
        try:
            future = self.producer.send(settings.KAFKA_LOGS_TOPIC, value=log_data)
            record_metadata = future.get(timeout=10)

            logger.info(
                "Log published to Kafka",
                extra={
                    "topic": record_metadata.topic,
                    "partition": record_metadata.partition,
                    "offset": record_metadata.offset,
                    "service": log_data.get("service"),
                    "level": log_data.get("level"),
                }
            )
            return True
        except KafkaError as e:
            logger.error(
                f"Failed to send log to Kafka: {str(e)}",
                extra={"log_data": log_data}
            )
            return False
        except Exception as e:
            logger.error(
                f"Unexpected error sending log to Kafka: {str(e)}",
                extra={"log_data": log_data}
            )
            return False

    def close(self):
        """Close producer connection."""
        self.producer.close()


# Singleton instance
_producer_instance: LogProducer | None = None


def get_producer() -> LogProducer:
    """Get or create producer singleton."""
    global _producer_instance
    if _producer_instance is None:
        _producer_instance = LogProducer()
    return _producer_instance
