# OllamaCode - AI-Powered Code Review & Generation Platform

Open-source alternative to CodeRabbit with integrated code generation powered by AgentMi.

## Features

### 🔍 Code Review
- AI-powered code review
- Static analysis (Semgrep, Bandit, TruffleHog)
- Security vulnerability detection
- Best practices enforcement

### 🔧 Auto-Fix
- AI-generated fixes for detected issues
- One-click fix application
- Safe refactoring suggestions

### ✨ Code Generation (NEW - Powered by AgentMi)
- Generate code from natural language
- Create fixes for issues automatically
- Generate test cases
- Multi-language support

### ⚡ Pipedream Integration
- Automated PR reviews
- GitHub webhook integration
- CI/CD pipeline support

## Architecture

```
OllamaCode Platform
├── backend/          # FastAPI server
├── cli/              # Command-line tool
├── tools/
│   └── agentmi/     # Code generation engine ⭐
└── workflows/        # Pipedream workflows
```

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/Oghenesuvwe-dev/ollamacode.git
cd ollamacode

# Install backend
cd backend
pip install -r requirements.txt

# Install CLI
cd ../cli
pip install -e .

# Install AgentMi (code generator)
cd ../tools/agentmi
pip install -r requirements.txt
```

### Usage

**Review Code:**
```bash
ollamacode review file.py
```

**Fix Issues:**
```bash
ollamacode fix file.py --line 42
```

**Generate Code (AgentMi):**
```bash
cd tools/agentmi
python llama_agent.py --spec "Build a Flask API"
```

## Components

### Backend (FastAPI)
- RESTful API for code review and fixing
- PostgreSQL database for history
- Ollama integration for AI

### CLI (Typer)
- Command-line interface
- Review, fix, and auth commands
- Rich terminal output

### AgentMi (Code Generator)
**Integrated as backend tool** for code generation capabilities:
- Generates code from specifications
- Creates fixes for detected issues
- Produces test cases
- See [tools/agentmi/README.md](tools/agentmi/README.md)

### Workflows (Pipedream)
- Automated PR review workflows
- GitHub integration
- Static analysis pipeline

## Tech Stack

- **Backend:** FastAPI, PostgreSQL, SQLModel
- **CLI:** Typer, Rich
- **AI:** Ollama, OpenAI
- **Code Generation:** AgentMi (integrated)
- **Analysis:** Semgrep, Bandit, TruffleHog
- **Orchestration:** Pipedream

## Documentation

- [Backend API](backend/README.md)
- [CLI Guide](cli/README.md)
- [AgentMi Integration](tools/agentmi/README.md)
- [Pipedream Setup](workflows/README.md)

## Development

```bash
# Run backend
cd backend
uvicorn app.main:app --reload

# Run tests
pytest tests/

# Run CLI
ollamacode --help
```

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License

## Related Projects

- **AgentMi:** Integrated as code generation tool
- **NemoCode Studio:** AI-powered IDE

---

**OllamaCode:** Complete AI code platform - Review, Fix, and Generate
