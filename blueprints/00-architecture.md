# 🤖 OllamaCode: Open-Source AI Code Reviewer
## Master Blueprint & Architecture

**OllamaCode** is a production-grade, 100% open-source alternative to commercial code review tools like CodeRabbit and DeepSource. It orchestrates AI-powered code reviews, static analysis, and security scanning without vendor lock-in, ensuring full data privacy and control.

---

## 🏗️ System Architecture

The system follows a decoupled, event-driven architecture designed for scalability and privacy.

```mermaid
graph LR
    User[Developer/CLI] -->|Trigger| GitHub[GitHub PR]
    GitHub -->|Webhook| Pipedream[Pipedream Orchestration]
    
    subgraph "Phase 1: Frontend"
        User
    end

    subgraph "Phase 2: Orchestration"
        Pipedream -->|1. Fetch Diff| GitHub
        Pipedream -->|2. Static Analysis| SAST[Semgrep/Bandit]
        Pipedream -->|3. AI Review| Intelligence
        Pipedream -->|4. Post Comment| GitHub
    end
    
    subgraph "Phase 3: Intelligence & Persistence"
        Intelligence[Intelligence Backend]
        Intelligence <-->|Inference| Ollama[Ollama (Llama 3)]
        Intelligence <-->|Store/Fetch| DB[(PostgreSQL)]
    end
```

---

## 🛠️ Open Source Tech Stack

We strictly use open-source technologies to ensure freedom and transparency.

### **Core Components**
| Component | Technology | License | Purpose |
| :--- | :--- | :--- | :--- |
| **Orchestration** | **Pipedream** | Apache 2.0 (Self-hostable) | Workflow automation & GitHub integration |
| **LLM Inference** | **Ollama** | MIT | Local LLM runner (Llama 3, CodeLlama) |
| **Database** | **PostgreSQL** | PostgreSQL | Relational data storage for findings |
| **CLI** | **Python (Typer)** | MIT | Developer frontend tool |

### **Static Analysis Tools (SAST)**
| Tool | Language | Purpose |
| :--- | :--- | :--- |
| **Semgrep** | Multi-language | Semantic code analysis for bugs & security |
| **Bandit** | Python | Common security issues scanner |
| **TruffleHog** | Universal | Secret & credential detection |
| **ESLint** | JavaScript/TS | Code quality & style |

---

## 📂 Project Structure & Phases

The project is divided into three distinct phases. Refer to the specific documentation for implementation details.

### **[Phase 1: Frontend CLI](./Phase-1-Frontend.md)**
*   **Goal**: Developer tool to manually trigger reviews or fixes.
*   **Stack**: Python, Typer, Rich.
*   **Key Features**: CLI interface, local fix application, manual triggers.

### **[Phase 2: Backend Orchestration](./Phase-2-Backend.md)**
*   **Goal**: Serverless workflow to manage the review lifecycle.
*   **Stack**: Pipedream, Node.js, Docker (via execa).
*   **Key Features**: GitHub Webhooks, Git cloning, Static Analysis execution, AI prompt construction.

### **[Phase 3: Intelligence & Database](./Phase-3-Database.md)**
*   **Goal**: Centralized intelligence server and historical data persistence.
*   **Stack**: Python (FastAPI), PostgreSQL, Ollama.
*   **Key Features**: LLM API wrapping, finding storage, dashboard data aggregation.

---

## 🚀 Getting Started

### Prerequisites
1.  **Docker & Docker Compose**: For running the database and local services.
2.  **Ollama**: Installed locally or on a GPU server (`curl -fsSL https://ollama.com/install.sh | sh`).
3.  **Pipedream Account**: For workflow orchestration.
4.  **Node.js & Python 3.10+**: For local development.

### Quick Setup
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-org/ollamacode.git
    cd ollamacode
    ```

2.  **Start Infrastructure (Phase 3)**:
    ```bash
    docker-compose up -d postgres ollama
    ```

3.  **Install CLI (Phase 1)**:
    ```bash
    pip install -e ./cli
    ollamacode init
    ```

4.  **Deploy Workflow (Phase 2)**:
    *   Import the workflow definition from `Phase-2-Backend.md` into Pipedream.
    *   Configure `GITHUB_TOKEN` and `OLLAMA_URL`.

---

## 📜 Best Practices Implemented
*   **Security First**: All secrets are detected before code leaves the perimeter.
*   **Privacy**: Code snippets for AI review are processed by **local/private** LLMs (Ollama), not public APIs.
*   **Idempotency**: Webhooks and workflows handle duplicate events gracefully.
*   **Structured Logging**: All findings are stored in a structured SQL schema for analytics.