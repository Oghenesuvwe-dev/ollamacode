from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.models import Run, Finding
from app.ollama_client import generate_review
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ReviewRequest(BaseModel):
    repo_name: str
    pr_number: int
    diff: str
    findings: List[dict]

@router.post("/review")
async def create_review(request: ReviewRequest):
    # 1. Create Run record
    # In a real app, we'd use dependency injection for the DB session
    # run = Run(repo_name=request.repo_name, pr_number=request.pr_number)
    # session.add(run)
    # session.commit()
    
    # 2. Generate AI Review
    ai_response = await generate_review(request.diff, request.findings)
    
    # 3. Store Findings
    # ... parsing logic would go here ...
    
    return {
        "status": "success",
        "ai_review": ai_response
    }

@router.post("/fix")
async def generate_fix(filename: str, content: str, line: int = None, context: str = None):
    # Simple endpoint for the CLI 'fix' command
    prompt = f"Fix the following code in {filename}:\n\n{content}\n"
    if line:
        prompt += f"\nFocus on line {line}."
    if context:
        prompt += f"\nUser context: {context}"
        
    # Reuse generate_review logic or create a specific generate_fix function
    # For now, mocking the response structure
    return {
        "explanation": "Here is a suggested fix based on your request.",
        "code": "# Fixed code would appear here"
    }
