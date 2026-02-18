"""Dense retrieval component for semantic matching."""

from dataiku_tutor.domain.models import RetrievedChunk


class SemanticRetriever:
    """Queries vector store using query embeddings for semantic relevance."""

    def __init__(self, embedding_service, vector_store) -> None:
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(self, query: str, k: int) -> list[RetrievedChunk]:
        """Return top-k semantically similar documentation chunks."""
        raise NotImplementedError
