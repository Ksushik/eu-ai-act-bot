"""
Compliance analysis API endpoints.

Core endpoints for AI system compliance assessment against EU AI Act.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
import time
import uuid
from datetime import datetime

from app.models.compliance import (
    AISystemDescription,
    ComplianceAnalysisRequest,
    ComplianceAnalysisResponse,
    ComplianceReport,
    RiskCategory
)
from app.services.compliance_analyzer import ComplianceAnalyzerService
from app.core.config import settings

router = APIRouter()

# Dependency to get compliance analyzer service
def get_compliance_analyzer():
    """Dependency to provide compliance analyzer service."""
    return ComplianceAnalyzerService()


@router.post("/assess", response_model=ComplianceAnalysisResponse)
async def analyze_ai_system(
    request: ComplianceAnalysisRequest,
    background_tasks: BackgroundTasks,
    analyzer: ComplianceAnalyzerService = Depends(get_compliance_analyzer)
):
    """
    Analyze AI system for EU AI Act compliance.
    
    Performs comprehensive compliance assessment and returns detailed report
    with risk categorization and recommendations.
    """
    start_time = time.time()
    analysis_id = str(uuid.uuid4())
    
    try:
        # Validate input
        if len(request.ai_system.description) < 10:
            raise HTTPException(
                status_code=400,
                detail="AI system description must be at least 10 characters"
            )
        
        if len(request.ai_system.description) > settings.MAX_ANALYSIS_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"AI system description exceeds maximum length of {settings.MAX_ANALYSIS_LENGTH}"
            )
        
        # Perform analysis
        report = await analyzer.analyze_system(request.ai_system)
        
        processing_time = time.time() - start_time
        
        # Log analysis for monitoring (background task)
        background_tasks.add_task(
            _log_analysis,
            analysis_id=analysis_id,
            system_id=request.ai_system.id,
            processing_time=processing_time,
            risk_category=report.risk_category,
            user_id=request.user_id
        )
        
        return ComplianceAnalysisResponse(
            success=True,
            report=report,
            analysis_id=analysis_id,
            processing_time_seconds=processing_time
        )
    
    except HTTPException:
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        
        # Log error
        background_tasks.add_task(
            _log_analysis_error,
            analysis_id=analysis_id,
            error=str(e),
            processing_time=processing_time
        )
        
        return ComplianceAnalysisResponse(
            success=False,
            error_message=f"Analysis failed: {str(e)}",
            analysis_id=analysis_id,
            processing_time_seconds=processing_time
        )


@router.get("/risk-categories", response_model=List[dict])
async def get_risk_categories():
    """Get list of EU AI Act risk categories with descriptions."""
    return [
        {
            "category": RiskCategory.UNACCEPTABLE,
            "title": "Unacceptable Risk",
            "description": "AI practices that are prohibited under the EU AI Act",
            "examples": [
                "Social scoring systems",
                "Real-time biometric identification in public spaces",
                "Emotion recognition in workplace/education",
                "Subliminal manipulation techniques"
            ]
        },
        {
            "category": RiskCategory.HIGH,
            "title": "High Risk", 
            "description": "AI systems subject to strict compliance requirements",
            "examples": [
                "Safety components in critical infrastructure",
                "Educational assessment systems",
                "Employment decision systems",
                "Essential service access systems",
                "Law enforcement applications"
            ]
        },
        {
            "category": RiskCategory.LIMITED,
            "title": "Limited Risk",
            "description": "AI systems with transparency obligations",
            "examples": [
                "Chatbots and conversational AI",
                "Emotion recognition systems",
                "Biometric categorization",
                "AI-generated content"
            ]
        },
        {
            "category": RiskCategory.MINIMAL,
            "title": "Minimal Risk",
            "description": "AI systems with no specific obligations under EU AI Act",
            "examples": [
                "AI-enabled video games",
                "Spam filters",
                "Inventory management systems",
                "Most other AI applications"
            ]
        }
    ]


@router.get("/domains", response_model=List[dict])
async def get_application_domains():
    """Get list of AI application domains for classification."""
    from app.models.compliance import AIApplicationDomain
    
    domain_descriptions = {
        AIApplicationDomain.BIOMETRIC_IDENTIFICATION: "Biometric identification and verification systems",
        AIApplicationDomain.CRITICAL_INFRASTRUCTURE: "Critical infrastructure safety and security",
        AIApplicationDomain.EDUCATION: "Educational and vocational training systems",
        AIApplicationDomain.EMPLOYMENT: "Employment, worker management, and recruitment",
        AIApplicationDomain.ESSENTIAL_SERVICES: "Essential private and public services access",
        AIApplicationDomain.LAW_ENFORCEMENT: "Law enforcement applications",
        AIApplicationDomain.MIGRATION_ASYLUM: "Migration, asylum and border control",
        AIApplicationDomain.JUSTICE_DEMOCRACY: "Administration of justice and democratic processes",
        AIApplicationDomain.HEALTHCARE: "Healthcare and medical applications",
        AIApplicationDomain.FINANCE: "Financial services and credit assessment",
        AIApplicationDomain.TRANSPORT: "Transportation and autonomous vehicles",
        AIApplicationDomain.ENERGY: "Energy grid and utilities management",
        AIApplicationDomain.SOCIAL_MEDIA: "Social media and content platforms",
        AIApplicationDomain.GAMING: "Gaming and entertainment",
        AIApplicationDomain.GENERAL_PURPOSE: "General purpose AI systems",
        AIApplicationDomain.OTHER: "Other applications not listed above"
    }
    
    return [
        {"domain": domain.value, "description": description}
        for domain, description in domain_descriptions.items()
    ]


@router.get("/report/{analysis_id}")
async def get_analysis_report(analysis_id: str):
    """
    Retrieve analysis report by ID.
    
    Note: This is a placeholder - in production, reports would be stored
    in database and retrieved by ID.
    """
    # TODO: Implement database storage and retrieval
    raise HTTPException(
        status_code=501,
        detail="Report retrieval not yet implemented. Reports are currently returned directly from analysis endpoint."
    )


@router.post("/validate")
async def validate_system_description(system: AISystemDescription):
    """
    Validate AI system description without performing full analysis.
    
    Useful for form validation in frontend.
    """
    try:
        # Pydantic validation happens automatically
        # Additional custom validation can be added here
        
        validation_results = {
            "valid": True,
            "warnings": [],
            "suggestions": []
        }
        
        # Add warnings for potential issues
        if len(system.description) < 100:
            validation_results["warnings"].append(
                "Description is quite short. More detail may improve analysis accuracy."
            )
        
        if not system.ai_techniques:
            validation_results["warnings"].append(
                "No AI techniques specified. This information helps with risk assessment."
            )
        
        if system.estimated_users and system.estimated_users > 1000000:
            validation_results["suggestions"].append(
                "Large user base detected. Consider additional privacy and safety measures."
            )
        
        return validation_results
    
    except Exception as e:
        return {
            "valid": False,
            "error": str(e),
            "warnings": [],
            "suggestions": []
        }


async def _log_analysis(
    analysis_id: str,
    system_id: str,
    processing_time: float,
    risk_category: RiskCategory,
    user_id: Optional[str] = None
):
    """Log successful analysis for monitoring and analytics."""
    # TODO: Implement actual logging to database or monitoring service
    print(f"Analysis completed: {analysis_id}, system: {system_id}, "
          f"time: {processing_time:.2f}s, risk: {risk_category}, user: {user_id}")


async def _log_analysis_error(
    analysis_id: str,
    error: str,
    processing_time: float
):
    """Log analysis error for debugging."""
    # TODO: Implement actual error logging
    print(f"Analysis failed: {analysis_id}, error: {error}, time: {processing_time:.2f}s")