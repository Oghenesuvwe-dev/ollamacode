# OllamaCode Web UI - Quick Start

## Run with Docker (Recommended)

```bash
docker-compose up -d
```

Access:
- **Web UI**: http://localhost:8501
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Run Locally

```bash
# Terminal 1: Start backend
cd backend
poetry install
poetry run uvicorn app.main:app --reload

# Terminal 2: Start web UI
pip install -r requirements-web.txt
streamlit run web_ui.py
```

## Features

### GitHub Review Tab
- Paste PR diff
- Get AI-powered review
- Security & quality analysis

### Code Fix Tab
- Paste problematic code
- Get automated fixes
- Line-specific suggestions

### Generate Code Tab
- Natural language specs
- Full code generation
- Uses AgentMi engine

## Environment Variables

```bash
export API_URL=http://localhost:8000/api/v1
```

## Push to GitHub

```bash
git add web_ui.py requirements-web.txt docker-compose.yml WEB_QUICKSTART.md
git commit -m "Add Streamlit web UI with GitHub integration"
git push origin main
```
