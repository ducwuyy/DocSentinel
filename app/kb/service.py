"""
Knowledge base: chunk, embed, store in Chroma; RAG query.
PRD §5.2.4; docs/01 — Chroma, sentence-transformers for embedding.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.models.parser import ParsedDocument


def _get_embeddings():
    if not hasattr(_get_embeddings, "_emb"):
        _get_embeddings._emb = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
        )
    return _get_embeddings._emb


class KnowledgeBaseService:
    """Single collection for MVP; persist to CHROMA_PERSIST_DIR."""

    CHUNK_SIZE = 1024
    CHUNK_OVERLAP = 128
    COLLECTION_NAME = "security_agent_kb"

    def __init__(self) -> None:
        persist_dir = Path(settings.CHROMA_PERSIST_DIR)
        persist_dir.mkdir(parents=True, exist_ok=True)
        self._vectorstore = Chroma(
            collection_name=self.COLLECTION_NAME,
            embedding_function=_get_embeddings(),
            persist_directory=str(persist_dir),
        )
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.CHUNK_SIZE,
            chunk_overlap=self.CHUNK_OVERLAP,
            separators=["\n\n", "\n", "。", " ", ""],
        )

    def add_document(self, parsed: ParsedDocument, document_id: str | None = None) -> str:
        """Ingest one parsed document into the KB; return document id."""
        content = parsed.content if isinstance(parsed.content, str) else str(parsed.content)
        doc_id = document_id or hashlib.sha256(content.encode()).hexdigest()[:16]
        chunks = self._splitter.split_text(content)
        if not chunks:
            return doc_id
        docs = [
            Document(
                page_content=c,
                metadata={
                    "source": parsed.metadata.filename,
                    "document_id": doc_id,
                    "type": parsed.metadata.type,
                },
            )
            for c in chunks
        ]
        self._vectorstore.add_documents(docs, ids=[f"{doc_id}_{i}" for i in range(len(docs))])
        return doc_id

    def query(self, query: str, top_k: int = 5) -> list[Document]:
        """RAG: return top_k relevant chunks."""
        return self._vectorstore.similarity_search(query, k=top_k)
