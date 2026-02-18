"""Core domain models shared across the RAG pipeline."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class Document:
    """Normalized documentation unit before chunking."""

    id: str
    content: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class Chunk:
    """Token-aware chunk enriched with hierarchy metadata."""

    id: str
    document_id: str
    content: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class RetrievedChunk:
    """Single retrieved chunk with source and score metadata."""

    chunk: Chunk
    score: float
    source: str


@dataclass(frozen=True)
class QueryRequest:
    """Application-level query request payload."""

    question: str
    top_k: int = 5
    mode: str = "hybrid"


@dataclass(frozen=True)
class QueryResponse:
    """Application-level response payload."""

    answer: str
    sources: list[dict[str, Any]] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.utcnow)
