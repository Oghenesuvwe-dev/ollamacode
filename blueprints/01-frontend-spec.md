# Phase 1: Frontend CLI

**Goal**: Provide a developer-friendly Command Line Interface (CLI) to trigger reviews, request fixes for specific errors, and manage configuration.

---

## 🛠️ Tech Stack
*   **Language**: Python 3.10+
*   **Framework**: `Typer` (Modern, fast CLI building)
*   **UI/Formatting**: `Rich` (Beautiful terminal formatting)
*   **HTTP Client**: `Httpx` (Async HTTP requests)
*   **Config Management**: `Pydantic` (Settings validation)

---

## 📂 Directory Structure

```text
cli/
├── ollamacode/
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── config.py        # Configuration management
│   ├── client.py        # API Client for Backend/Pipedream
│   └── commands/
│       ├── fix.py       # 'fix' command
│       ├── review.py    # 'review' command
│       └── auth.py      # 'login' command
├── pyproject.toml       # Dependencies
└── README.md
```

---

## 💻 Implementation Details

### 1. Configuration (`config.py`)
Use `pydantic-settings` to manage environment variables and local config files (`~/.ollamacode/config.json`).

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_url: str = "https://api.ollamacode.dev" # Or Pipedream webhook URL
    api_key: str | None = None
    
    class Config:
        env_prefix = "OLLACODE_"
```

### 2. Main Entry Point (`main.py`)
Setup the Typer app with Rich exception handling.

```python
import typer
from rich.console import Console
from ollamacode.commands import fix, review, auth

app = typer.Typer(
    name="ollamacode",
    help="🤖 Open Source AI Code Reviewer CLI",
    add_completion=False
)
console = Console()

app.add_typer(fix.app, name="fix")
app.add_typer(review.app, name="review")
app.add_typer(auth.app, name="auth")

if __name__ == "__main__":
    app()
```

### 3. The `fix` Command (`commands/fix.py`)
Allows developers to send a specific file or error context to the AI for an immediate fix suggestion.

```python
import typer
from pathlib import Path
from ollamacode.client import APIClient

app = typer.Typer()

@app.command()
def file(
    path: Path = typer.Argument(..., exists=True, help="Path to the file to fix"),
    line: int = typer.Option(None, help="Specific line number to focus on"),
    context: str = typer.Option(None, help="Additional error context or instructions")
):
    """
    Request an AI fix for a specific file.
    """
    with open(path, "r") as f:
        content = f.read()

    client = APIClient()
    response = client.trigger_fix(
        filename=path.name,
        content=content,
        line=line,
        user_context=context
    )
    
    # Display the diff/suggestion
    client.display_solution(response)
```

---

## 🔄 Workflow Integration

When a user runs `ollamacode fix`, the CLI:
1.  Reads the local file content.
2.  Captures optional user context (e.g., "This function is raising a ValueError").
3.  Sends a JSON payload to the **Pipedream Webhook** (Phase 2).

**Payload Format:**
```json
{
  "type": "manual_fix",
  "repository": "owner/repo",
  "file_path": "src/utils.py",
  "content": "def foo()...",
  "line_number": 42,
  "user_instruction": "Fix the type error on line 42"
}
```

---

## ✅ Best Practices
*   **User Feedback**: Use `rich.status` spinners to indicate network activity.
*   **Error Handling**: Gracefully handle network timeouts and invalid API keys.
*   **Security**: Never send `.env` files or ignored files (respect `.gitignore`).
