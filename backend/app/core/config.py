"""
Application configuration settings.
Uses environment variables for all configuration.
"""

import os
from functools import lru_cache
from typing import Optional
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "AI Incident Management System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://incident_user:incident_password@postgres:5432/incident_db"
    )
    SQLALCHEMY_ECHO: bool = os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS",
        "kafka:9092"
    )
    KAFKA_LOGS_TOPIC: str = os.getenv("KAFKA_LOGS_TOPIC", "logs-topic")
    KAFKA_INCIDENTS_TOPIC: str = os.getenv("KAFKA_INCIDENTS_TOPIC", "incidents-topic")
    KAFKA_CONSUMER_GROUP: str = os.getenv("KAFKA_CONSUMER_GROUP", "incident-processor")

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # AI/ML
    ANOMALY_DETECTION_THRESHOLD: float = float(
        os.getenv("ANOMALY_DETECTION_THRESHOLD", "2.0")
    )
    DEDUPLICATION_TIME_WINDOW: int = int(
        os.getenv("DEDUPLICATION_TIME_WINDOW", "300")
    )  # 5 minutes
    CLUSTERING_SIMILARITY_THRESHOLD: float = float(
        os.getenv("CLUSTERING_SIMILARITY_THRESHOLD", "0.7")
    )
    ANOMALY_WINDOW_SIZE: int = int(
        os.getenv("ANOMALY_WINDOW_SIZE", "100")
    )  # Number of logs to track

    # Feature flags
    ENABLE_ANOMALY_DETECTION: bool = os.getenv(
        "ENABLE_ANOMALY_DETECTION", "True"
    ).lower() == "true"
    ENABLE_CLUSTERING: bool = os.getenv(
        "ENABLE_CLUSTERING", "True"
    ).lower() == "true"


@lru_cache()
def get_settings() -> Settings:
    """Get application settings (cached singleton)."""
    return Settings()
