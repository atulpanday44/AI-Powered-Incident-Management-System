"""
Log clustering module using TF-IDF and cosine similarity.
Groups similar logs together.
"""

from typing import Dict, Any, Optional
from collections import defaultdict
import math
import re
from app.core import get_logger, get_settings

logger = get_logger("ai.clustering")
settings = get_settings()


class LogClusterer:
    """Clusters similar logs using TF-IDF and cosine similarity."""

    def __init__(self):
        """Initialize log clusterer."""
        self.clusters: Dict[str, list] = defaultdict(list)
        self.cluster_counter = 0
        self.vocabulary: set = set()
        self.document_count = 0
        self.doc_frequency: Dict[str, int] = defaultdict(int)
        self.similarity_threshold = settings.CLUSTERING_SIMILARITY_THRESHOLD

    def cluster(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cluster log message with existing clusters.

        Args:
            log_data: Dictionary containing log information

        Returns:
            Dictionary with cluster information
        """
        try:
            message = log_data.get("message", "")
            service = log_data.get("service", "unknown")

            # Normalize and tokenize message
            tokens = self._tokenize(message)
            self.vocabulary.update(tokens)
            self.document_count += 1

            # Update document frequency
            for token in set(tokens):
                self.doc_frequency[token] += 1

            # Find most similar cluster
            best_cluster_id = None
            best_similarity = 0.0

            for cluster_id, cluster_logs in self.clusters.items():
                if not cluster_logs:
                    continue

                # Compare with first log in cluster (representative)
                representative = cluster_logs[0]
                similarity = self._cosine_similarity(
                    tokens,
                    self._tokenize(representative["message"])
                )

                if similarity > best_similarity:
                    best_similarity = similarity
                    best_cluster_id = cluster_id

            # Create new cluster or add to existing
            if best_similarity >= self.similarity_threshold and best_cluster_id:
                self.clusters[best_cluster_id].append(log_data)
                logger.debug(
                    "Log added to existing cluster",
                    extra={
                        "cluster_id": best_cluster_id,
                        "similarity": best_similarity,
                        "service": service,
                    }
                )
            else:
                # Create new cluster
                self.cluster_counter += 1
                new_cluster_id = f"cluster_{service}_{self.cluster_counter}"
                self.clusters[new_cluster_id].append(log_data)
                best_cluster_id = new_cluster_id
                logger.debug(
                    "New cluster created",
                    extra={
                        "cluster_id": new_cluster_id,
                        "service": service,
                    }
                )

            return {
                "cluster_id": best_cluster_id,
                "similarity_score": best_similarity,
            }

        except Exception as e:
            logger.error(f"Error in clustering: {str(e)}")
            return {
                "cluster_id": f"cluster_error_{self.cluster_counter}",
                "similarity_score": 0.0,
            }

    def _tokenize(self, text: str) -> list:
        """
        Tokenize text for TF-IDF.

        Args:
            text: Text to tokenize

        Returns:
            List of tokens
        """
        # Convert to lowercase and remove special characters
        text = text.lower()
        # Split on whitespace and punctuation
        tokens = re.findall(r'\b\w+\b', text)
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'was', 'are', 'be', 'been',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can'
        }
        tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
        return tokens

    def _cosine_similarity(self, tokens1: list, tokens2: list) -> float:
        """
        Calculate cosine similarity between two token lists.

        Args:
            tokens1: First token list
            tokens2: Second token list

        Returns:
            Similarity score (0-1)
        """
        if not tokens1 or not tokens2:
            return 0.0

        # Count occurrences
        count1 = defaultdict(int)
        count2 = defaultdict(int)

        for token in tokens1:
            count1[token] += 1
        for token in tokens2:
            count2[token] += 1

        # Calculate TF-IDF vectors
        vector1 = {}
        vector2 = {}

        all_tokens = set(count1.keys()) | set(count2.keys())

        for token in all_tokens:
            # TF-IDF = (count / total) * log(doc_count / doc_frequency)
            tf1 = count1.get(token, 0) / len(tokens1)
            idf = math.log(max(self.document_count / self.doc_frequency[token], 1))
            vector1[token] = tf1 * idf

            tf2 = count2.get(token, 0) / len(tokens2)
            vector2[token] = tf2 * idf

        # Calculate cosine similarity
        dot_product = sum(
            vector1.get(token, 0) * vector2.get(token, 0)
            for token in all_tokens
        )

        magnitude1 = math.sqrt(sum(v ** 2 for v in vector1.values())) or 1
        magnitude2 = math.sqrt(sum(v ** 2 for v in vector2.values())) or 1

        similarity = dot_product / (magnitude1 * magnitude2)
        return max(0.0, min(1.0, similarity))  # Clamp to [0, 1]
