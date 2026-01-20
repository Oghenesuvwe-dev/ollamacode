# AgentMi - Code Generation Tool

**Integrated Code Generator for OllamaCode**

## Overview

AgentMi is the code generation engine integrated into OllamaCode. It provides AI-powered code generation capabilities that complement the code review and fixing features.

## Purpose

AgentMi serves as a **backend tool** for OllamaCode, enabling:
- Generate code from natural language specifications
- Create fixes for detected issues
- Generate test cases for reviewed code
- Produce documentation from code

## Architecture

```
OllamaCode (Main Platform)
    └── tools/
        └── agentmi/  ← Code Generation Engine
            ├── llama_agent.py    # Core generation logic
            ├── agent_ui.py       # Streamlit UI (optional)
            └── requirements.txt  # Dependencies
```

## Integration

AgentMi is used by OllamaCode's backend services:

### 1. Fix Generation
When OllamaCode detects issues, AgentMi generates fixes:
```python
from tools.agentmi.llama_agent import generate_code

# Generate fix for detected issue
fix = generate_code(f"Fix this issue: {issue_description}")
```

### 2. Code Generation
Generate new code from specifications:
```python
# Generate code from spec
code = generate_code("Build a Flask API for user authentication")
```

### 3. Test Generation
Create tests for reviewed code:
```python
# Generate tests
tests = generate_code(f"Generate unit tests for:\n{code}")
```

## Usage

### As Standalone Tool
```bash
cd tools/agentmi
python llama_agent.py --spec "Build a Flask API"
```

### As Backend Service
AgentMi is automatically used by OllamaCode's backend when:
- Generating fixes for issues
- Creating code from specifications
- Producing test cases

## Features

- **Multi-backend Support:** Ollama (local) or OpenAI (cloud)
- **TODO Extraction:** Breaks down tasks into steps
- **Code Validation:** Validates generated Python syntax
- **Streamlit UI:** Optional web interface

## Configuration

AgentMi uses the same configuration as OllamaCode:
- Ollama endpoint: `http://localhost:11434`
- Model: `codellama:13b-instruct`
- OpenAI API key: Set via `--api-key` flag

## Dependencies

```bash
# Install AgentMi dependencies
cd tools/agentmi
pip install -r requirements.txt
```

## Status

**Role:** Backend code generation tool for OllamaCode  
**Status:** Integrated and operational  
**Version:** 1.0.0

## Related

- **Main Platform:** [OllamaCode](../../README.md)
- **Backend API:** [Backend Documentation](../../backend/README.md)
- **CLI Tool:** [CLI Documentation](../../cli/README.md)

---

**Note:** AgentMi is designed to work as part of OllamaCode's ecosystem. For standalone code generation, use the main OllamaCode CLI with `generate` commands.
