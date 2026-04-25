"""Incident management module for deduplication and severity classification."""

from .deduplication import DeduplicationEngine
from .severity import SeverityClassifier

__all__ = ["DeduplicationEngine", "SeverityClassifier"]
