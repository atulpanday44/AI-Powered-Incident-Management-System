"""
Logging configuration for the application.
Provides structured logging with JSON formatting for production.
"""

import logging
import json
from typing import Any
from datetime import datetime
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter for structured logging."""

    def add_fields(
        self, log_record: dict, record: logging.LogRecord, message_dict: dict
    ) -> None:
        """Add custom fields to log record."""
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record["timestamp"] = datetime.utcnow().isoformat()
        log_record["level"] = record.levelname
        log_record["logger"] = record.name


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Configure application logging with JSON format.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("incident_manager")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Console handler with JSON formatter
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))

    formatter = CustomJsonFormatter(
        "%(timestamp)s %(level)s %(name)s %(message)s"
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(f"incident_manager.{name}")
