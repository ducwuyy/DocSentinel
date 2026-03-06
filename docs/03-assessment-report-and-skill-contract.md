# 03 — 评估报告与 Skill 契约 | Assessment Report and Skill Contract

**状态 / Status**：[ ] 草稿 Draft | [ ] 评审中 In Review | [ ] 已定稿 Approved  
**版本 / Version**：0.1  
**对应 PRD**：Section 5.2.3 Skill、Section 6 功能范围；API 响应体与 02-api-specification.yaml 一致

---

## 1. 评估报告结构 | Assessment Report Schema

Agent 完成评估后输出的**结构化报告**应与此 schema 一致，便于 API 返回、前端展示与回写 ServiceNow。

### 1.1 JSON Schema（可抽为独立 .json 文件供校验）

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
    "summary": { "type": "string", "description": "评估结论摘要" },
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
        "source_ref": { "type": "string", "description": "来源文档/段落引用" },
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

_可将上述内容保存为 `docs/schemas/assessment-report.json`，在 CI 或运行时做校验。_

### 1.2 Markdown 报告模板（可选）

当 `format == "markdown"` 时，可同时提供人类可读的 Markdown，结构建议如下：

```markdown
# 安全评估报告 | Assessment Report
**任务 ID**：{task_id}  
**完成时间**：{completed_at}

## 摘要
{summary}

## 风险项 | Risk Items
| ID | 标题 | 严重程度 | 描述 |
|----|------|----------|------|
| ... | ... | ... | ... |

## 合规差距 | Compliance Gaps
| 控制/条款 | 差距描述 | 证据建议 |
|------------|----------|----------|
| ... | ... | ... |

## 整改建议 | Remediations
| 优先级 | 建议措施 | 关联风险/差距 |
|--------|----------|----------------|
| ... | ... | ... |
```

---

## 2. 文件解析器输出 Schema | Parser Output Schema

评估输入文件与知识库上传文件经 Parser 后的**统一输出**，供 Agent 与 KB 入库消费。

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
        { "type": "object", "description": "结构化内容（如表格）" }
      ]
    },
    "metadata": {
      "type": "object",
      "required": ["filename", "type"],
      "properties": {
        "filename": { "type": "string" },
        "type": { "type": "string", "description": "MIME 或扩展名，如 application/pdf" },
        "pages": { "type": "integer" },
        "language": { "type": "string" }
      }
    }
  }
}
```

---

## 3. Skill 契约 | Skill Contract

### 3.1 通用约定

- 每个 Skill 实现**统一调用签名**（由编排层约定）：
  - **输入**：`SkillInput`（见下），包含任务上下文、已解析文档、可选知识库检索结果。
  - **输出**：`SkillOutput`（见下），包含结论、结构化发现（风险/差距/建议）、可选置信度或溯源。
- 编排层负责组装 `SkillInput`、调用 Skill、将多个 Skill 输出聚合为最终报告。

### 3.2 SkillInput（建议）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_id` | string | 是 | 评估任务 ID |
| `scenario_id` | string | 否 | 评估场景 ID |
| `parsed_documents` | array of ParsedDocument | 是 | 已解析的文档列表（见上） |
| `kb_chunks` | array | 否 | 知识库检索到的相关片段 |
| `project_metadata` | object | 否 | 来自 ServiceNow 等的项目元数据 |
| `options` | object | 否 | Skill 特定参数（如 strict_mode） |

### 3.3 SkillOutput（建议）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `skill_id` | string | 是 | 如 questionnaire_policy_check |
| `success` | boolean | 是 | 是否成功执行 |
| `findings` | object | 是 | 包含 risk_items / compliance_gaps / remediations 的子集或全部 |
| `summary` | string | 否 | 本 Skill 的结论摘要 |
| `error_message` | string | 否 | 失败时错误信息 |
| `trace` | array | 否 | 可选溯源（引用的 chunk、条款等） |

### 3.4 首个 Skill 示例：问卷与策略比对 | Example Skill — Questionnaire vs Policy

**Skill ID**：`questionnaire_policy_check`

**功能**：对比用户提交的问卷/文档内容与知识库中的控制要求，输出合规差距与证据建议。

**输入**：使用通用 `SkillInput`；`parsed_documents` 中应包含问卷类文档（如 Excel/Word 转成的 Markdown 或 JSON 表格）；`kb_chunks` 为与「控制要求」「策略条款」相关的检索结果。

**输出**：使用通用 `SkillOutput`；`findings` 中至少包含：
- `compliance_gaps`：每条含 control_or_clause、gap_description、evidence_suggestion
- `remediations`：可选的整改建议，并可通过 related_gap_ids 关联

**实现备注**：可由 LLM 根据 prompt + parsed_documents + kb_chunks 生成；或规则引擎 + LLM 混合（规则做匹配，LLM 做表述与建议）。

---

## 4. 修订记录 | Changelog

| 版本 | 日期 | 变更 |
|------|------|------|
| 0.1 | _填写_ | 初稿：报告 Schema、Parser 输出、Skill 契约 |
