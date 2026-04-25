"""
Consumer application for processing logs.
Entry point for the Kafka consumer service.
"""

import logging
from app.core import setup_logging, get_settings
from app.kafka import start_consumer

settings = get_settings()
setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger("incident_manager.consumer")


if __name__ == "__main__":
    logger.info("Starting Kafka consumer service...")
    try:
        start_consumer()
    except KeyboardInterrupt:
        logger.info("Consumer interrupted")
    except Exception as e:
        logger.error(f"Consumer error: {str(e)}", exc_info=True)
