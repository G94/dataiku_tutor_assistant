"""Embedding provider abstraction and provider-specific implementations."""

from __future__ import annotations

import hashlib
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
        raise NotImplementedError("OpenAI embedding integration intentionally not implemented yet.")


class SentenceTransformerEmbeddingService(EmbeddingService):
    """Embedding service for sentence-transformers backends with deterministic fallback."""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self._model = None
        self._load_error: Exception | None = None
        self._fallback_dimension = 384
        try:
            from sentence_transformers import SentenceTransformer  # type: ignore

            self._model = SentenceTransformer(model_name)
        except Exception as exc:  # pragma: no cover - environment dependent branch
            self._load_error = exc

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        if self._model is not None:
            vectors = self._model.encode(texts, normalize_embeddings=True)
            return [list(map(float, vector)) for vector in vectors]

        # deterministic fallback allows local testing even when dependency isn't installed.
        return [self._hash_embedding(text, self._fallback_dimension) for text in texts]

    @staticmethod
    def _hash_embedding(text: str, dim: int) -> list[float]:
        seed = text.encode("utf-8")
        values: list[float] = []
        counter = 0
        while len(values) < dim:
            digest = hashlib.sha256(seed + counter.to_bytes(4, "big")).digest()
            for idx in range(0, len(digest), 4):
                chunk = digest[idx : idx + 4]
                if len(chunk) < 4:
                    continue
                val = int.from_bytes(chunk, "big") / 2**32
                values.append((val * 2.0) - 1.0)
                if len(values) >= dim:
                    break
            counter += 1

        norm = sum(v * v for v in values) ** 0.5 or 1.0
        return [v / norm for v in values]


class EmbeddingFactory:
    """Factory for constructing embedding services from configuration."""

    @staticmethod
    def create(provider: str, model_name: str) -> EmbeddingService:
        normalized_provider = provider.strip().lower()
        if normalized_provider in {"sentence_transformers", "sentence-transformers"}:
            return SentenceTransformerEmbeddingService(model_name=model_name)
        if normalized_provider == "openai":
            return OpenAIEmbeddingService(model_name=model_name)
        raise ValueError(f"Unsupported embedding provider: {provider}")
