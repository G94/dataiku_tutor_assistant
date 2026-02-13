"""Application service orchestrating retrieval and generation flows."""

from dataiku_tutor.domain.models import QueryRequest, QueryResponse


class TutorService:
    """Coordinates retriever selection and response generation."""

    def __init__(self, retrievers: dict[str, object], response_generator) -> None:
        self.retrievers = retrievers
        self.response_generator = response_generator

    def answer(self, request: QueryRequest) -> QueryResponse:
        """Process user question and return grounded answer + sources."""
        raise NotImplementedError

    def _select_retriever(self, mode: str):
        """Route retrieval mode to semantic, keyword, or hybrid strategy."""
        raise NotImplementedError
