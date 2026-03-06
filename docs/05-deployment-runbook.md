# 05 — 部署与运行手册 | Deployment and Runbook

**状态 / Status**：[ ] 草稿 Draft | [ ] 评审中 In Review | [ ] 已定稿 Approved  
**版本 / Version**：0.1  
**对应 PRD**：Section 7 非功能需求（部署与连通性、安全与隐私）

---

## 1. 环境要求 | Environment Requirements

### 1.1 运行时

| 项目 | 要求 |
|------|------|
| Python | _填写，建议 3.10+_ |
| 操作系统 | Linux（推荐）/ Windows Server / 容器镜像基础 _填写_ |
| 内存 | _填写，如：最低 4GB，推荐 8GB+_ |
| CPU | _填写_ |
| 磁盘 | _填写，用于上传文件、向量库、日志_ |

### 1.2 依赖服务（按实际选型填写）

| 服务 | 用途 | 是否必须 |
|------|------|----------|
| 向量库（Chroma/Qdrant/…）| 知识库检索 | 是 |
| Redis | 会话/缓存/记忆体 | 可选 |
| PostgreSQL / SQLite | 任务、用户、审计 | 按 01 架构确定 |
| AAD（微软登录）| 身份与 SSO | 生产推荐 |
| ServiceNow | 项目元数据、可选回写 | 可选 |
| LLM 端点 | OpenAI / Ollama / 千问 / Claude 等 | 是 |

---

## 2. 部署方式 | Deployment Options

### 2.1 本地 / 单机

```bash
# 示例：克隆/进入项目后
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # 编辑 .env 填入配置
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

- **适用**：开发、PoC、小团队内网。
- **注意**：向量库、DB 若为嵌入式（如 Chroma、SQLite），数据目录需持久化。

### 2.2 Docker（示例）

_Dockerfile 与 docker-compose 以项目实际为准；此处仅作模板。_

```dockerfile
# Dockerfile 示例
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml 示例（片段）
services:
  agent:
    build: .
    ports: ["8000:8000"]
    env_file: .env
    volumes: ["./data:/app/data"]
    depends_on: [redis]
  redis:
    image: redis:7-alpine
    volumes: ["redis_data:/data"]
volumes:
  redis_data:
```

### 2.3 内网 / 私有化

- 部署于客户内网，**不访问公网**时：
  - LLM 需使用**本地或内网可用**的模型（如 Ollama、内网部署的 vLLM）。
  - AAD 若不可达，可关闭 SSO，改用本地账号或内网 IdP（在 04 中说明）。
  - ServiceNow 一般为内网或 VPN 可达，按 04 配置实例 URL 与认证。

---

## 3. 配置项清单 | Configuration Reference

以下为**建议**的配置项名称与说明；最终以代码与 01 架构为准。

### 3.1 应用与 API

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `ENV` | 环境 | development / staging / production |
| `LOG_LEVEL` | 日志级别 | INFO |
| `API_PREFIX` | API 路径前缀 | /api/v1 |
| `SECRET_KEY` | 会话/签名密钥 | _随机字符串_ |
| `ALLOWED_ORIGINS` | CORS 允许来源 | https://your-frontend.example.com |

### 3.2 认证（AAD）

| 变量名 | 说明 | 见 04-integration-guide |
|--------|------|-------------------------|
| `AAD_TENANT_ID` | 租户 ID | |
| `AAD_CLIENT_ID` | 应用（客户端）ID | |
| `AAD_CLIENT_SECRET` | 客户端密钥 | |
| `AAD_REDIRECT_URI` | 回调 URI | |
| `OIDC_ISSUER` / `OIDC_JWKS_URI` | OIDC 发现 | |

### 3.3 LLM

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `LLM_PROVIDER` | 当前使用的后端 | openai / ollama / qwen / claude |
| `OPENAI_API_KEY` | OpenAI API Key | sk-… |
| `OPENAI_BASE_URL` | 可选，自建或代理 base URL | |
| `OLLAMA_BASE_URL` | Ollama 服务地址 | http://localhost:11434 |
| `OLLAMA_MODEL` | 模型名 | llama2 / … |

### 3.4 向量库 / 知识库

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `VECTOR_STORE_TYPE` | chroma / qdrant / … | chroma |
| `CHROMA_PERSIST_DIR` | Chroma 持久化目录 | ./data/chroma |
| `EMBEDDING_MODEL` | 嵌入模型名或路径 | |

### 3.5 文件与解析

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `UPLOAD_MAX_FILE_SIZE_MB` | 单文件大小上限（MB）| 50 |
| `UPLOAD_MAX_FILES` | 单次请求最大文件数 | 10 |
| `PARSER_TIMEOUT_SECONDS` | 单文件解析超时 | 120 |

### 3.6 ServiceNow（可选）

| 变量名 | 说明 | 见 04-integration-guide |
|--------|------|-------------------------|
| `SERVICENOW_INSTANCE` | 实例 URL | |
| `SERVICENOW_USERNAME` / `SERVICENOW_PASSWORD` | 或 OAuth/API Key | |

### 3.7 网络与防火墙（汇总）

| 目标 | 用途 | 方向 |
|------|------|------|
| AAD | 登录、Token 校验 | 本系统 → login.microsoftonline.com |
| ServiceNow | 项目元数据、回写 | 本系统 → &lt;instance&gt;.service-now.com |
| LLM 提供商 | 调用模型 | 本系统 → 各厂商 API 或内网 Ollama |
| 向量库/Redis/DB | 若为远程服务 | 本系统 → 内网或自建服务 |

_部署前与客户/运维确认上述域名或 IP 已放行。_

---

## 4. 运维与监控 | Operations and Monitoring

### 4.1 健康检查

- **HTTP**：`GET /health` 返回 200 表示服务存活。
- **依赖**：可选 `GET /health/ready` 检查 DB、向量库、LLM 可达性（若实现）。

### 4.2 日志

- **位置**：_填写，如：stdout + 文件 / 集中日志_。
- **内容**：请求 ID、用户/角色、任务 ID、模型调用耗时、错误栈；**避免记录敏感文档内容或完整 Token**。

### 4.3 审计

- **范围**：谁在何时发起了哪次评估、访问了哪些项目/报告（见 PRD 7 安全与隐私）。
- **存储**：_填写，如：审计表或独立日志_。
- **保留期**：_按合规要求填写_。

### 4.4 备份与恢复

| 对象 | 建议 |
|------|------|
| 向量库数据 | 定期备份 Chroma/Qdrant 数据目录或快照 |
| 关系型数据 | 按 DB 常规备份策略 |
| 上传文件 | 按策略决定是否长期保留及备份 |

---

## 5. 常见问题与排错 | Troubleshooting

| 现象 | 可能原因 | 处理建议 |
|------|----------|----------|
| 登录一直重定向或 401 | AAD 配置错误、回调 URI 不匹配、网络不通 | 核对 04 中 AAD 配置与重定向 URI；检查本机到 login.microsoftonline.com 连通性 |
| 评估任务一直 pending | 队列阻塞、LLM 超时、解析失败 | 查应用日志与任务状态；检查 LLM 端点与解析器日志 |
| 知识库检索无结果 | 向量库未就绪、集合名错误、嵌入模型不一致 | 确认向量库已写入且 query 使用相同 embedding 模型与集合 |
| ServiceNow 拉取项目失败 | 实例 URL、认证、权限或网络 | 按 04 核对实例与认证；用 curl 测试 REST API |

---

## 6. 修订记录 | Changelog

| 版本 | 日期 | 变更 |
|------|------|------|
| 0.1 | _填写_ | 初稿：环境、部署方式、配置项、运维要点 |
