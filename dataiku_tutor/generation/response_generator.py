"""Prompting and response-shaping for procedural Dataiku guidance."""

from dataiku_tutor.domain.models import RetrievedChunk


class ResponseGenerator:
    """Builds grounded prompts and returns step-by-step task instructions."""

    def __init__(self, llm_client, max_sources: int = 5) -> None:
        self.llm_client = llm_client
        self.max_sources = max_sources

    def generate(self, query: str, retrieved_chunks: list[RetrievedChunk]) -> str:
        """Generate procedural answer with references to retrieved docs."""
        raise NotImplementedError

    def build_prompt(self, query: str, retrieved_chunks: list[RetrievedChunk]) -> str:
        """Construct constrained prompt enforcing operational step output."""
        raise NotImplementedError

    def format_sources(self, retrieved_chunks: list[RetrievedChunk]) -> list[dict]:
        """Extract source metadata for API/UI rendering."""
        raise NotImplementedError
