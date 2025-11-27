from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class Run(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    repo_name: str
    pr_number: int
    commit_sha: Optional[str] = None
    status: str = Field(default="PENDING") # PENDING, SUCCESS, FAILED
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    findings: List["Finding"] = Relationship(back_populates="run")

class Finding(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    run_id: uuid.UUID = Field(foreign_key="run.id")
    file_path: str
    line_number: Optional[int] = None
    tool_name: str # semgrep, bandit, ai-reviewer
    severity: str # INFO, WARNING, ERROR, CRITICAL
    message: str
    suggested_fix: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    run: Optional[Run] = Relationship(back_populates="findings")
