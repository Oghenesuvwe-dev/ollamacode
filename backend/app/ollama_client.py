import httpx
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ollama_url: str = "http://localhost:11434"
    model_name: str = "llama3:70b"

settings = Settings()

async def generate_review(diff: str, findings: list) -> str:
    """
    Generate a code review using Ollama.
    """
    prompt = f"""
You are an expert code reviewer.
CONTEXT:
The following are static analysis findings for the code:
{findings}

CODE DIFF:
{diff}

TASK:
Review the code changes. Focus on:
1. Logic errors
2. Security vulnerabilities missed by static analysis
3. Performance issues

Format your response as a Markdown list of issues.
"""
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.ollama_url}/api/generate",
                json={
                    "model": settings.model_name,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120.0
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            return f"Error generating review: {str(e)}"
