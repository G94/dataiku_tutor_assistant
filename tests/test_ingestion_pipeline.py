import tempfile
import unittest
from pathlib import Path

from dataiku_tutor.embeddings.embedding_service import SentenceTransformerEmbeddingService
from dataiku_tutor.ingestion.chunker import DocumentationChunker
from dataiku_tutor.ingestion.loader import DocumentationLoader
from dataiku_tutor.ingestion.updater import IndexUpdater
from dataiku_tutor.vectorstore.faiss_store import FaissVectorStore


class IngestionPipelineTests(unittest.TestCase):
    def test_loader_chunker_updater_builds_local_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            docs_path = tmp_path / "docs"
            docs_path.mkdir()
            (docs_path / "recipe.md").write_text(
                "# Group recipe\nOpen your dataset and add a group recipe to aggregate values.",
                encoding="utf-8",
            )
            (docs_path / "join.json").write_text(
                '{"url": "https://doc", "section": "recipes", "content": "Create a join recipe from flow."}',
                encoding="utf-8",
            )

            loader = DocumentationLoader()
            chunker = DocumentationChunker(chunk_size=8, overlap=2)
            embedding_service = SentenceTransformerEmbeddingService("all-MiniLM-L6-v2")
            vector_store = FaissVectorStore(
                index_path=str(tmp_path / "faiss.index"),
                metadata_path=str(tmp_path / "faiss_metadata.json"),
            )

            updater = IndexUpdater(loader, chunker, embedding_service, vector_store)
            indexed = updater.run_full_reindex(str(docs_path))

            self.assertGreater(indexed, 0)
            self.assertTrue((tmp_path / "faiss.index").exists())
            self.assertTrue((tmp_path / "faiss_metadata.json").exists())

            query_vector = embedding_service.embed(["How do I create a group recipe?"])[0]
            results = vector_store.search(query_vector, k=3)
            self.assertGreater(len(results), 0)
            self.assertTrue(any(result.chunk.content for result in results))


if __name__ == "__main__":
    unittest.main()
