# Changelog

All notable changes to Arthor Agent are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.2.0] — 2026-03-06

### Added
- **Streamlit Frontend**: A modern, interactive dashboard for managing assessments and knowledge base.
  - **Dashboard**: Visual metrics and activity charts.
  - **Assessment Workbench**: Drag-and-drop file upload, real-time progress tracking, and structured report viewing (Risks, Compliance, Remediations).
  - **Knowledge Base Manager**: UI for uploading policy documents and testing RAG retrieval.
- **Developer Experience**:
  - Added `pyproject.toml` for unified tool configuration.
  - Added `Makefile` for common development tasks (`make install`, `make test`, `make lint`).
  - Added `pre-commit` hooks for code quality assurance.
  - Integrated **Ruff** for fast linting and formatting.
- **Documentation**:
  - Updated README with frontend screenshots and demo GIF.
  - Added `DEMO-RECORD.md` guide.

### Changed
- **CI/CD**: Updated GitHub Actions workflow to include linting steps.
- **Project Structure**: Migrated `pytest.ini` to `pyproject.toml`.

[0.2.0]: https://github.com/arthurpanhku/Arthor-Agent/releases/tag/v0.2.0
[0.1.0]: https://github.com/arthurpanhku/Arthor-Agent/releases/tag/v0.1.0
