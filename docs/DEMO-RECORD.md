# How to Record a 30s Demo | 如何录制 30 秒演示

Record a 30–60s GIF/Video of the assessment workflow and save it to **`docs/images/demo-assessment.gif`**.

---

## Option 1: Browser + Demo Page (Recommended) | 浏览器 + 演示页

1.  **Start API**:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```
2.  **Open Demo**: Open **`docs/demo.html`** in your browser.
    -   *Note: If you hit CORS issues, serve the docs directory:* `cd docs && python -m http.server 8888`.
3.  **Record**: (e.g. using QuickTime or LICEcap).
4.  **Workflow** (20-30s):
    -   Select **`examples/sample.txt`**.
    -   Click **Assess**.
    -   Wait for JSON report to appear.
    -   End recording.
5.  **Save**: Export as GIF to `docs/images/demo-assessment.gif`.

---

## Option 2: Swagger UI (/docs) | Swagger 界面

1.  Open **http://localhost:8000/docs**.
2.  **POST /api/v1/assessments**: Try it out → Upload `sample.txt` → Execute.
3.  Copy `task_id`.
4.  **GET /api/v1/assessments/{task_id}**: Paste ID → Execute → View Report.
5.  Save recording as GIF.

---

## Option 3: Terminal Script (Geek Style) | 终端脚本

1.  Start API.
2.  Record terminal window.
3.  Run:
    ```bash
    chmod +x scripts/demo.sh
    ./scripts/demo.sh
    ```
4.  Save recording as GIF.

---

## Update README | 更新 README

Once saved, replace the placeholder in `README.md` with:

```markdown
![Demo: upload → assessment report](docs/images/demo-assessment.gif)
```
