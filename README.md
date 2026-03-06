# Arthor Agent

Automated security assessment for documents and questionnaires. This project implements **Arthor Agent** as described in the PRD: parse multi-format documents, query a policy/knowledge base, and produce structured assessment reports (risks, compliance gaps, remediations) using an LLM.

## Quick Start

```bash
# Clone or enter project
cd Arthor-Agent

# Create venv and install
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Optional: run Ollama locally for LLM (default)
# ollama serve && ollama pull llama2

# Copy env and run
cp .env.example .env
# Edit .env if needed (e.g. LLM_PROVIDER=openai and OPENAI_API_KEY=...)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **API docs**: http://localhost:8000/docs  
- **Health**: http://localhost:8000/health  
- **Submit assessment**: `POST /api/v1/assessments` with `files` (multipart) and optional `scenario_id`, `project_id`.  
- **Get result**: `GET /api/v1/assessments/{task_id}`  
- **Upload to KB**: `POST /api/v1/kb/documents` with `file`.  
- **Query KB**: `POST /api/v1/kb/query` with body `{"query": "...", "top_k": 5}`.

## Project Layout

- **app/** — FastAPI app, API routes, agent orchestration, KB, LLM, parser, models.  
- **docs/** — Design and specification (architecture, API, report schema, integration, deployment).  
- **PRD** — Product requirements: see [Arthor-Agent-PRD.md](./Arthor-Agent-PRD.md) in the repo root.

## Configuration

See `.env.example` and **docs/05-deployment-runbook.md**. Key settings:

- `LLM_PROVIDER`: `ollama` (default) or `openai`  
- `OLLAMA_BASE_URL`, `OLLAMA_MODEL` or `OPENAI_API_KEY`, `OPENAI_MODEL`  
- `CHROMA_PERSIST_DIR` — where the knowledge base is stored  
- `UPLOAD_MAX_FILE_SIZE_MB`, `UPLOAD_MAX_FILES` — limits (PRD §7.2)

## Security

See **SECURITY.md** for vulnerability reporting and security-related configuration. Security requirements and controls are defined in **PRD §7.2**.

## License

TBD (see PRD and CONTRIBUTING when open-sourcing).
