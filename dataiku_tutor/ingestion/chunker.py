"""Token-aware chunking strategy interfaces and skeletons."""

from dataiku_tutor.domain.models import Chunk, Document


class DocumentationChunker:
    """Splits documents into overlapping chunks while preserving hierarchy metadata."""

    def __init__(self, chunk_size: int, overlap: int) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, documents: list[Document]) -> list[Chunk]:
        """Produce chunks with inherited metadata and section breadcrumbs."""
        raise NotImplementedError

    def _split_text(self, text: str) -> list[str]:
        """Token-aware splitting helper with overlap windows."""
        raise NotImplementedError
