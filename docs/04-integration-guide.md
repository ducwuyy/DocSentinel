# 04 — 集成指南 | Integration Guide

**状态 / Status**：[ ] 草稿 Draft | [ ] 评审中 In Review | [ ] 已定稿 Approved  
**版本 / Version**：0.1  
**对应 PRD**：Section 5.2.7 企业集成、5.2.8 IAM；Section 7 部署与连通性

---

## 1. Azure AD（AAD / Entra ID）| Identity Provider

### 1.1 应用注册与配置

| 步骤 | 说明 | 填写/链接 |
|------|------|-----------|
| 1. 在 Azure 门户创建应用注册 | 租户：_填写租户 ID 或名称_ | [Azure Portal → App registrations](https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade) |
| 2. 应用（客户端）ID | 复制到本系统配置 | `AZURE_CLIENT_ID` = _填写_ |
| 3. 客户端密钥 / 证书 | 若使用 client_secret；生产建议证书 | `AZURE_CLIENT_SECRET` = _占位，勿提交代码库_ |
| 4. 重定向 URI | Web：`https://<本系统域名>/auth/callback` | _填写本系统实际 URL_ |
| 5. API 权限 (Scopes) | 至少：OpenID、email、profile；如需组：Group.Read.All 等 | _列出本系统实际申请的 scope_ |
| 6. 颁发 IDP 元数据 URL | 用于 OIDC 发现 | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` |

### 1.2 环境变量 / 配置项（示例）

```bash
# AAD / OIDC
AAD_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AAD_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AAD_CLIENT_SECRET=********
AAD_REDIRECT_URI=https://your-agent.example.com/auth/callback
OIDC_ISSUER=https://login.microsoftonline.com/{tenant_id}/v2.0
OIDC_JWKS_URI=https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys
```

### 1.3 网络与防火墙

- 本系统需能**出站**访问：`login.microsoftonline.com`、`*.login.microsoftonline.com`（OIDC、Token）。
- 若部署在内网，确认代理或防火墙放行上述域名。

### 1.4 可选：组与角色映射

| 配置项 | 说明 |
|--------|------|
| AAD 组 → 本系统角色 | 如：安全组 `Security-Agent-Analysts` 映射为 `security_analyst`；在配置或代码中维护映射表。 |
| 声明 (Claims) | 使用 `groups` 或 `roles` claim 做 RBAC；需在应用注册中配置可选声明。 |

---

## 2. ServiceNow（项目管理平台）| Project Management Platform

### 2.1 目标表 / API（与 PRD「项目元数据」对齐）

| 用途 | 表或 API | 说明 |
|------|----------|------|
| 项目主数据 | _填写，如：pm_project / Project API_ | 项目 ID、名称、类型、状态、所属部门 |
| 项目类型 / 合规范围 | _填写，如：自定义字段或关联表_ | 用于选择评估场景、过滤知识库 |
| 客户/合同 | _填写，如：客户表或合同表_ | 可选，用于场景或权限 |
| 工单（回写评估结果）| _填写，如：incident / task / 变更请求_ | 可选，评估结果或链接回写 |

_以上需与运维/项目管理方确认实例版本与可用 API。_

### 2.2 字段映射（项目元数据 → 本系统）

| 本系统字段（内部使用）| ServiceNow 来源 | 备注 |
|------------------------|-----------------|------|
| `project_id` | _填写，如：pm_project.sys_id_ | 唯一标识 |
| `project_name` | _填写_ | |
| `project_type` | _填写，如：u_project_type_ | 用于评估场景选择 |
| `compliance_scope` | _填写，如：u_compliance_framework_ | 合规框架标签 |
| `department` / `owner` | _填写_ | 可选，用于权限或展示 |

### 2.3 认证方式

| 方式 | 说明 |
|------|------|
| Basic Auth | 用户名 + 密码（不推荐生产长期使用）|
| OAuth 2.0 | 若 ServiceNow 实例支持，推荐 |
| API Key / Token | 若实例支持，填写获取方式与配置项名 |

_本系统配置项示例：_

```bash
SERVICENOW_INSTANCE=https://your-instance.service-now.com
SERVICENOW_USERNAME=integration_user
SERVICENOW_PASSWORD=********
# 或 SERVICENOW_OAUTH_* / SERVICENOW_API_KEY
```

### 2.4 网络与防火墙

- 本系统需能**出站**访问：`<SERVICENOW_INSTANCE>`（REST API）。
- 若本系统与 ServiceNow 不在同一网段，确认防火墙/代理放行。

### 2.5 可选：回写评估结果

- **目标**：将评估报告链接或摘要写入 ServiceNow 工单/任务。
- **表/API**：_填写，如：PATCH /api/now/table/task/{sys_id}_。
- **字段**：_填写，如：work_notes、u_assessment_report_url、u_assessment_summary_。
- **触发时机**：评估任务状态变为 `completed` 且请求中带有 `project_id` / `ticket_id` 时。

---

## 3. 其他 IdP（可选）| Other Identity Providers

若后续支持 Okta、Google Workspace 等，可在此追加小节，结构同上：

- 应用/客户端配置
- 环境变量与 OIDC 端点
- 组/角色映射（若适用）

---

## 4. 修订记录 | Changelog

| 版本 | 日期 | 变更 |
|------|------|------|
| 0.1 | _填写_ | 初稿：AAD、ServiceNow 模板 |
