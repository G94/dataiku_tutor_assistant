"""Documentation loading and normalization interfaces."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Protocol

from dataiku_tutor.domain.models import Document


class DocumentationParser(Protocol):
    """Pluggable parser contract for HTML, Markdown, and JSON formats."""

    def parse(self, raw_content: str, source_name: str) -> Document:
        ...


class DocumentationLoader:
    """Loads raw documentation files and normalizes metadata-rich documents."""

    SUPPORTED_EXTENSIONS = {".html", ".htm", ".md", ".markdown", ".json"}

    def __init__(self, parsers: dict[str, DocumentationParser] | None = None) -> None:
        self.parsers = parsers or {}

    def load_documents(self, source_path: str) -> list[Document]:
        """Load and normalize documentation from a path into Document models."""
        root = Path(source_path)
        if not root.exists():
            return []

        files: list[Path] = []
        if root.is_file():
            files = [root]
        else:
            files = [
                path
                for path in root.rglob("*")
                if path.is_file() and path.suffix.lower() in self.SUPPORTED_EXTENSIONS
            ]
        files = sorted(files)

        documents: list[Document] = []
        for file_path in files:
            try:
                raw = file_path.read_text(encoding="utf-8", errors="ignore")
                parser = self._select_parser(file_path.suffix)
                if parser:
                    parsed = parser.parse(raw, str(file_path))
                    metadata = {"source_path": str(file_path), **parsed.metadata}
                    documents.append(
                        Document(id=parsed.id, content=parsed.content.strip(), metadata=metadata)
                    )
                    continue

                documents.append(self._parse_with_builtin(file_path=file_path, raw_content=raw))
            except Exception:
                # Skip malformed files and continue indexing; caller can add logging.
                continue

        return documents

    def _select_parser(self, extension: str) -> DocumentationParser | None:
        """Choose parser implementation by file extension."""
        return self.parsers.get(extension.lower())

    def _parse_with_builtin(self, file_path: Path, raw_content: str) -> Document:
        extension = file_path.suffix.lower()
        normalized_text = raw_content
        metadata: dict[str, str] = {
            "source_path": str(file_path),
            "file_name": file_path.name,
            "extension": extension,
        }

        if extension in {".json"}:
            try:
                payload = json.loads(raw_content)
                if isinstance(payload, dict):
                    normalized_text = self._extract_json_text(payload)
                    metadata.update(
                        {
                            "url": str(payload.get("url", "")),
                            "section": str(payload.get("section", "")),
                            "version": str(payload.get("version", "")),
                            "recipe_name": str(payload.get("recipe_name", "")),
                        }
                    )
                else:
                    normalized_text = json.dumps(payload, ensure_ascii=False)
            except json.JSONDecodeError:
                normalized_text = raw_content

        document_id = hashlib.sha1(str(file_path).encode("utf-8")).hexdigest()
        return Document(id=document_id, content=normalized_text.strip(), metadata=metadata)

    @staticmethod
    def _extract_json_text(payload: dict) -> str:
        text_candidate_keys = ["content", "text", "body", "markdown", "html"]
        for key in text_candidate_keys:
            if key in payload and isinstance(payload[key], str):
                return payload[key]

        values: list[str] = []
        for value in payload.values():
            if isinstance(value, str):
                values.append(value)
            elif isinstance(value, list):
                values.extend([v for v in value if isinstance(v, str)])
        return "\n".join(values).strip()
