# Testing Generated Code Instructions

## Overview
After running `python llama_agent.py` (or with `--spec`), the agent generates code in `output/generated_code.py`. Follow these steps to test it:

## Steps to Test

1. **Navigate to output directory**:
   ```
   cd output
   ```

2. **Run the generated code**:
   ```
   python generated_code.py
   ```
   - Observe the output in the terminal.
   - For specs requiring input (e.g., CLI args), provide them: `python generated_code.py arg1 arg2`.

3. **Verify correctness**:
   - **Factorial (fibonacci.txt or task_spec.txt)**: Input n=5, expect output like [1, 1, 2, 3, 5] or factorial 120.
   - **Todo API (todo_api.txt)**: Run with `python generated_code.py` (if it includes a test server), use curl: `curl -X POST http://localhost:5000/todos -d '{"title": "Test"}' -H "Content-Type: application/json"`, then `curl http://localhost:5000/todos`.
   - **Web Scraper (web_scraper.txt)**: Expect printed paragraphs from https://example.com.
   - Check for errors; if syntax validation warned, fix manually.

4. **Iterate if needed**:
   - Review `output/todos.md` for steps.
   - Rerun agent with refined spec to improve.

## Automated Testing (Optional)
Create a simple test script for specific outputs, e.g., for factorial:

```python
# test_factorial.py
import sys
sys.path.append('output')
try:
    from generated_code import factorial  # Assume function name
    assert factorial(5) == 120
    print("Test passed!")
except Exception as e:
    print(f"Test failed: {e}")
```

Run: `python test_factorial.py`.

If generated code doesn't match expected functions, adapt the test.

## Testing New Features

### Multi-Backend and Model Selection
1. **Ollama with different model**:
   - Pull another model: `ollama pull codellama:7b-instruct`
   - Run: `python llama_agent.py --model codellama:7b-instruct --spec "Simple task"`
   - Verify TODOs and code generation differ or match expectations.

2. **OpenAI Backend**:
   - Ensure you have an OpenAI API key.
   - Run: `python llama_agent.py --backend openai --api-key sk-your-key --model gpt-3.5-turbo --spec "Simple task"`
   - Check for successful generation without Ollama dependency; compare output quality.

3. **Error Handling**:
   - Invalid model: Use non-existent model; expect error message.
   - Missing API key: Run OpenAI without key; expect parser error.

### Streamlit UI Testing
1. **Run the UI**:
   ```bash
   streamlit run agent_ui.py
   ```
   - Browser opens at http://localhost:8501.

2. **Basic Flow**:
   - Select Ollama, default model, enter spec, click Generate.
   - Verify TODOs display, code shows with syntax check, save works (check output/ files).

3. **OpenAI in UI**:
   - Select OpenAI, enter model and API key, generate.
   - Ensure no errors; outputs saved.

4. **Edge Cases**:
   - Empty spec: Expect warning.
   - Invalid backend config: Expect error messages in UI.

For all tests, review generated code in output/ and run it manually to verify functionality.