"""
Health check endpoints for EU AI Act Compliance Bot API.

Basic health monitoring and service status endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
import os
import psutil

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: datetime
    version: str
    uptime_seconds: float
    checks: Dict[str, Any]


class ServiceStatus(BaseModel):
    """Individual service status."""
    name: str
    status: str
    details: Dict[str, Any]


@router.get("/", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint."""
    try:
        # Get system metrics
        process = psutil.Process()
        uptime = process.create_time()
        current_time = datetime.utcnow()
        
        checks = {
            "api": {"status": "healthy", "details": "API is responding"},
            "database": await _check_database(),
            "ai_service": await _check_ai_services(),
            "memory_usage": {
                "status": "healthy",
                "details": {
                    "memory_percent": process.memory_percent(),
                    "memory_mb": process.memory_info().rss / 1024 / 1024
                }
            }
        }
        
        # Determine overall status
        overall_status = "healthy"
        for check_name, check_result in checks.items():
            if check_result.get("status") != "healthy":
                overall_status = "degraded"
                break
        
        return HealthResponse(
            status=overall_status,
            timestamp=current_time,
            version="0.1.0",
            uptime_seconds=(current_time.timestamp() - uptime),
            checks=checks
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )


@router.get("/detailed", response_model=Dict[str, ServiceStatus])
async def detailed_health():
    """Detailed health check with individual service status."""
    services = {}
    
    # Database check
    db_status = await _check_database()
    services["database"] = ServiceStatus(
        name="Database",
        status=db_status["status"],
        details=db_status["details"]
    )
    
    # AI Services check
    ai_status = await _check_ai_services()
    services["ai_services"] = ServiceStatus(
        name="AI Services",
        status=ai_status["status"],
        details=ai_status["details"]
    )
    
    # Vector DB check (when implemented)
    services["vector_db"] = ServiceStatus(
        name="Vector Database",
        status="not_implemented",
        details={"message": "Vector DB integration pending"}
    )
    
    return services


@router.get("/ready")
async def readiness_check():
    """Kubernetes-style readiness check."""
    try:
        # Check critical dependencies
        db_status = await _check_database()
        ai_status = await _check_ai_services()
        
        if db_status["status"] != "healthy" or ai_status["status"] != "healthy":
            raise HTTPException(status_code=503, detail="Service not ready")
        
        return {"status": "ready", "timestamp": datetime.utcnow()}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Readiness check failed: {str(e)}")


@router.get("/live")
async def liveness_check():
    """Kubernetes-style liveness check."""
    return {"status": "alive", "timestamp": datetime.utcnow()}


async def _check_database() -> Dict[str, Any]:
    """Check database connectivity."""
    try:
        # TODO: Implement actual database connection check
        # For now, check if database URL is configured
        from app.core.config import settings
        db_url = settings.get_database_url()
        
        if not db_url:
            return {
                "status": "unhealthy",
                "details": {"error": "Database URL not configured"}
            }
        
        # Placeholder for actual DB connection test
        return {
            "status": "healthy",
            "details": {
                "database_url": db_url.split("://")[0] + "://***",
                "note": "Connection test not implemented yet"
            }
        }
    
    except Exception as e:
        return {
            "status": "unhealthy",
            "details": {"error": str(e)}
        }


async def _check_ai_services() -> Dict[str, Any]:
    """Check AI service connectivity."""
    try:
        from app.core.config import settings
        
        services = {}
        overall_status = "healthy"
        
        # Check Anthropic API key
        if settings.ANTHROPIC_API_KEY:
            services["anthropic"] = "configured"
        else:
            services["anthropic"] = "not_configured"
            overall_status = "degraded"
        
        # Check OpenAI API key (optional)
        if settings.OPENAI_API_KEY:
            services["openai"] = "configured"
        else:
            services["openai"] = "not_configured"
        
        return {
            "status": overall_status,
            "details": {
                "services": services,
                "note": "API connectivity test not implemented yet"
            }
        }
    
    except Exception as e:
        return {
            "status": "unhealthy",
            "details": {"error": str(e)}
        }