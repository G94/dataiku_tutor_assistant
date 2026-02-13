"""Incremental indexing orchestration for ingestion and re-indexing workflows."""

from dataiku_tutor.domain.models import Chunk


class IndexUpdater:
    """Coordinates document loading, chunking, embedding, and vector updates."""

    def __init__(self, loader, chunker, embedding_service, vector_store) -> None:
        self.loader = loader
        self.chunker = chunker
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def run_full_reindex(self, source_path: str) -> int:
        """Rebuild index from scratch and return indexed chunk count."""
        raise NotImplementedError

    def run_incremental_update(self, changed_sources: list[str]) -> int:
        """Update index only for changed docs and return updated chunk count."""
        raise NotImplementedError

    def _prepare_embeddings(self, chunks: list[Chunk]) -> list[list[float]]:
        """Extract chunk content and request embedding vectors."""
        raise NotImplementedError
