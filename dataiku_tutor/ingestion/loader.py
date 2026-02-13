"""Documentation loading and normalization interfaces."""

from typing import Protocol

from dataiku_tutor.domain.models import Document


class DocumentationParser(Protocol):
    """Pluggable parser contract for HTML, Markdown, and JSON formats."""

    def parse(self, raw_content: str, source_name: str) -> Document:
        ...


class DocumentationLoader:
    """Loads raw documentation files and normalizes metadata-rich documents."""

    def __init__(self, parsers: dict[str, DocumentationParser]) -> None:
        self.parsers = parsers

    def load_documents(self, source_path: str) -> list[Document]:
        """Load and normalize documentation from a path into Document models."""
        raise NotImplementedError

    def _select_parser(self, extension: str) -> DocumentationParser:
        """Choose parser implementation by file extension."""
        raise NotImplementedError
