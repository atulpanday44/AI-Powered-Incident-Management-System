"""
Severity classification for incidents.
Uses rule-based approach based on log level and frequency.
"""

from typing import Dict, Any, Optional
from app.core import get_logger

logger = get_logger("incident.severity")


class SeverityClassifier:
    """Classifies incident severity based on log characteristics."""

    # Severity rules
    CRITICAL_KEYWORDS = {
        'critical', 'panic', 'crash', 'fatal', 'failure', 'down',
        'outage', 'unavailable', 'unrecoverable', 'system failure'
    }

    ERROR_KEYWORDS = {
        'error', 'exception', 'failed', 'failure', 'fault',
        'unexpected', 'invalid', 'unable', 'could not'
    }

    WARNING_KEYWORDS = {
        'warning', 'warn', 'deprecated', 'slow', 'timeout',
        'retry', 'fallback', 'degraded'
    }

    def classify(
        self,
        log_data: Dict[str, Any],
        anomaly_result: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Classify incident severity.

        Args:
            log_data: Dictionary containing log information
            anomaly_result: Optional anomaly detection result

        Returns:
            Severity level: CRITICAL, HIGH, MEDIUM, LOW
        """
        try:
            level = log_data.get("level", "INFO").upper()
            message = log_data.get("message", "").lower()

            # Check for critical keywords
            if any(keyword in message for keyword in self.CRITICAL_KEYWORDS):
                return "CRITICAL"

            if level == "CRITICAL":
                return "CRITICAL"

            # Check for error-level issues
            if level == "ERROR":
                # If anomaly detected, escalate to HIGH
                if anomaly_result and anomaly_result.get("is_anomaly"):
                    return "HIGH"
                # Check message content
                if any(keyword in message for keyword in self.ERROR_KEYWORDS):
                    return "HIGH"
                return "MEDIUM"

            # Check for warning
            if level == "WARNING":
                if any(keyword in message for keyword in self.WARNING_KEYWORDS):
                    return "MEDIUM"
                return "LOW"

            # Default
            return "LOW"

        except Exception as e:
            logger.error(f"Error in severity classification: {str(e)}")
            # Fail safe to MEDIUM
            return "MEDIUM"

    def should_create_incident(
        self,
        severity: str,
        log_level: str
    ) -> bool:
        """
        Determine if incident should be created for this log.

        Args:
            severity: Classified severity level
            log_level: Original log level

        Returns:
            True if incident should be created
        """
        # Create incidents for ERROR and above
        return log_level.upper() in ["ERROR", "CRITICAL"]
