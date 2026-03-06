# Marketing & Launch Checklist | 推广与发布清单

This document outlines the strategy to increase visibility and adoption of **Arthor-Agent**.

本文档概述了提高 **Arthor-Agent** 曝光度与采用率的策略。

---

## 1. Distribution & Packaging | 分发与打包

- [ ] **Publish to PyPI**: Ensure users can install via `pip install arthor-agent`.
    ```bash
    pip install build twine
    python3 -m build
    python3 -m twine upload dist/*
    ```
- [ ] **Docker Hub**: Push the Docker image to Docker Hub (e.g., `arthurpanhku/arthor-agent`).
    - Add a `latest` tag and version tags (e.g., `v0.1.0`).

## 2. Ecosystem Integration | 生态集成

- [ ] **Submit to MCP Registries**:
    - [awesome-mcp](https://github.com/punkpeye/awesome-mcp)
    - [glama.ai/mcp/servers](https://glama.ai/mcp/servers)
    - [smithery.ai](https://smithery.ai)
- [ ] **Submit to "Awesome" Lists**:
    - [awesome-langchain](https://github.com/kyrolabs/awesome-langchain)
    - [awesome-security-automation](https://github.com/0x4D31/awesome-security-automation)
    - [awesome-local-llm](https://github.com/janhq/awesome-local-ai)

## 3. Content Marketing | 内容营销

- [ ] **Record the Demo Video**: Follow `docs/DEMO-RECORD.md`.
    - Upload to YouTube / Loom.
    - Embed in README (replace the GIF if the video is better).
- [ ] **Write a Blog Post**: "Building an AI Security Agent with MCP and LangChain".
    - Publish on Medium, Dev.to, or personal blog.
    - Share the link on LinkedIn / Twitter.
- [ ] **Tweet / X Thread**:
    - "Just released Arthor-Agent: An open-source AI security assessor."
    - Highlight: MCP support, Local LLM (Ollama), RAG.
    - Tag: `@LangChainAI`, `@AnthropicAI` (for MCP), `@Ollama`.

## 4. Community Launch | 社区发布

- [ ] **Hacker News (Show HN)**:
    - Title: "Show HN: Arthor-Agent – Open Source AI Security Assessment (MCP support)"
    - Post at peak time (e.g., weekday morning PT).
- [ ] **Reddit**:
    - r/LocalLLaMA: Focus on "Run locally with Ollama".
    - r/netsec / r/cybersecurity: Focus on "Automating questionnaire reviews".
    - r/selfhosted: Focus on "Docker deployable security tool".
- [ ] **Product Hunt**: Prepare a launch page (optional but good for traffic).

## 5. Documentation Polish | 文档打磨

- [ ] **Shields.io Badges**: Ensure all badges in README are green/passing.
- [ ] **"Deploy to..." Buttons**: Add One-Click Deploy for Render/Railway if possible.
- [ ] **User Success Stories**: If anyone uses it, ask for a testimonial.

---

## 📅 Launch Timeline Example

| Day       | Activity                                                           |
| :-------- | :----------------------------------------------------------------- |
| **Day 1** | Finalize docs, record demo, publish to PyPI/DockerHub.             |
| **Day 2** | **"Soft Launch"**: Post to Reddit (r/LocalLLaMA). Gather feedback. |
| **Day 3** | **"Hard Launch"**: Show HN, Product Hunt, Twitter Thread.          |
| **Day 4** | Submit PRs to "Awesome" lists and MCP registries.                  |
| **Day 5** | Respond to comments, fix bugs, thank contributors.                 |
