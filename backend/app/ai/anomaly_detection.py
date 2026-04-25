"""
Anomaly detection module using statistical methods.
Detects spikes in error frequency using Z-score.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from collections import deque
import math
from app.core import get_logger, get_settings

logger = get_logger("ai.anomaly_detection")
settings = get_settings()


class AnomalyDetector:
    """Detects anomalies in log streams using statistical methods."""

    def __init__(self, window_size: int = 100):
        """
        Initialize anomaly detector.

        Args:
            window_size: Number of logs to track in sliding window
        """
        self.window_size = window_size
        self.log_history: deque = deque(maxlen=window_size)
        self.error_counts: Dict[str, List[int]] = {}
        self.threshold = settings.ANOMALY_DETECTION_THRESHOLD

    def detect(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect if log represents an anomaly.

        Args:
            log_data: Dictionary containing log information

        Returns:
            Dictionary with anomaly detection results
        """
        try:
            service = log_data.get("service", "unknown")
            level = log_data.get("level", "INFO")

            # Add to history
            self.log_history.append({
                "service": service,
                "level": level,
                "timestamp": log_data.get("timestamp", datetime.utcnow())
            })

            # Track error counts
            if service not in self.error_counts:
                self.error_counts[service] = []

            # Count errors in window
            error_count = sum(
                1 for log in self.log_history
                if log["service"] == service and log["level"] in ["ERROR", "CRITICAL"]
            )
            self.error_counts[service].append(error_count)

            # Keep only recent counts (window size)
            if len(self.error_counts[service]) > self.window_size:
                self.error_counts[service].pop(0)

            # Calculate anomaly score using Z-score
            anomaly_score = self._calculate_z_score(service)
            is_anomaly = abs(anomaly_score) > self.threshold

            logger.debug(
                "Anomaly detection result",
                extra={
                    "service": service,
                    "level": level,
                    "anomaly_score": anomaly_score,
                    "is_anomaly": is_anomaly,
                }
            )

            return {
                "is_anomaly": is_anomaly,
                "anomaly_score": anomaly_score,
                "service": service,
            }

        except Exception as e:
            logger.error(f"Error in anomaly detection: {str(e)}")
            return {
                "is_anomaly": False,
                "anomaly_score": 0.0,
                "service": log_data.get("service", "unknown"),
            }

    def _calculate_z_score(self, service: str) -> float:
        """
        Calculate Z-score for error count spike.

        Args:
            service: Service name

        Returns:
            Z-score value
        """
        if service not in self.error_counts:
            return 0.0

        counts = self.error_counts[service]
        if len(counts) < 2:
            return 0.0

        # Current value
        current = counts[-1]

        # Calculate mean and std dev
        mean = sum(counts[:-1]) / len(counts[:-1]) if len(counts) > 1 else 0
        variance = sum((x - mean) ** 2 for x in counts[:-1]) / max(len(counts[:-1]), 1)
        std_dev = math.sqrt(variance) if variance > 0 else 1.0

        # Avoid division by zero
        if std_dev == 0:
            return 0.0 if current == mean else float('inf')

        # Z-score = (x - mean) / std_dev
        z_score = (current - mean) / std_dev
        return z_score
