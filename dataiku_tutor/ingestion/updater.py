"""Incremental indexing orchestration for ingestion and re-indexing workflows."""

from __future__ import annotations

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
        documents = self.loader.load_documents(source_path)
        chunks = self.chunker.chunk(documents)
        embeddings = self._prepare_embeddings(chunks)

        metadata = [
            {
                "id": chunk.id,
                "document_id": chunk.document_id,
                "content": chunk.content,
                "metadata": chunk.metadata,
            }
            for chunk in chunks
        ]

        self.vector_store.add(embeddings=embeddings, metadata=metadata)
        self.vector_store.save()
        return len(chunks)

    def run_incremental_update(self, changed_sources: list[str]) -> int:
        """Update index only for changed docs and return updated chunk count."""
        if not changed_sources:
            return 0

        updated_chunks = 0
        for source in changed_sources:
            documents = self.loader.load_documents(source)
            chunks = self.chunker.chunk(documents)
            if not chunks:
                continue

            self.vector_store.delete([chunk.id for chunk in chunks])
            embeddings = self._prepare_embeddings(chunks)
            metadata = [
                {
                    "id": chunk.id,
                    "document_id": chunk.document_id,
                    "content": chunk.content,
                    "metadata": chunk.metadata,
                }
                for chunk in chunks
            ]
            self.vector_store.add(embeddings=embeddings, metadata=metadata)
            updated_chunks += len(chunks)

        self.vector_store.save()
        return updated_chunks

    def _prepare_embeddings(self, chunks: list[Chunk]) -> list[list[float]]:
        """Extract chunk content and request embedding vectors."""
        if not chunks:
            return []
        texts = [chunk.content for chunk in chunks]
        return self.embedding_service.embed(texts)
