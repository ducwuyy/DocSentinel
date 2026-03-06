"""
Agent orchestration: parse docs, query KB, invoke Skill, call LLM, produce report.
PRD §5.2.1; docs/03 — Assessment report schema and Skill contract.
"""
from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from app.core.config import settings
from app.kb.service import KnowledgeBaseService
from app.llm.base import invoke_llm
from app.models.assessment import (
    AssessmentReport,
    ComplianceGap,
    ReportMetadata,
    Remediation,
    RiskItem,
)
from app.models.parser import ParsedDocument


async def run_assessment(
    task_id: UUID,
    parsed_documents: list[ParsedDocument],
    scenario_id: str | None = None,
    project_id: str | None = None,
) -> AssessmentReport:
    """
    Run the assessment pipeline: RAG retrieval + LLM-based Skill -> report.
    """
    # 1) Build context from parsed documents
    doc_texts = []
    for d in parsed_documents:
        c = d.content if isinstance(d.content, str) else str(d.content)
        doc_texts.append(f"[{d.metadata.filename}]\n{c}")
    combined_input = "\n\n---\n\n".join(doc_texts)

    # 2) Retrieve relevant KB chunks (if any)
    kb = KnowledgeBaseService()
    try:
        chunks = kb.query(combined_input[:2000], top_k=5)  # query from start of content
        kb_context = "\n\n".join(d.page_content for d in chunks) if chunks else "No policy documents loaded."
    except Exception:
        kb_context = "Knowledge base not available or empty."

    # 3) Invoke LLM to produce structured assessment (single Skill: policy/questionnaire check)
    system_prompt = """You are a security assessor. Given document content and optional policy/knowledge base excerpts, identify:
1. Risk items (id, title, severity: low/medium/high/critical, description, source_ref if possible)
2. Compliance gaps (id, control_or_clause, gap_description, evidence_suggestion)
3. Remediations (id, action, priority: low/medium/high, related_risk_ids or related_gap_ids if applicable)

Respond in JSON only, with keys: summary (string), risk_items (array), compliance_gaps (array), remediations (array). Use the exact field names. If none, use empty arrays."""

    user_prompt = f"""## Documents to assess\n\n{combined_input[:12000]}\n\n## Reference (policy/KB excerpts)\n\n{kb_context[:4000]}\n\nProduce the assessment JSON."""

    try:
        raw = await invoke_llm(system_prompt, user_prompt)
    except Exception as e:
        return AssessmentReport(
            task_id=str(task_id),
            status="failed",
            summary=f"LLM invocation failed: {e!s}",
            metadata=ReportMetadata(
                scenario_id=scenario_id,
                project_id=project_id,
                model_used=settings.LLM_PROVIDER,
                completed_at=datetime.now(timezone.utc),
            ),
        )

    # 4) Parse LLM output into report (best-effort)
    report = _parse_llm_output_to_report(raw, task_id, scenario_id, project_id)
    return report


def _parse_llm_output_to_report(
    raw: str,
    task_id: UUID,
    scenario_id: str | None,
    project_id: str | None,
) -> AssessmentReport:
    """Extract JSON from LLM response and map to AssessmentReport."""
    import json
    import re

    risk_items: list[RiskItem] = []
    compliance_gaps: list[ComplianceGap] = []
    remediations: list[Remediation] = []
    summary = "Assessment completed."

    # Try to find JSON block
    json_match = re.search(r"\{[\s\S]*\}", raw)
    if json_match:
        try:
            data = json.loads(json_match.group(0))
            summary = data.get("summary") or summary
            for i, r in enumerate(data.get("risk_items") or []):
                risk_items.append(
                    RiskItem(
                        id=r.get("id") or f"risk-{i}",
                        title=r.get("title") or "Unnamed risk",
                        severity=r.get("severity") or "medium",
                        description=r.get("description"),
                        source_ref=r.get("source_ref"),
                        category=r.get("category"),
                    )
                )
            for i, g in enumerate(data.get("compliance_gaps") or []):
                compliance_gaps.append(
                    ComplianceGap(
                        id=g.get("id") or f"gap-{i}",
                        control_or_clause=g.get("control_or_clause") or "",
                        gap_description=g.get("gap_description") or "",
                        evidence_suggestion=g.get("evidence_suggestion"),
                        framework=g.get("framework"),
                    )
                )
            for i, rem in enumerate(data.get("remediations") or []):
                remediations.append(
                    Remediation(
                        id=rem.get("id") or f"rem-{i}",
                        action=rem.get("action") or "",
                        priority=rem.get("priority"),
                        related_risk_ids=rem.get("related_risk_ids") or [],
                        related_gap_ids=rem.get("related_gap_ids") or [],
                    )
                )
        except (json.JSONDecodeError, KeyError, TypeError):
            summary = "Assessment completed with partial parsing; raw output may contain more."

    return AssessmentReport(
        version="1.0",
        task_id=str(task_id),
        status="completed",
        summary=summary,
        risk_items=risk_items,
        compliance_gaps=compliance_gaps,
        remediations=remediations,
        metadata=ReportMetadata(
            scenario_id=scenario_id,
            project_id=project_id,
            model_used=settings.LLM_PROVIDER,
            completed_at=datetime.now(timezone.utc),
        ),
        format="json",
    )
