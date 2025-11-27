# Project Roadmap & Tasks

## 📂 Specifications
- [x] Architecture Overview: [00-architecture.md](blueprints/00-architecture.md)
- [x] Frontend CLI Spec: [01-frontend-spec.md](blueprints/01-frontend-spec.md)
- [x] Orchestration Spec: [02-orchestration-spec.md](blueprints/02-orchestration-spec.md)
- [x] Intelligence Spec: [03-intelligence-spec.md](blueprints/03-intelligence-spec.md)

## 🚀 Phase 1: Frontend CLI
- [x] **Setup**: Project structure, `pyproject.toml`, dependencies
- [x] **Core**: `config.py` and `main.py` entry point
- [x] **Commands**:
    - [x] `fix`: Request AI fixes for local files
    - [x] `review`: Trigger PR reviews manually
    - [x] `auth`: Manage API keys and settings

## ⚡ Phase 2: Backend Orchestration
- [x] **Workflow**: Define Pipedream steps in `workflow_steps.js`
- [x] **Steps**:
    - [x] Trigger & Clone
    - [x] Static Analysis (Semgrep, Bandit)
    - [x] AI Review Integration

## 🧠 Phase 3: Intelligence & Database
- [x] **Backend**: Setup FastAPI project
- [x] **Database**:
    - [x] Define `Run` and `Finding` models (SQLModel)
    - [x] Setup Migrations (Alembic)
- [x] **AI**: Implement Ollama client for inference
- [x] **API**:
    - [x] `/review` endpoint
    - [x] `/fix` endpoint

## 🔮 Future / To-Do
- [x] **Testing**: Add unit tests for CLI and Backend
- [x] **CI/CD**: Setup GitHub Actions for the project itself
- [x] **Deployment**: Docker Compose for full stack deployment
