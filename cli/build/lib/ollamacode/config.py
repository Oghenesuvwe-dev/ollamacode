from pydantic_settings import BaseSettings
from pathlib import Path
import json
from typing import Optional

CONFIG_DIR = Path.home() / ".ollamacode"
CONFIG_FILE = CONFIG_DIR / "config.json"

class Settings(BaseSettings):
    api_url: str = "http://localhost:8000" # Default to local backend
    api_key: Optional[str] = None
    
    class Config:
        env_prefix = "OLLACODE_"

def load_config() -> Settings:
    """Load configuration from file or env vars."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            try:
                data = json.load(f)
                return Settings(**data)
            except json.JSONDecodeError:
                pass
    return Settings()

def save_config(settings: Settings):
    """Save configuration to file."""
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        f.write(settings.model_dump_json(indent=2))
