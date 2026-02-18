"""Vector store abstraction for local and cloud backends."""

from abc import ABC, abstractmethod
from typing import Any

from dataiku_tutor.domain.models import RetrievedChunk


class BaseVectorStore(ABC):
    """Dense vector storage contract independent of backend technology."""

    @abstractmethod
    def add(self, embeddings: list[list[float]], metadata: list[dict[str, Any]]) -> None:
        """Persist vectors and associated metadata."""

    @abstractmethod
    def search(self, query_embedding: list[float], k: int) -> list[RetrievedChunk]:
        """Run similarity search and return ranked chunks."""

    @abstractmethod
    def delete(self, ids: list[str]) -> None:
        """Remove vectors by chunk ids for incremental updates."""

    @abstractmethod
    def save(self) -> None:
        """Persist in-memory state to durable storage."""
