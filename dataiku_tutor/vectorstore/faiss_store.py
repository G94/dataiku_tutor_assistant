"""FAISS-backed vector store for local execution with pure-Python fallback."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from dataiku_tutor.domain.models import Chunk, RetrievedChunk
from dataiku_tutor.vectorstore.base_store import BaseVectorStore


class FaissVectorStore(BaseVectorStore):
    """Local FAISS implementation with metadata persistence."""

    def __init__(self, index_path: str, metadata_path: str) -> None:
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)
        self._dim: int | None = None
        self._metadata: list[dict[str, Any]] = []
        self._deleted_ids: set[str] = set()
        self._index = None
        self._vectors: list[list[float]] = []
        self._use_faiss = False

        self._load_runtime_backend()
        self._load_existing()

    def add(self, embeddings: list[list[float]], metadata: list[dict[str, Any]]) -> None:
        if len(embeddings) != len(metadata):
            raise ValueError("embeddings and metadata must have the same length")
        if not embeddings:
            return

        dim = len(embeddings[0])
        if any(len(vector) != dim for vector in embeddings):
            raise ValueError("all embeddings must have consistent dimensions")
        if self._dim is None:
            self._dim = dim
            if self._use_faiss:
                self._index = self._faiss().IndexFlatIP(dim)
        elif self._dim != dim:
            raise ValueError(f"expected embedding dimension {self._dim}, got {dim}")

        normalized = [self._normalize(v) for v in embeddings]

        if self._use_faiss:
            self._index.add(self._to_faiss_matrix(normalized))
        else:
            self._vectors.extend(normalized)

        self._metadata.extend(metadata)

    def search(self, query_embedding: list[float], k: int) -> list[RetrievedChunk]:
        if k <= 0:
            return []
        if self._dim is None or not self._metadata:
            return []
        if len(query_embedding) != self._dim:
            raise ValueError(f"query embedding dim mismatch: expected {self._dim}, got {len(query_embedding)}")

        query = self._normalize(query_embedding)

        if self._use_faiss:
            scores, indices = self._index.search(self._to_faiss_matrix([query]), min(k, len(self._metadata)))
            scored = [(int(idx), float(score)) for idx, score in zip(indices[0].tolist(), scores[0].tolist())]
        else:
            scored = [(idx, self._dot(query, vector)) for idx, vector in enumerate(self._vectors)]
            scored.sort(key=lambda item: item[1], reverse=True)
            scored = scored[: min(k, len(scored))]

        results: list[RetrievedChunk] = []
        for idx, score in scored:
            if idx < 0 or idx >= len(self._metadata):
                continue
            row = self._metadata[idx]
            chunk_id = str(row.get("id", ""))
            if chunk_id and chunk_id in self._deleted_ids:
                continue
            chunk = Chunk(
                id=chunk_id,
                document_id=str(row.get("document_id", "")),
                content=str(row.get("content", "")),
                metadata=row.get("metadata", {}),
            )
            results.append(RetrievedChunk(chunk=chunk, score=float(score), source="faiss"))
        return results

    def delete(self, ids: list[str]) -> None:
        self._deleted_ids.update(ids)

    def save(self) -> None:
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.metadata_path.parent.mkdir(parents=True, exist_ok=True)

        if self._use_faiss:
            self._faiss().write_index(self._index, str(self.index_path))
        else:
            # Persist fallback vectors as JSON for dependency-free local execution.
            payload = {"vectors": self._vectors}
            self.index_path.write_text(json.dumps(payload), encoding="utf-8")

        payload = {
            "dim": self._dim,
            "metadata": self._metadata,
            "deleted_ids": sorted(self._deleted_ids),
        }
        self.metadata_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _load_runtime_backend(self) -> None:
        try:
            self._faiss()
            self._use_faiss = True
        except Exception:
            self._use_faiss = False

    def _load_existing(self) -> None:
        if self.metadata_path.exists():
            payload = json.loads(self.metadata_path.read_text(encoding="utf-8"))
            self._dim = payload.get("dim")
            self._metadata = payload.get("metadata", [])
            self._deleted_ids = set(payload.get("deleted_ids", []))

        if self._use_faiss:
            if self.index_path.exists():
                self._index = self._faiss().read_index(str(self.index_path))
            else:
                self._index = self._faiss().IndexFlatIP(self._dim or 1)
        else:
            if self.index_path.exists():
                payload = json.loads(self.index_path.read_text(encoding="utf-8"))
                self._vectors = payload.get("vectors", [])

    @staticmethod
    def _normalize(vector: list[float]) -> list[float]:
        norm = math.sqrt(sum(v * v for v in vector)) or 1.0
        return [float(v) / norm for v in vector]

    @staticmethod
    def _dot(left: list[float], right: list[float]) -> float:
        return float(sum(a * b for a, b in zip(left, right)))

    @staticmethod
    def _to_faiss_matrix(vectors: list[list[float]]):
        import array

        # FAISS python bindings accept numpy arrays; provide best effort conversion if numpy exists.
        try:
            import numpy as np

            matrix = np.asarray(vectors, dtype="float32")
            if matrix.ndim == 1:
                matrix = matrix.reshape(1, -1)
            return matrix
        except Exception:  # pragma: no cover - only used with FAISS installed and numpy missing
            flat = [value for row in vectors for value in row]
            return array.array("f", flat)

    @staticmethod
    def _faiss():
        import faiss  # type: ignore

        return faiss


class VectorStoreFactory:
    """Factory to support backend migration (FAISS, OpenSearch, Qdrant, etc.)."""

    @staticmethod
    def create(config: dict[str, Any]) -> BaseVectorStore:
        store_type = str(config.get("type", "faiss")).lower().strip()
        if store_type != "faiss":
            raise ValueError(f"Unsupported vectorstore type: {store_type}")
        return FaissVectorStore(
            index_path=str(config.get("index_path", "./storage/faiss.index")),
            metadata_path=str(config.get("metadata_path", "./storage/faiss_metadata.json")),
        )
