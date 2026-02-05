"""
Data models for EU AI Act compliance assessment.

Defines Pydantic models for AI system descriptions, compliance reports,
and related data structures.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
import uuid


class RiskCategory(str, Enum):
    """EU AI Act risk categories."""
    UNACCEPTABLE = "unacceptable"
    HIGH = "high" 
    LIMITED = "limited"
    MINIMAL = "minimal"


class AIApplicationDomain(str, Enum):
    """AI application domains for risk assessment."""
    BIOMETRIC_IDENTIFICATION = "biometric_identification"
    CRITICAL_INFRASTRUCTURE = "critical_infrastructure"
    EDUCATION = "education"
    EMPLOYMENT = "employment"
    ESSENTIAL_SERVICES = "essential_services"
    LAW_ENFORCEMENT = "law_enforcement"
    MIGRATION_ASYLUM = "migration_asylum"
    JUSTICE_DEMOCRACY = "justice_democracy"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    TRANSPORT = "transport"
    ENERGY = "energy"
    SOCIAL_MEDIA = "social_media"
    GAMING = "gaming"
    GENERAL_PURPOSE = "general_purpose"
    OTHER = "other"


class DataType(str, Enum):
    """Types of data processed by AI system."""
    PERSONAL_DATA = "personal_data"
    BIOMETRIC_DATA = "biometric_data"
    HEALTH_DATA = "health_data"
    FINANCIAL_DATA = "financial_data"
    BEHAVIORAL_DATA = "behavioral_data"
    LOCATION_DATA = "location_data"
    COMMUNICATION_DATA = "communication_data"
    AUDIO_VISUAL = "audio_visual"
    TEXT_DOCUMENTS = "text_documents"
    SENSOR_DATA = "sensor_data"
    PUBLIC_DATA = "public_data"


class DeploymentContext(str, Enum):
    """Context where AI system is deployed."""
    PUBLIC_SPACE = "public_space"
    WORKPLACE = "workplace"
    EDUCATIONAL_INSTITUTION = "educational_institution"
    HEALTHCARE_FACILITY = "healthcare_facility"
    ONLINE_PLATFORM = "online_platform"
    MOBILE_APPLICATION = "mobile_application"
    EMBEDDED_SYSTEM = "embedded_system"
    CLOUD_SERVICE = "cloud_service"
    PRIVATE_USE = "private_use"


class ComplianceStatus(str, Enum):
    """Compliance status for specific requirements."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    REQUIRES_REVIEW = "requires_review"
    NOT_APPLICABLE = "not_applicable"


class Recommendation(BaseModel):
    """Individual compliance recommendation."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., description="Brief recommendation title")
    description: str = Field(..., description="Detailed recommendation")
    priority: str = Field(..., regex="^(critical|high|medium|low)$")
    category: str = Field(..., description="Recommendation category (technical, process, legal)")
    estimated_effort: str = Field(..., description="Estimated implementation effort")
    timeline: str = Field(..., description="Suggested timeline for implementation")
    references: List[str] = Field(default=[], description="EU AI Act article references")


class RequirementAssessment(BaseModel):
    """Assessment of specific EU AI Act requirement."""
    requirement_id: str = Field(..., description="EU AI Act requirement identifier")
    title: str = Field(..., description="Requirement title")
    description: str = Field(..., description="Requirement description")
    status: ComplianceStatus = Field(..., description="Compliance status")
    rationale: str = Field(..., description="Rationale for assessment")
    evidence: Optional[str] = Field(None, description="Supporting evidence")
    recommendations: List[str] = Field(default=[], description="Specific recommendations for this requirement")


class AISystemDescription(BaseModel):
    """Description of AI system for compliance assessment."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=10, max_length=50000)
    domain: AIApplicationDomain = Field(..., description="Primary application domain")
    additional_domains: List[AIApplicationDomain] = Field(default=[], description="Additional domains")
    
    # Technical details
    ai_techniques: List[str] = Field(..., description="AI/ML techniques used")
    data_types: List[DataType] = Field(..., description="Types of data processed")
    deployment_context: DeploymentContext = Field(..., description="Deployment context")
    
    # Scope and impact
    target_users: str = Field(..., description="Target user groups")
    geographic_scope: List[str] = Field(..., description="Geographic deployment scope")
    estimated_users: Optional[int] = Field(None, ge=0, description="Estimated number of users")
    
    # Development details
    development_stage: str = Field(..., regex="^(concept|development|testing|production|discontinued)$")
    vendor_info: Optional[str] = Field(None, description="Vendor or development organization")
    
    # Additional context
    regulatory_context: Optional[str] = Field(None, description="Existing regulatory compliance")
    risk_mitigation: Optional[str] = Field(None, description="Existing risk mitigation measures")
    
    @validator('ai_techniques', 'data_types')
    def validate_non_empty_lists(cls, v):
        if not v:
            raise ValueError("At least one item must be specified")
        return v


class ComplianceReport(BaseModel):
    """Comprehensive compliance assessment report."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    system_id: str = Field(..., description="AI system identifier")
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Overall assessment
    risk_category: RiskCategory = Field(..., description="Overall risk category")
    compliance_score: float = Field(..., ge=0.0, le=1.0, description="Overall compliance score")
    
    # Detailed assessments
    requirement_assessments: List[RequirementAssessment] = Field(..., description="Individual requirement assessments")
    recommendations: List[Recommendation] = Field(..., description="Prioritized recommendations")
    
    # Summary
    executive_summary: str = Field(..., description="Executive summary of findings")
    key_risks: List[str] = Field(..., description="Key identified risks")
    immediate_actions: List[str] = Field(..., description="Immediate actions required")
    
    # Compliance timeline
    estimated_compliance_time: Optional[str] = Field(None, description="Estimated time to achieve compliance")
    critical_deadlines: List[Dict[str, Any]] = Field(default=[], description="Critical compliance deadlines")
    
    # Metadata
    analysis_version: str = Field(default="1.0", description="Analysis methodology version")
    confidence_level: str = Field(..., regex="^(high|medium|low)$", description="Confidence in assessment")
    
    @validator('requirement_assessments')
    def validate_requirements_not_empty(cls, v):
        if not v:
            raise ValueError("At least one requirement assessment must be provided")
        return v


class ComplianceAnalysisRequest(BaseModel):
    """Request model for compliance analysis."""
    ai_system: AISystemDescription = Field(..., description="AI system to analyze")
    analysis_options: Dict[str, Any] = Field(default={}, description="Analysis configuration options")
    user_id: Optional[str] = Field(None, description="User identifier for tracking")


class ComplianceAnalysisResponse(BaseModel):
    """Response model for compliance analysis."""
    success: bool = Field(..., description="Whether analysis completed successfully")
    report: Optional[ComplianceReport] = Field(None, description="Compliance report if successful")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    analysis_id: str = Field(..., description="Unique analysis identifier")
    processing_time_seconds: Optional[float] = Field(None, description="Time taken for analysis")