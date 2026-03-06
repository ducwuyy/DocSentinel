# Security Policy | 安全策略

This document covers vulnerability disclosure and security-related practices for the **Arthor Agent** project. It aligns with [**PRD §7.2 Security Requirements and Controls**](./SPEC.md).

---

## Supported Versions | 支持版本

| Version   | Supported          |
| :-------- | :----------------- |
| **0.1.x** | :white_check_mark: |

---

## Reporting a Vulnerability | 漏洞报告

If you discover a security vulnerability, please report it responsibly:

1.  **Do not** open a public GitHub issue for security-sensitive findings.
2.  **Email** the maintainers (e.g. the contact in the PRD: `u3638376@connect.hku.hk`) with:
    -   A description of the vulnerability and steps to reproduce.
    -   Impact and suggested fix if possible.
3.  We will acknowledge receipt and aim to respond within a reasonable timeframe. We may ask for more details and will keep you updated on remediation and disclosure.

---

## Security-Related Configuration | 安全相关配置

-   **Secrets**: Do not commit `.env` or any file containing `SECRET_KEY`, API keys, or passwords. Use `.env.example` as a template only.
-   **Input Validation**: File type and size limits are enforced (see `UPLOAD_MAX_FILE_SIZE_MB`, `UPLOAD_MAX_FILES`). Only allowed extensions are parsed (see `app/parser/service.py`).
-   **TLS**: In production, use HTTPS and TLS 1.2+ for all endpoints and external calls ([PRD §7.2 DATA-01](./SPEC.md)).
-   **Auth**: API currently does not enforce authentication in the MVP; add AAD/API Key as per [PRD §5.2.8 and §7.2 IAM](./SPEC.md) before exposing externally.

---

## References | 参考

-   [**SPEC.md Section 7.2**](./SPEC.md) — Security Requirements and Controls (identity, data, application, operations, supply chain).
-   [**docs/05-deployment-runbook.md**](./docs/05-deployment-runbook.md) — Deployment, configuration, and network requirements.
