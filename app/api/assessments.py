"""
Assessment API: submit task, get result.
PRD §6; docs/02-api-specification.yaml.
"""
from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.agent.orchestrator import run_assessment
from app.models.assessment import AssessmentTaskCreated, AssessmentTaskResult
from app.parser import parse_file

router = APIRouter(prefix="/assessments", tags=["assessment"])

# In-memory task store for MVP (replace with DB/Redis later)
_tasks: dict[str, dict] = {}


@router.post("", response_model=AssessmentTaskCreated)
async def submit_assessment(
    files: list[UploadFile] = File(..., description="Documents to assess"),
    scenario_id: str | None = Form(None),
    project_id: str | None = Form(None),
):
    """Submit an assessment task; returns task_id for polling."""
    from app.core.config import settings

    if len(files) > settings.UPLOAD_MAX_FILES:
        raise HTTPException(413, f"Max {settings.UPLOAD_MAX_FILES} files allowed")
    if not files:
        raise HTTPException(400, "At least one file required")

    task_id = uuid4()
    parsed_list = []
    for f in files:
        content = await f.read()
        if len(content) > settings.upload_max_bytes:
            raise HTTPException(413, f"File {f.filename} exceeds {settings.UPLOAD_MAX_FILE_SIZE_MB}MB")
        try:
            parsed = parse_file(content, f.filename or "unknown")
            parsed_list.append(parsed)
        except ValueError as e:
            raise HTTPException(400, str(e))

    created_at = datetime.now(timezone.utc)
    _tasks[str(task_id)] = {
        "status": "running",
        "report": None,
        "error": None,
        "created_at": created_at,
        "completed_at": None,
    }

    # Run assessment (blocking in async - for MVP; use background task in production)
    try:
        report = await run_assessment(task_id, parsed_list, scenario_id=scenario_id, project_id=project_id)
        _tasks[str(task_id)]["status"] = "completed"
        _tasks[str(task_id)]["report"] = report.model_dump()
        _tasks[str(task_id)]["completed_at"] = datetime.now(timezone.utc)
    except Exception as e:
        _tasks[str(task_id)]["status"] = "failed"
        _tasks[str(task_id)]["error"] = str(e)
        _tasks[str(task_id)]["completed_at"] = datetime.now(timezone.utc)

    return AssessmentTaskCreated(
        task_id=task_id,
        status="accepted",
        message="Assessment task created. Use GET /assessments/{task_id} to retrieve the result.",
    )


@router.get("/{task_id}", response_model=AssessmentTaskResult)
async def get_assessment(task_id: str):
    """Get assessment task status and report."""
    if task_id not in _tasks:
        raise HTTPException(404, "Task not found")
    t = _tasks[task_id]
    from app.models.assessment import AssessmentReport

    report = None
    if t.get("report"):
        report = AssessmentReport(**t["report"])
    return AssessmentTaskResult(
        task_id=UUID(task_id),
        status=t["status"],
        report=report,
        error_message=t.get("error"),
        created_at=t["created_at"],
        completed_at=t.get("completed_at"),
    )
