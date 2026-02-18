"""Executable ingestion pipeline for local indexing workflows."""

from __future__ import annotations

from dataclasses import dataclass

from dataiku_tutor.config.settings import Settings
from dataiku_tutor.embeddings.embedding_service import EmbeddingFactory
from dataiku_tutor.ingestion.chunker import DocumentationChunker
from dataiku_tutor.ingestion.loader import DocumentationLoader
from dataiku_tutor.ingestion.updater import IndexUpdater
from dataiku_tutor.vectorstore.faiss_store import VectorStoreFactory


@dataclass
class IngestionPipeline:
    """Builds and executes the indexing pipeline from YAML configuration."""

    settings: Settings

    def build_index_updater(self) -> IndexUpdater:
        ingestion_cfg = self.settings.section("ingestion")
        embedding_cfg = self.settings.section("embeddings")
        vectorstore_cfg = self.settings.section("vectorstore")

        loader = DocumentationLoader()
        chunker = DocumentationChunker(
            chunk_size=int(ingestion_cfg.get("chunk_size", 500)),
            overlap=int(ingestion_cfg.get("chunk_overlap", 100)),
        )
        embedding_service = EmbeddingFactory.create(
            provider=str(embedding_cfg.get("provider", "sentence_transformers")),
            model_name=str(embedding_cfg.get("model_name", "all-MiniLM-L6-v2")),
        )
        vector_store = VectorStoreFactory.create(vectorstore_cfg)
        return IndexUpdater(loader, chunker, embedding_service, vector_store)

    def run_full_reindex(self) -> int:
        ingestion_cfg = self.settings.section("ingestion")
        source_path = str(ingestion_cfg.get("source_path", "./data/docs"))
        updater = self.build_index_updater()
        return updater.run_full_reindex(source_path=source_path)


def run_pipeline(config_path: str = "dataiku_tutor/config/settings.yaml") -> int:
    pipeline = IngestionPipeline(settings=Settings(config_path))
    return pipeline.run_full_reindex()


if __name__ == "__main__":
    indexed = run_pipeline()
    print(f"Indexed chunks: {indexed}")
