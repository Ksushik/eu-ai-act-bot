"""
Configuration settings for EU AI Act Compliance Bot.

Environment-based configuration using Pydantic settings.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "EU AI Act Compliance Bot"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "eu-ai-act-compliance-bot"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # Next.js dev server
        "http://localhost:8000",  # FastAPI dev server
        "https://eu-ai-act-bot.vercel.app",  # Production frontend
    ]
    
    # Database
    DATABASE_URL: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: Optional[str] = None
    
    # AI Services
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    
    # Vector Database
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: Optional[str] = None
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 3600  # 1 hour
    
    # Analysis Settings
    MAX_ANALYSIS_LENGTH: int = 50000  # Max characters in AI system description
    DEFAULT_TEMPERATURE: float = 0.1  # Low temperature for consistent analysis
    MAX_TOKENS: int = 4000
    
    # File Storage
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_database_url(self) -> str:
        """Construct database URL from components."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        
        if all([self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_HOST, self.POSTGRES_DB]):
            return (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )
        
        # Fallback to SQLite for development
        return "sqlite:///./eu_ai_act_bot.db"

    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS origins to list if string."""
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS


# Global settings instance
settings = Settings()