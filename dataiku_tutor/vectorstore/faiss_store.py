"""FAISS-backed vector store skeleton for local execution."""

from pathlib import Path
from typing import Any

from dataiku_tutor.domain.models import RetrievedChunk
from dataiku_tutor.vectorstore.base_store import BaseVectorStore


class FaissVectorStore(BaseVectorStore):
    """Local FAISS implementation placeholder with metadata persistence."""

    def __init__(self, index_path: str, metadata_path: str) -> None:
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)

    def add(self, embeddings: list[list[float]], metadata: list[dict[str, Any]]) -> None:
        raise NotImplementedError

    def search(self, query_embedding: list[float], k: int) -> list[RetrievedChunk]:
        raise NotImplementedError

    def delete(self, ids: list[str]) -> None:
        raise NotImplementedError

    def save(self) -> None:
        raise NotImplementedError


class VectorStoreFactory:
    """Factory to support backend migration (FAISS, OpenSearch, Qdrant, etc.)."""

    @staticmethod
    def create(config: dict[str, Any]) -> BaseVectorStore:
        raise NotImplementedError
