# How to Record Demo Assets | 如何录制演示素材

We need two types of assets: **Static Screenshots** (for README) and a **Live Demo GIF**.

---

## 1. Static Screenshots (Required) | 静态截图（必须）

**Target**: `docs/images/streamlit-dashboard.png` and `docs/images/streamlit-workbench.png`.

1.  **Start Streamlit**:
    ```bash
    streamlit run frontend/Home.py
    ```
2.  **Dashboard**: Take a screenshot of the main **Dashboard** page.
    -   Save as: `docs/images/streamlit-dashboard.png`.
3.  **Workbench**: Navigate to **Assessment Workbench**, upload a file, and wait for results.
    -   Take a screenshot of the results page (Risk/Compliance tabs).
    -   Save as: `docs/images/streamlit-workbench.png`.

---

## 2. Live Demo GIF (Optional) | 动态演示 GIF（可选）

**Target**: `docs/images/demo-assessment.gif`.

1.  **Record**: (e.g. using QuickTime, LICEcap, or ScreenToGif).
2.  **Workflow** (30-60s):
    -   Start on Dashboard.
    -   Click **Assessment Workbench**.
    -   Upload `examples/test_iso_27001_extract.pdf`.
    -   Click **Start Assessment**.
    -   Wait for the "Processing" steps.
    -   Show the final report tabs (Risk, Compliance).
3.  **Save**: Export as GIF to `docs/images/demo-assessment.gif`.

---

## Legacy: Browser + Demo Page (Old) | 旧版演示页

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
