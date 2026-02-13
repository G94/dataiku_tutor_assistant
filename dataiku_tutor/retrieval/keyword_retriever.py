"""Keyword retrieval component (BM25 or equivalent sparse index)."""

from dataiku_tutor.domain.models import Chunk, RetrievedChunk


class KeywordRetriever:
    """Performs lexical retrieval to capture exact Dataiku terminology matches."""

    def __init__(self) -> None:
        self._index_ready = False

    def build_index(self, chunks: list[Chunk]) -> None:
        """Create sparse index over chunk text and metadata keywords."""
        raise NotImplementedError

    def retrieve(self, query: str, k: int) -> list[RetrievedChunk]:
        """Return top-k keyword matches from sparse index."""
        raise NotImplementedError
