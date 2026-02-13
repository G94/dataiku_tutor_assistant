"""Embedding provider abstraction and provider-specific skeletons."""

from abc import ABC, abstractmethod


class EmbeddingService(ABC):
    """Abstract embedding service contract for swappable providers."""

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Convert texts into dense vectors."""


class OpenAIEmbeddingService(EmbeddingService):
    """Embedding service placeholder for OpenAI embedding APIs."""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError


class SentenceTransformerEmbeddingService(EmbeddingService):
    """Embedding service placeholder for sentence-transformers backends."""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError


class EmbeddingFactory:
    """Factory for constructing embedding services from configuration."""

    @staticmethod
    def create(provider: str, model_name: str) -> EmbeddingService:
        raise NotImplementedError
