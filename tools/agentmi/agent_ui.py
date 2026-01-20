import streamlit as st
import os
from ollama import Client
import openai
from llama_agent import extract_todos, extract_code, validate_python_syntax

def initialize_client(backend, api_key, model):
    if backend == "ollama":
        client = Client(host='http://localhost:11434')
        # Check backend
        try:
            client.generate(model=model, prompt='test')
            models = client.list()
            if not any(model in m['name'] for m in models['models']):
                st.error(f"Model '{model}' not found. Run 'ollama pull {model}'.")
                return None
        except Exception as e:
            st.error(f"Ollama server not accessible: {e}")
            return None
        return client, "ollama"
    else:
        if not api_key:
            st.error("API key required for OpenAI.")
            return None, None
        try:
            openai_client = openai.OpenAI(api_key=api_key)
            openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
        except Exception as e:
            st.error(f"OpenAI API error: {e}")
            return None, None
        return openai_client, "openai"

def generate_todos(client, backend, model, spec):
    messages = [
        {'role': 'system', 'content': 'You are a helpful coding assistant. Always break down tasks into clear, numbered TODO steps first.'},
        {'role': 'user', 'content': f"Break down this coding task into a detailed list of TODO steps:\n\n{spec}"}
    ]
    if backend == "ollama":
        response = client.chat(model=model, messages=messages)
        return response['message']['content']
    else:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2
        )
        return response.choices[0].message.content

def generate_code(client, backend, model, spec, todos):
    messages = [
        {'role': 'system', 'content': 'You are a helpful coding assistant. Generate complete, executable code with imports and examples.'},
        {'role': 'user', 'content': f"Implement the following coding task, following these TODO steps:\n\nTask: {spec}\n\nTODOs:\n{todos}\n\nProvide the full code in a Python code block."}
    ]
    if backend == "ollama":
        response = client.chat(model=model, messages=messages)
        return response['message']['content']
    else:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2
        )
        return response.choices[0].message.content

st.title("AgentMi - LLaMA Coding Agent UI")

# Sidebar
st.sidebar.header("Configuration")
backend = st.sidebar.selectbox("Backend", ["ollama", "openai"])
model = st.sidebar.text_input("Model", 
                              value="codellama:13b-instruct" if backend == "ollama" else "gpt-3.5-turbo",
                              help="Ollama: e.g., codellama:13b-instruct; OpenAI: e.g., gpt-3.5-turbo")
if backend == "openai":
    api_key = st.sidebar.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")

spec = st.text_area("Task Specification", 
                    value="Write a Python function that calculates the factorial of a number.",
                    height=100)

if st.button("Generate"):
    if not spec.strip():
        st.warning("Please enter a task specification.")
    else:
        with st.spinner("Initializing backend..."):
            client, actual_backend = initialize_client(backend, api_key if backend == "openai" else None, model)
            if client is None:
                st.stop()
        
        # Generate TODOs
        with st.spinner("Generating TODO list..."):
            todo_response = generate_todos(client, actual_backend, model, spec)
            todos = extract_todos(todo_response)
        
        st.subheader("Generated TODOs")
        st.text(todos)
        
        # Generate Code
        with st.spinner("Generating code..."):
            code_response = generate_code(client, actual_backend, model, spec, todos)
            code = extract_code(code_response)
        
        st.subheader("Generated Code")
        st.code(code, language="python")
        
        # Validation
        if validate_python_syntax(code):
            st.success("Syntax validation passed!")
        else:
            st.warning("Syntax validation failed. Review the code.")
        
        # Save option
        if st.button("Save Outputs"):
            output_dir = "output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            with open(os.path.join(output_dir, "todos.md"), "w") as f:
                f.write(f"# Generated TODOs\n\n{todos}")
            with open(os.path.join(output_dir, "generated_code.py"), "w") as f:
                f.write(code)
            st.success("Outputs saved to output/ directory.")

# Instructions
with st.expander("How to Use"):
    st.write("""
    1. Select backend (Ollama for local, OpenAI for paid).
    2. Enter model name (defaults provided).
    3. For OpenAI, input your API key.
    4. Enter task spec and click Generate.
    5. Review TODOs and code; optionally save.
    6. Run the UI with: streamlit run agent_ui.py
    """)