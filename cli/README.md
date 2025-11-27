# OllamaCode CLI

The official command-line interface for OllamaCode.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Initialize configuration
ollamacode auth login

# Request a fix for a file
ollamacode fix src/main.py --line 42

# Trigger a full review (manual trigger)
ollamacode review
```
