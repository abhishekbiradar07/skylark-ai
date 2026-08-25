"""Configuration management for Skylark BI Agent."""
import os
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    # Monday.com Configuration
    MONDAY_API_TOKEN: str = os.getenv("MONDAY_API_TOKEN", "")
    MONDAY_WORK_ORDERS_BOARD_ID: str = os.getenv("MONDAY_WORK_ORDERS_BOARD_ID", "5030843474")
    MONDAY_DEALS_BOARD_ID: str = os.getenv("MONDAY_DEALS_BOARD_ID", "5030842785")
    MONDAY_API_URL: str = "https://api.monday.com/v2"
    
    # LLM Configuration - Groq only
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # Server Configuration
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    # Cache Configuration
    CACHE_DURATION_MINUTES: int = int(os.getenv("CACHE_DURATION_MINUTES", "5"))
    
    @classmethod
    def validate(cls) -> list[str]:
        """Validate required configuration."""
        errors = []
        
        if not cls.MONDAY_API_TOKEN:
            errors.append("MONDAY_API_TOKEN is required")
        
        if not cls.GROQ_API_KEY:
            errors.append("GROQ_API_KEY is required")
        
        return errors

config = Config()
