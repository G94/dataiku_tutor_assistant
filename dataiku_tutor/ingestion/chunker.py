"""Token-aware chunking strategy interfaces and skeletons."""

from __future__ import annotations

from dataiku_tutor.domain.models import Chunk, Document


class DocumentationChunker:
    """Splits documents into overlapping chunks while preserving hierarchy metadata."""

    def __init__(self, chunk_size: int, overlap: int) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be > 0")
        if overlap < 0:
            raise ValueError("overlap must be >= 0")
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, documents: list[Document]) -> list[Chunk]:
        """Produce chunks with inherited metadata and section breadcrumbs."""
        chunks: list[Chunk] = []
        for doc in documents:
            split_texts = self._split_text(doc.content)
            for idx, text in enumerate(split_texts):
                metadata = {
                    **doc.metadata,
                    "chunk_index": idx,
                    "chunk_size": self.chunk_size,
                    "chunk_overlap": self.overlap,
                }
                chunks.append(
                    Chunk(
                        id=f"{doc.id}:{idx}",
                        document_id=doc.id,
                        content=text,
                        metadata=metadata,
                    )
                )
        return chunks

    def _split_text(self, text: str) -> list[str]:
        """Token-aware splitting helper with overlap windows."""
        if not text or not text.strip():
            return []

        # Approximate tokenization with word units; can be swapped with tiktoken later.
        words = text.split()
        if not words:
            return []

        windows: list[str] = []
        start = 0
        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            window = " ".join(words[start:end]).strip()
            if window:
                windows.append(window)
            if end >= len(words):
                break
            start = max(0, end - self.overlap)
        return windows
