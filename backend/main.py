"""
EU AI Act Compliance Bot - FastAPI Backend

Main application entry point for the compliance assessment API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from dotenv import load_dotenv

from app.api import analysis, health
from app.core.config import settings

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("Starting EU AI Act Compliance Bot API")
    
    # Initialize services here
    # await initialize_knowledge_base()
    # await initialize_vector_db()
    
    yield
    
    logger.info("Shutting down EU AI Act Compliance Bot API")
    # Cleanup here
    # await cleanup_resources()

# Create FastAPI application
app = FastAPI(
    title="EU AI Act Compliance Bot",
    description="Automated regulatory assessment for AI systems under EU AI Act",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["Analysis"])

@app.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {
        "message": "EU AI Act Compliance Bot API",
        "version": "0.1.0",
        "docs": "/docs",
        "status": "active"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )