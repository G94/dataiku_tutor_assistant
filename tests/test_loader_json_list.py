import json
import tempfile
import unittest
from pathlib import Path

from dataiku_tutor.ingestion.loader import DocumentationLoader


class DocumentationLoaderJsonListTests(unittest.TestCase):
    def test_load_documents_from_single_json_list_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            source_file = Path(tmp) / "docs.json"
            source_file.write_text(
                json.dumps(
                    [
                        {
                            "id": "doc-1",
                            "url": "https://doc.dataiku.com/page-1",
                            "title": "Title 1",
                            "content": "First page content",
                            "topic": "preparation",
                            "subtopic": "processors",
                            "page_name": "page-1.html",
                        },
                        {
                            "id": "doc-2",
                            "url": "https://doc.dataiku.com/page-2",
                            "title": "Title 2",
                            "content": "Second page content",
                            "topic": "ml",
                            "subtopic": "models",
                            "page_name": "page-2.html",
                        },
                    ]
                ),
                encoding="utf-8",
            )

            loader = DocumentationLoader()
            documents = loader.load_documents(str(source_file))

            self.assertEqual(len(documents), 2)
            self.assertEqual(documents[0].id, "doc-1")
            self.assertEqual(documents[0].metadata["topic"], "preparation")
            self.assertEqual(documents[0].metadata["subtopic"], "processors")
            self.assertEqual(documents[0].metadata["page_name"], "page-1.html")
            self.assertEqual(documents[0].metadata["title"], "Title 1")
            self.assertEqual(documents[1].id, "doc-2")
            self.assertEqual(documents[1].metadata["topic"], "ml")


if __name__ == "__main__":
    unittest.main()
