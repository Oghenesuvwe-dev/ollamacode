# Phase 3: Intelligence & Database

**Goal**: Provide a centralized, persistent backend that hosts the Intelligence API (LLM interface) and stores review history for analytics.

---

## 🛠️ Tech Stack
*   **Language**: Python 3.10+ (FastAPI)
*   **Database**: PostgreSQL 15+
*   **ORM**: SQLAlchemy / SQLModel
*   **LLM Runtime**: Ollama (Local)
*   **Model**: `llama3:70b` (Recommended) or `codellama`

---

## 🧠 Intelligence Backend (FastAPI)

This service sits between Pipedream and the raw Ollama API. It adds application logic, logging, and database persistence.

### API Endpoints

#### `POST /api/v1/review`
Receives the diff and static analysis results from Pipedream.

**Request:**
```json
{
  "repo_name": "owner/repo",
  "pr_number": 123,
  "diff": "...",
  "findings": [...]
}
```

**Logic:**
1.  Creates a record in `RUNS` table.
2.  Forwards prompt to Ollama (`http://localhost:11434/api/generate`).
3.  Parses Ollama response.
4.  Stores individual issues in `FINDINGS` table.
5.  Returns formatted review to Pipedream.

---

## 💾 Database Schema (PostgreSQL)

We use a relational schema to track code quality over time.

```sql
-- Tracks each execution of the review pipeline
CREATE TABLE runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    repo_name VARCHAR(255) NOT NULL,
    pr_number INTEGER NOT NULL,
    commit_sha VARCHAR(40),
    status VARCHAR(20) CHECK (status IN ('PENDING', 'SUCCESS', 'FAILED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stores specific issues found by tools or AI
CREATE TABLE findings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id UUID REFERENCES runs(id),
    file_path VARCHAR(512) NOT NULL,
    line_number INTEGER,
    tool_name VARCHAR(50) NOT NULL, -- 'semgrep', 'bandit', 'ai-reviewer'
    severity VARCHAR(20) CHECK (severity IN ('INFO', 'WARNING', 'ERROR', 'CRITICAL')),
    message TEXT NOT NULL,
    suggested_fix TEXT, -- Code snippet for the fix
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for fast dashboard queries
CREATE INDEX idx_runs_repo ON runs(repo_name);
CREATE INDEX idx_findings_run ON findings(run_id);
```

---

## 🤖 Ollama Setup & Configuration

To ensure high-quality reviews, we use specific system prompts and model parameters.

### Recommended Model
We recommend **Llama 3 70B** for its reasoning capabilities, or **CodeLlama 34B** for strictly code-focused tasks.

```bash
# Install and run
ollama pull llama3:70b
ollama run llama3:70b
```

### System Prompt
```text
You are a Principal Software Engineer doing a code review.
Your goal is to find BUGS, SECURITY FLAWS, and PERFORMANCE ISSUES.
Do NOT comment on formatting, indentation, or variable naming unless it affects readability significantly.
Be concise. Provide code examples for fixes.
```

---

## 📊 Analytics & Dashboarding

By persisting data in PostgreSQL, we can generate SQL-based insights:

1.  **Top Failing Rules**: `SELECT message, COUNT(*) FROM findings GROUP BY message ORDER BY COUNT(*) DESC;`
2.  **Repo Health**: Average findings per PR over time.
3.  **AI Efficacy**: Track how many AI-suggested fixes were applied (requires feedback loop implementation).

---

## ✅ Best Practices
*   **Connection Pooling**: Use `pgbouncer` or SQLAlchemy pooling to handle high concurrency from webhooks.
*   **Sanitization**: Sanitize all inputs before constructing SQL queries (handled by ORM).
*   **Async I/O**: Use `async` handlers in FastAPI to prevent blocking during long LLM inference times.
