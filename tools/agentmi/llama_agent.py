
import os
import argparse
import re
from ollama import Client

def check_backend(client, backend, model):
   """Check if backend is accessible and model is available."""
   if backend == "ollama":
       try:
           # Test connection
           client.generate(model=model, prompt='test')
           # List models to confirm
           models = client.list()
           if not any(model in m['name'] for m in models['models']):
               raise Exception(f"Model '{model}' not found. Run 'ollama pull {model}'.")
           return True
       except Exception as e:
           raise Exception(f"Ollama server not accessible or model missing: {e}. Ensure Ollama is running with 'ollama run {model}'.")
   else:  # openai
       try:
           client.chat.completions.create(
               model=model,
               messages=[{"role": "user", "content": "test"}],
               max_tokens=1
           )
           return True
       except Exception as e:
           raise Exception(f"OpenAI API not accessible with model '{model}': {e}. Check your API key and internet connection.")

def extract_todos(response_text):
   """Extract TODO list from response using simple regex."""
   todo_pattern = r'TODOs?[:\s]*((?:\n?\s*\d+\.\s*[^#\n]+)+)'
   match = re.search(todo_pattern, response_text, re.IGNORECASE | re.DOTALL)
   if match:
       return match.group(1).strip()
   return "No TODOs extracted."

def extract_code(response_text):
   """Extract code block from response."""
   code_pattern = r'```(?:python)?\n(.*?)\n```'
   match = re.search(code_pattern, response_text, re.DOTALL)
   if match:
       return match.group(1).strip()
   # Fallback: everything after 'Code:' or similar
   code_start = re.search(r'(?:code|implementation)[:\s]*', response_text, re.IGNORECASE)
   if code_start:
       return response_text[code_start.end():].strip()
   return response_text.strip()

def validate_python_syntax(code):
   """Basic syntax validation for Python code."""
   try:
       compile(code, '<string>', 'exec')
       return True
   except SyntaxError as e:
       print(f"Syntax error in generated code: {e}")
       return False

def save_output(todos, code, output_dir="output"):
   """Save TODOs and code to files."""
   if not os.path.exists(output_dir):
       os.makedirs(output_dir)
       print(f"Created directory: {output_dir}")
   
   with open(os.path.join(output_dir, "todos.md"), "w") as f:
       f.write(f"# Generated TODOs\n\n{todos}")
   print(f"Saved TODOs to {output_dir}/todos.md")
   
   with open(os.path.join(output_dir, "generated_code.py"), "w") as f:
       f.write(code)
   print(f"Saved code to {output_dir}/generated_code.py")

def generate_response(client, backend, model, messages):
    """Generate response using the appropriate backend."""
    if backend == "ollama":
        response = client.chat(model=model, messages=messages)
        return response['message']['content']
    else:  # openai
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2
        )
        return response.choices[0].message.content


def main():
    parser = argparse.ArgumentParser(description="Local Code LLaMA Agent")
    parser.add_argument("--spec", type=str, help="Custom task specification (overrides file)")
    parser.add_argument("--model", type=str, default=None, help="Model to use (default: codellama:13b-instruct for ollama, gpt-3.5-turbo for openai)")
    parser.add_argument("--backend", type=str, default="ollama", choices=["ollama", "openai"], help="Backend: ollama (local) or openai (paid API)")
    parser.add_argument("--api-key", type=str, help="OpenAI API key (required if backend=openai)")
    args = parser.parse_args()
    
    if args.backend == "openai":
        if not args.api_key:
            parser.error("API key required for OpenAI backend. Use --api-key YOUR_KEY")
        import openai
        client = openai.OpenAI(api_key=args.api_key)
        model = args.model or "gpt-3.5-turbo"
    else:
        client = Client(host='http://localhost:11434')
        model = args.model or "codellama:13b-instruct"
   
# Read task specification
specs_dir = "specs"
task_spec_path = os.path.join(specs_dir, "task_spec.txt")

if not os.path.exists(specs_dir):
    os.makedirs(specs_dir)
    print(f"Created directory: {specs_dir}")

if args.spec:
    task_specification = args.spec
    print(f"Using custom spec:\n{task_specification}\n")
else:
    if not os.path.exists(task_spec_path):
        with open(task_spec_path, "w") as f:
            f.write("Write a Python function that calculates the factorial of a number.")
        print(f"Created placeholder task specification: {task_spec_path}")
    
    with open(task_spec_path, "r") as f:
        task_specification = f.read()

print(f"Task Specification:\n{task_specification}\n")

# Check backend
try:
    check_backend(client, args.backend, model)
except Exception as e:
    print(e)
    return

# Step 1: Generate TODOs
print("Generating TODO list...")
try:
    todo_messages = [
        {'role': 'system', 'content': 'You are a helpful coding assistant. Always break down tasks into clear, numbered TODO steps first.'},
        {'role': 'user', 'content': f"Break down this coding task into a detailed list of TODO steps:\n\n{task_specification}"}
    ]
    todo_text = generate_response(client, args.backend, model, todo_messages)
    todos = extract_todos(todo_text)
    print("\n--- Generated TODOs ---\n")
    print(todos)
except Exception as e:
    print(f"Error generating TODOs: {e}")
    return

# Step 2: Generate code based on spec and TODOs
print("\nGenerating code...")
try:
    code_messages = [
        {'role': 'system', 'content': 'You are a helpful coding assistant. Generate complete, executable code with imports and examples.'},
        {'role': 'user', 'content': f"Implement the following coding task, following these TODO steps:\n\nTask: {task_specification}\n\nTODOs:\n{todos}\n\nProvide the full code in a Python code block."}
    ]
    full_response = generate_response(client, args.backend, model, code_messages)
    code = extract_code(full_response)
    print("\n--- Generated Code ---\n")
    print(code)
    
    # Validate syntax
    if not validate_python_syntax(code):
        print("Warning: Generated code has syntax errors. Review before running.")
    
    # Save outputs
    save_output(todos, code)
    
    # Iterative refinement option
    refine = input("\nWould you like to refine the output? (y/n): ").lower().strip()
    if refine == 'y':
        print("Refinement mode: Provide feedback below (run script again with updated spec for full iteration).")
        # For MVP, simple note; full loop would require more UI
except Exception as e:
    print(f"Error generating code: {e}")
    return

if __name__ == "__main__":
    main()
