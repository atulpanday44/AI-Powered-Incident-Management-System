"""
Deduplication engine for detecting duplicate/similar incidents.
"""

import hashlib
from typing import Dict, Any, Optional
from app.core import get_logger

logger = get_logger("incident.deduplication")


class DeduplicationEngine:
    """Handles deduplication of incidents based on similarity."""

    def __init__(self):
        """Initialize deduplication engine."""
        self.seen_hashes: set = set()

    def get_log_hash(self, log_data: Dict[str, Any]) -> str:
        """
        Generate hash for log message for deduplication.

        Args:
            log_data: Dictionary containing log information

        Returns:
            Hash string
        """
        try:
            # Normalize message by removing numbers and special chars for matching
            message = log_data.get("message", "")
            service = log_data.get("service", "")
            level = log_data.get("level", "")

            # Create signature from normalized content
            normalized = self._normalize_message(message)
            signature = f"{service}:{level}:{normalized}"

            hash_obj = hashlib.md5(signature.encode())
            return hash_obj.hexdigest()

        except Exception as e:
            logger.error(f"Error generating log hash: {str(e)}")
            return ""

    def _normalize_message(self, message: str) -> str:
        """
        Normalize message for similarity matching.

        Args:
            message: Raw message text

        Returns:
            Normalized message
        """
        import re

        # Convert to lowercase
        normalized = message.lower()

        # Remove numbers
        normalized = re.sub(r'\d+', 'X', normalized)

        # Remove special characters but keep spaces
        normalized = re.sub(r'[^a-z\s]', '', normalized)

        # Remove extra whitespace
        normalized = ' '.join(normalized.split())

        # Take first 100 chars as signature
        return normalized[:100]

    def is_duplicate(self, log_data: Dict[str, Any]) -> bool:
        """
        Check if log is a duplicate of previously seen log.

        Args:
            log_data: Dictionary containing log information

        Returns:
            True if duplicate, False otherwise
        """
        log_hash = self.get_log_hash(log_data)

        if log_hash in self.seen_hashes:
            logger.debug(
                "Duplicate log detected",
                extra={
                    "service": log_data.get("service"),
                    "level": log_data.get("level"),
                }
            )
            return True

        self.seen_hashes.add(log_hash)
        return False
