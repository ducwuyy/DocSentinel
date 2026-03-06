# 03 — Assessment Report and Skill Contract | 评估报告与 Skill 契约

|                 |                                            |
| :-------------- | :----------------------------------------- |
| **Status**      | [ ] Draft \| [ ] In Review \| [ ] Approved |
| **Version**     | 0.1                                        |
| **Related PRD** | Section 5.2.3 Skill, Section 6 Features    |

---

## 1. Assessment Report Schema | 评估报告结构

Agent outputs a **structured report** conforming to this schema. It is used for API responses, frontend rendering, and ServiceNow write-back.

### 1.1 JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://security-ai-agent.example/schemas/assessment-report.json",
  "title": "AssessmentReport",
  "type": "object",
  "required": ["version", "task_id", "status", "summary"],
  "properties": {
    "version": { "type": "string", "const": "1.0" },
    "task_id": { "type": "string", "format": "uuid" },
    "status": { "type": "string", "enum": ["completed", "partial", "failed"] },
    "summary": { "type": "string", "description": "Executive summary of findings" },
    "risk_items": {
      "type": "array",
      "items": { "$ref": "#/$defs/RiskItem" }
    },
    "compliance_gaps": {
      "type": "array",
      "items": { "$ref": "#/$defs/ComplianceGap" }
    },
    "remediations": {
      "type": "array",
      "items": { "$ref": "#/$defs/Remediation" }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "scenario_id": { "type": "string" },
        "project_id": { "type": "string" },
        "model_used": { "type": "string" },
        "completed_at": { "type": "string", "format": "date-time" }
      }
    },
    "format": { "type": "string", "enum": ["json", "markdown"], "default": "json" }
  },
  "$defs": {
    "RiskItem": {
      "type": "object",
      "required": ["id", "title", "severity"],
      "properties": {
        "id": { "type": "string" },
        "title": { "type": "string" },
        "severity": { "type": "string", "enum": ["low", "medium", "high", "critical"] },
        "description": { "type": "string" },
        "source_ref": { "type": "string", "description": "Reference to source doc/section" },
        "category": { "type": "string" }
      }
    },
    "ComplianceGap": {
      "type": "object",
      "required": ["id", "control_or_clause", "gap_description"],
      "properties": {
        "id": { "type": "string" },
        "control_or_clause": { "type": "string" },
        "gap_description": { "type": "string" },
        "evidence_suggestion": { "type": "string" },
        "framework": { "type": "string" }
      }
    },
    "Remediation": {
      "type": "object",
      "required": ["id", "action"],
      "properties": {
        "id": { "type": "string" },
        "action": { "type": "string" },
        "priority": { "type": "string", "enum": ["low", "medium", "high"] },
        "related_risk_ids": { "type": "array", "items": { "type": "string" } },
        "related_gap_ids": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

*Save this as `docs/schemas/assessment-report.json` for validation.*

### 1.2 Markdown Template (Optional)

When `format == "markdown"`, the output should follow:

```markdown
# Assessment Report | 安全评估报告
**Task ID**: {task_id}  
**Completed**: {completed_at}

## Summary | 摘要
{summary}

## Risk Items | 风险项
| ID  | Title | Severity | Description |
| --- | ----- | -------- | ----------- |
| ... | ...   | ...      | ...         |

## Compliance Gaps | 合规差距
| Control/Clause | Gap Description | Evidence Suggestion |
| -------------- | --------------- | ------------------- |
| ...            | ...             | ...                 |

## Remediations | 整改建议
| Priority | Action | Related Risks/Gaps |
| -------- | ------ | ------------------ |
| ...      | ...    | ...                |
```

---

## 2. Parser Output Schema | 文件解析输出结构

Unified output format for both Assessment Input and Knowledge Base Ingestion.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ParsedDocument",
  "type": "object",
  "required": ["format", "content", "metadata"],
  "properties": {
    "format": { "type": "string", "enum": ["markdown", "json"] },
    "content": {
      "oneOf": [
        { "type": "string" },
        { "type": "object", "description": "Structured content (e.g. spreadsheet rows)" }
      ]
    },
    "metadata": {
      "type": "object",
      "required": ["filename", "type"],
      "properties": {
        "filename": { "type": "string" },
        "type": { "type": "string", "description": "MIME type or extension" },
        "pages": { "type": "integer" },
        "language": { "type": "string" }
      }
    }
  }
}
```

---

## 3. Skill Contract | Skill 契约

### 3.1 General Agreement

-   **Uniform Signature**: All Skills implement the same interface invoked by the Orchestrator.
-   **Input**: `SkillInput` (context, parsed docs, KB chunks).
-   **Output**: `SkillOutput` (findings, summary).

### 3.2 SkillInput

| Field              | Type   | Required | Description                   |
| :----------------- | :----- | :------- | :---------------------------- |
| `task_id`          | string | Yes      | Unique task ID                |
| `scenario_id`      | string | No       | Assessment scenario ID        |
| `parsed_documents` | array  | Yes      | List of `ParsedDocument`      |
| `kb_chunks`        | array  | No       | Relevant RAG chunks           |
| `project_metadata` | object | No       | Metadata from ServiceNow etc. |
| `options`          | object | No       | Skill-specific config         |

### 3.3 SkillOutput

| Field           | Type    | Required | Description                                |
| :-------------- | :------ | :------- | :----------------------------------------- |
| `skill_id`      | string  | Yes      | e.g. `questionnaire_policy_check`          |
| `success`       | boolean | Yes      | Execution status                           |
| `findings`      | object  | Yes      | Subset of `AssessmentReport` (risks, gaps) |
| `summary`       | string  | No       | Summary for this specific skill            |
| `error_message` | string  | No       | If failed                                  |
| `trace`         | array   | No       | Citations or reasoning trace               |

### 3.4 Example Skill: Questionnaire vs Policy

**Skill ID**: `questionnaire_policy_check`

**Function**: Compares user-uploaded questionnaire/docs against Knowledge Base controls.

**Input**:
-   `parsed_documents`: The questionnaire (e.g. Excel converted to Markdown table).
-   `kb_chunks`: Retrieved policy clauses relevant to the questionnaire content.

**Output**:
-   `findings.compliance_gaps`: List of gaps with `evidence_suggestion`.
-   `findings.remediations`: Suggestions linked to gaps.

**Implementation Note**:
Can be implemented via LLM Prompt (Prompt + Parsed Docs + KB Chunks -> JSON) or a hybrid Rule+LLM engine.

---

## 4. Changelog | 修订记录

| Version | Date    | Changes                                                 |
| :------ | :------ | :------------------------------------------------------ |
| **0.1** | Initial | Draft Report Schema, Parser Output, and Skill Contract. |
