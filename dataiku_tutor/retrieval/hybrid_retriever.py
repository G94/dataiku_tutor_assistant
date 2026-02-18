"""Hybrid retrieval merging semantic and keyword results."""

from dataiku_tutor.domain.models import RetrievedChunk


class HybridRetriever:
    """Combines sparse and dense retrievers using weighted score fusion."""

    def __init__(self, semantic_retriever, keyword_retriever, semantic_weight: float = 0.6) -> None:
        self.semantic_retriever = semantic_retriever
        self.keyword_retriever = keyword_retriever
        self.semantic_weight = semantic_weight

    def retrieve(self, query: str, k: int) -> list[RetrievedChunk]:
        """Merge and rerank semantic and keyword outputs."""
        raise NotImplementedError

    def _normalize_scores(self, results: list[RetrievedChunk]) -> list[RetrievedChunk]:
        """Normalize retriever-specific score ranges before fusion."""
        raise NotImplementedError
