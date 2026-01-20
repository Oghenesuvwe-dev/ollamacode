import streamlit as st
import requests
import os

st.set_page_config(page_title="OllamaCode", page_icon="🔍", layout="wide")

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

st.title("🔍 OllamaCode - AI Code Review Platform")

tab1, tab2, tab3 = st.tabs(["GitHub Review", "Code Fix", "Generate Code"])

# Tab 1: GitHub Review
with tab1:
    st.header("GitHub PR Review")
    
    col1, col2 = st.columns(2)
    with col1:
        repo_name = st.text_input("Repository", placeholder="owner/repo")
    with col2:
        pr_number = st.number_input("PR Number", min_value=1, step=1)
    
    diff = st.text_area("Code Diff", height=200, placeholder="Paste git diff here...")
    
    if st.button("Review Code", type="primary"):
        if not repo_name or not diff:
            st.error("Repository and diff required")
        else:
            with st.spinner("Analyzing code..."):
                try:
                    response = requests.post(f"{API_URL}/review", json={
                        "repo_name": repo_name,
                        "pr_number": pr_number,
                        "diff": diff,
                        "findings": []
                    })
                    if response.status_code == 200:
                        result = response.json()
                        st.success("Review complete!")
                        st.markdown("### AI Review")
                        st.markdown(result.get("ai_review", "No review generated"))
                    else:
                        st.error(f"Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

# Tab 2: Code Fix
with tab2:
    st.header("Fix Code Issues")
    
    filename = st.text_input("Filename", placeholder="example.py")
    code = st.text_area("Code to Fix", height=300, placeholder="Paste code here...")
    line = st.number_input("Line Number (optional)", min_value=0, value=0)
    context = st.text_input("Issue Description", placeholder="Describe the problem...")
    
    if st.button("Generate Fix", type="primary"):
        if not code:
            st.error("Code required")
        else:
            with st.spinner("Generating fix..."):
                try:
                    response = requests.post(f"{API_URL}/fix", params={
                        "filename": filename or "code.py",
                        "content": code,
                        "line": line if line > 0 else None,
                        "context": context
                    })
                    if response.status_code == 200:
                        result = response.json()
                        st.success("Fix generated!")
                        st.markdown("### Explanation")
                        st.info(result.get("explanation", ""))
                        st.markdown("### Fixed Code")
                        st.code(result.get("code", ""), language="python")
                    else:
                        st.error(f"Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

# Tab 3: Generate Code
with tab3:
    st.header("Generate Code from Spec")
    
    spec = st.text_area("Task Specification", height=150, 
                       placeholder="Describe what you want to build...")
    
    if st.button("Generate", type="primary"):
        if not spec:
            st.error("Specification required")
        else:
            st.info("Code generation coming soon - uses AgentMi backend")

# Sidebar
with st.sidebar:
    st.header("Settings")
    st.text_input("API URL", value=API_URL, disabled=True)
    
    if st.button("Check Backend"):
        try:
            response = requests.get("http://localhost:8000/health")
            if response.status_code == 200:
                st.success("✅ Backend connected")
            else:
                st.error("❌ Backend error")
        except:
            st.error("❌ Backend offline")
    
    st.divider()
    st.markdown("### About")
    st.markdown("OllamaCode v0.9.0")
    st.markdown("[GitHub](https://github.com/Oghenesuvwe-dev/ollamacode)")
