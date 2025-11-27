from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="OllamaCode Intelligence Backend",
    description="API for AI-powered code reviews and persistence.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "OllamaCode Backend is running"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

from app.api import router
app.include_router(router, prefix="/api/v1")
