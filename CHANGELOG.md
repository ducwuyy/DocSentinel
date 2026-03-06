# Changelog

All notable changes to Arthor Agent are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [Unreleased]

- (Add new changes here before cutting a release.)

---

## [0.1.0] — 2025-03-07

### Added

- **Assessment API**: Submit documents (PDF, Word, Excel, PPT, text) and receive structured assessment reports (risk items, compliance gaps, remediations).
- **Knowledge base (RAG)**: Upload policy/compliance documents; chunking and embedding with Chroma; query endpoint for retrieval.
- **Multi-format parser**: PyMuPDF (PDF), python-docx (Word), openpyxl (Excel), python-pptx (PPT), plain text/Markdown.
- **LLM abstraction**: Support for OpenAI and Ollama (local); configurable via `LLM_PROVIDER` and env vars.
- **REST API**: FastAPI app with `/api/v1/assessments`, `/api/v1/kb/documents`, `/api/v1/kb/query`, `/health`; Swagger at `/docs`.
- **Docker**: `Dockerfile` and `docker-compose.yml` for one-command run with optional Ollama service.
- **Documentation**: SPEC, ARCHITECTURE.md, design docs (01–05), SECURITY.md, README with Quick Start.

### Notes

- Task store is in-memory (MVP); replace with DB/Redis for production.
- AAD and ServiceNow integrations are planned; see SPEC and docs/04-integration-guide.md.

[Unreleased]: https://github.com/arthurpanhku/Arthor-Agent/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/arthurpanhku/Arthor-Agent/releases/tag/v0.1.0
