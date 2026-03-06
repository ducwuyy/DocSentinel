"""
Parsed document model.
Aligned with docs/03-assessment-report-and-skill-contract.md §2 Parser Output Schema.
"""
from typing import Any

from pydantic import BaseModel, Field


class ParsedDocumentMetadata(BaseModel):
    filename: str
    type: str  # MIME or extension
    pages: int | None = None
    language: str | None = None


class ParsedDocument(BaseModel):
    """Unified output from document parser for assessment and KB ingestion."""

    format: str = "markdown"  # "markdown" | "json"
    content: str | dict[str, Any] = Field(..., description="Extracted text or structured content")
    metadata: ParsedDocumentMetadata
