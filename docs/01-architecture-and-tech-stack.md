# 01 — 技术选型与架构设计 | Architecture and Tech Stack

**状态 / Status**：[x] 草稿 Draft（已实现 MVP 对齐） | [ ] 评审中 In Review | [ ] 已定稿 Approved  
**版本 / Version**：0.2  
**对应 PRD**：Section 5 系统架构、Section 9 后续步骤

---

## 1. 技术选型 | Technology Choices

### 1.1 语言与运行时 | Language and Runtime

| 项目 | 选型 | 版本 | 备注 |
|------|------|------|------|
| 编程语言 | Python | 3.10+ | |
| 包管理 | pip | — | requirements.txt |
| 运行时 | CPython / 容器内 | — | 见 05-deployment-runbook.md |

### 1.2 Web 与 API | Web and API

| 项目 | 选型 | 版本 | 备注 |
|------|------|------|------|
| Web 框架 | FastAPI | ≥0.109 | 异步、自动 OpenAPI |
| ASGI 服务器 | Uvicorn | ≥0.27 | |
| API 文档 | OpenAPI 3.x（由 FastAPI 生成） | — | 见 `02-api-specification.yaml` |

### 1.3 Agent 与 LLM | Agent and LLM

| 项目 | 选型 | 版本 | 备注 |
|------|------|------|------|
| 编排 | 自研（app/agent/orchestrator） | — | 解析→KB→LLM→报告 |
| LLM 抽象 | LangChain ChatOpenAI / ChatOllama | langchain-openai, langchain-community | 支持 OpenAI、Ollama 切换 |
| 首批支持的 LLM | OpenAI, Ollama | — | 见 PRD 5.2.6 |

### 1.4 向量库与 RAG | Vector Store and RAG

| 项目 | 选型 | 版本 | 备注 |
|------|------|------|------|
| 向量数据库 | Chroma | ≥0.4 | 嵌入式，持久化到 CHROMA_PERSIST_DIR |
| 嵌入模型 | HuggingFaceEmbeddings（sentence-transformers） | all-MiniLM-L6-v2 等 | 可配置 EMBEDDING_MODEL |
| 切块策略 | RecursiveCharacterTextSplitter | 1024 字符，重叠 128 | 见 app/kb/service.py |

### 1.5 文档解析 | Document Parsing

| 格式 | 库/组件 | 版本 | 备注 |
|------|---------|------|------|
| PDF | PyMuPDF (fitz) | ≥1.23 | app/parser/service.py |
| Word | python-docx | ≥1.1 | |
| Excel | openpyxl | ≥3.1 | |
| PPT | python-pptx | ≥0.6 | |
| 纯文本/MD | 内置 decode | — | .txt, .md |
| 统一入口 | 自研路由（扩展名白名单） | — | parse_file() |

### 1.6 身份与集成 | Identity and Integrations

| 项目 | 选型 | 备注 |
|------|------|------|
| OAuth2/OIDC（AAD） | 占位 app/integrations | 见 docs/04-integration-guide.md |
| ServiceNow | 占位 app/integrations | 见 docs/04-integration-guide.md |
| 配置管理 | pydantic-settings + .env | app/core/config.py |

### 1.7 存储与缓存 | Storage and Cache

| 项目 | 选型 | 备注 |
|------|------|------|
| 任务状态（MVP） | 内存 dict | 生产替换为 DB/Redis |
| 向量库 | Chroma 持久化目录 | 见 CHROMA_PERSIST_DIR |
| 文件存储 | 不落盘（流式解析） | 仅解析后内容进入 KB 或 Agent |

---

## 2. 整体架构图与数据流 | Architecture and Data Flow

### 2.1 逻辑架构（与 PRD 5.1 对齐）

```
[ 接入层 ]  API (FastAPI) / Web UI / CLI
      |
[ 核心 ]  任务编排 (LangGraph/自研) ←→ 记忆体 ←→ Skill 层 ←→ 知识库 (RAG) ←→ 文件解析 (Parser)
      |
[ LLM 抽象 ]  →  OpenAI / Ollama / 千问 / Claude / ...
[ 集成 ]   AAD (登录/Token)  |  ServiceNow (项目元数据)
```

_可在此处插入更详细的框图（Mermaid 或图片路径）。_

### 2.2 组件职责与接口（简要）

| 组件 | 职责 | 对外的接口/协议 |
|------|------|------------------|
| API 层 | 认证、路由、限流、请求校验 | REST，见 02-api-specification.yaml |
| 任务编排 | 接收任务、调用 Parser/KB/Skill/LLM、写记忆、汇总结果 | 内部：调用各子组件 |
| 记忆体 | 会话/工作记忆、可选情景记忆 | 读写接口（如 get/set by session_id） |
| Skill 层 | 问卷比对、策略符合性等，见 PRD 5.2.3 | 输入/输出见 03-assessment-report-and-skill-contract.md |
| 知识库 | 多格式上传→解析→切块→向量化→检索 | 上传 API、query(chunk) API |
| 文件解析 | 多格式→统一 JSON/Markdown | parse(file) → 统一 schema，见 03 |
| LLM 抽象 | 统一 chat/completion、可选 function calling | 封装各厂商 SDK |

### 2.3 知识库切块策略 | KB Chunking Strategy

| 参数 | 取值 | 说明 |
|------|------|------|
| 块大小（字符或 token） | _填写_ | 如 512 / 1024 |
| 重叠 overlap | _填写_ | 如 0 / 64 / 128 |
| 切分方式 | 按标题/段落 / 固定长度 / 语义 | _填写_ |
| 元数据保留 | 来源文件、页码、标题层级 | _填写_ |

---

## 3. 目录/模块划分（已实现）| Module Layout (Implemented)

```
Security-AI-Agent/
├── app/
│   ├── api/                # FastAPI 路由：health, assessments, kb
│   ├── core/               # config (pydantic-settings)
│   ├── agent/              # orchestrator: run_assessment
│   ├── kb/                 # KnowledgeBaseService (Chroma + chunking)
│   ├── llm/                # get_llm, invoke_llm (OpenAI/Ollama)
│   ├── parser/             # parse_file (PDF, docx, xlsx, pptx, txt, md)
│   ├── integrations/       # 占位：AAD、ServiceNow
│   ├── models/             # assessment, parser (Pydantic)
│   └── main.py
├── docs/                   # 设计文档与 Schema
├── tests/
├── requirements.txt
└── .env.example
```

---

## 4. 依赖清单（示例）| Dependency List

在 `requirements.txt` 或 `pyproject.toml` 中维护；此处仅列出**与架构强相关**的包，版本以实际为准。

```text
# Web & API
fastapi>=0.100.0
uvicorn[standard]>=0.22.0

# Agent / LLM
langchain>=0.1.0
langchain-openai
# langgraph 如选用

# Vector & Embedding
chromadb  # 或 qdrant-client, pymilvus 等

# Document parsing
unstructured
pymupdf
python-docx
openpyxl
python-pptx

# Auth / HTTP
httpx
python-jose[cryptography]
# 其他按 1.6 选型填写
```

---

## 5. 修订记录 | Changelog

| 版本 | 日期 | 变更 |
|------|------|------|
| 0.1 | _填写_ | 初稿 |
