"""
EU AI Act Compliance Analyzer Service.

Core service for analyzing AI systems against EU AI Act requirements
using Claude LLM for intelligent assessment.
"""

from typing import List, Dict, Any, Optional
import asyncio
import json
import uuid
from datetime import datetime

from app.models.compliance import (
    AISystemDescription,
    ComplianceReport,
    RiskCategory,
    RequirementAssessment,
    Recommendation,
    ComplianceStatus,
    AIApplicationDomain
)
from app.core.config import settings


class ComplianceAnalyzerService:
    """Service for analyzing AI systems against EU AI Act compliance."""
    
    def __init__(self):
        """Initialize the compliance analyzer."""
        self.anthropic_client = None
        self.knowledge_base = None
        
        # TODO: Initialize actual services
        # self.anthropic_client = self._init_anthropic_client()
        # self.knowledge_base = self._init_knowledge_base()
    
    async def analyze_system(self, ai_system: AISystemDescription) -> ComplianceReport:
        """
        Perform comprehensive compliance analysis of AI system.
        
        Args:
            ai_system: AI system description to analyze
            
        Returns:
            ComplianceReport with detailed assessment and recommendations
        """
        # For MVP, use rule-based analysis
        # TODO: Replace with Claude LLM integration
        
        # Determine risk category
        risk_category = await self._assess_risk_category(ai_system)
        
        # Get applicable requirements
        requirements = await self._get_applicable_requirements(ai_system, risk_category)
        
        # Assess each requirement
        requirement_assessments = []
        for req in requirements:
            assessment = await self._assess_requirement(ai_system, req)
            requirement_assessments.append(assessment)
        
        # Generate recommendations
        recommendations = await self._generate_recommendations(ai_system, requirement_assessments)
        
        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(requirement_assessments)
        
        # Generate executive summary
        executive_summary = await self._generate_executive_summary(
            ai_system, risk_category, requirement_assessments, recommendations
        )
        
        return ComplianceReport(
            system_id=ai_system.id,
            risk_category=risk_category,
            compliance_score=compliance_score,
            requirement_assessments=requirement_assessments,
            recommendations=recommendations,
            executive_summary=executive_summary,
            key_risks=self._extract_key_risks(requirement_assessments),
            immediate_actions=self._extract_immediate_actions(recommendations),
            estimated_compliance_time=self._estimate_compliance_time(recommendations),
            confidence_level="medium"  # Rule-based analysis has medium confidence
        )
    
    async def _assess_risk_category(self, ai_system: AISystemDescription) -> RiskCategory:
        """Determine EU AI Act risk category based on system description."""
        
        # Unacceptable Risk indicators
        unacceptable_keywords = [
            "social scoring", "social credit", "subliminal", "manipulation",
            "real-time biometric identification", "public space surveillance",
            "emotion recognition workplace", "emotion recognition education"
        ]
        
        description_lower = ai_system.description.lower()
        
        if any(keyword in description_lower for keyword in unacceptable_keywords):
            return RiskCategory.UNACCEPTABLE
        
        # High Risk domains
        high_risk_domains = {
            AIApplicationDomain.CRITICAL_INFRASTRUCTURE,
            AIApplicationDomain.EDUCATION,
            AIApplicationDomain.EMPLOYMENT, 
            AIApplicationDomain.ESSENTIAL_SERVICES,
            AIApplicationDomain.LAW_ENFORCEMENT,
            AIApplicationDomain.MIGRATION_ASYLUM,
            AIApplicationDomain.JUSTICE_DEMOCRACY
        }
        
        if ai_system.domain in high_risk_domains:
            return RiskCategory.HIGH
        
        # Limited Risk indicators
        limited_risk_keywords = [
            "chatbot", "conversational ai", "emotion recognition",
            "biometric categorization", "generated content", "deepfake"
        ]
        
        if any(keyword in description_lower for keyword in limited_risk_keywords):
            return RiskCategory.LIMITED
        
        # Healthcare and Finance might be high or limited risk depending on use case
        if ai_system.domain in [AIApplicationDomain.HEALTHCARE, AIApplicationDomain.FINANCE]:
            # Simple heuristic: if involves decision-making, likely high risk
            decision_keywords = ["decision", "approval", "rejection", "assessment", "scoring"]
            if any(keyword in description_lower for keyword in decision_keywords):
                return RiskCategory.HIGH
            else:
                return RiskCategory.LIMITED
        
        # Default to minimal risk
        return RiskCategory.MINIMAL
    
    async def _get_applicable_requirements(
        self, 
        ai_system: AISystemDescription, 
        risk_category: RiskCategory
    ) -> List[Dict[str, Any]]:
        """Get applicable EU AI Act requirements based on risk category."""
        
        # Simplified requirement database
        # TODO: Replace with comprehensive knowledge base
        
        base_requirements = []
        
        if risk_category == RiskCategory.UNACCEPTABLE:
            base_requirements.extend([
                {
                    "id": "art5",
                    "title": "Article 5 - Prohibited AI Practices", 
                    "description": "AI systems with unacceptable risk are prohibited",
                    "mandatory": True
                }
            ])
        
        elif risk_category == RiskCategory.HIGH:
            base_requirements.extend([
                {
                    "id": "art9",
                    "title": "Article 9 - Risk Management System",
                    "description": "Establish, implement and maintain risk management system",
                    "mandatory": True
                },
                {
                    "id": "art10", 
                    "title": "Article 10 - Data and Data Governance",
                    "description": "Training, validation and testing data must meet quality criteria",
                    "mandatory": True
                },
                {
                    "id": "art11",
                    "title": "Article 11 - Technical Documentation",
                    "description": "Draw up technical documentation demonstrating compliance",
                    "mandatory": True
                },
                {
                    "id": "art12",
                    "title": "Article 12 - Record-keeping",
                    "description": "Keep logs automatically generated by high-risk AI systems",
                    "mandatory": True
                },
                {
                    "id": "art13",
                    "title": "Article 13 - Transparency and Information to Users",
                    "description": "Ensure sufficient transparency for users to interpret output",
                    "mandatory": True
                },
                {
                    "id": "art14",
                    "title": "Article 14 - Human Oversight",
                    "description": "Ensure appropriate human oversight measures",
                    "mandatory": True
                }
            ])
        
        elif risk_category == RiskCategory.LIMITED:
            base_requirements.extend([
                {
                    "id": "art52",
                    "title": "Article 52 - Transparency Obligations",
                    "description": "Inform users they are interacting with AI system",
                    "mandatory": True
                }
            ])
        
        # Add general requirements for all categories except unacceptable
        if risk_category != RiskCategory.UNACCEPTABLE:
            base_requirements.extend([
                {
                    "id": "gdpr_compliance",
                    "title": "GDPR Compliance",
                    "description": "Ensure compliance with GDPR for personal data processing",
                    "mandatory": True
                },
                {
                    "id": "cybersecurity",
                    "title": "Cybersecurity Measures", 
                    "description": "Implement appropriate cybersecurity measures",
                    "mandatory": False
                }
            ])
        
        return base_requirements
    
    async def _assess_requirement(
        self, 
        ai_system: AISystemDescription, 
        requirement: Dict[str, Any]
    ) -> RequirementAssessment:
        """Assess compliance with specific requirement."""
        
        # Simplified assessment logic
        # TODO: Implement Claude-based intelligent assessment
        
        req_id = requirement["id"]
        
        # Default assessment
        status = ComplianceStatus.REQUIRES_REVIEW
        rationale = "Requires detailed review based on system implementation"
        recommendations = []
        
        # Some basic heuristics
        if req_id == "art52" and "chatbot" in ai_system.description.lower():
            status = ComplianceStatus.REQUIRES_REVIEW
            rationale = "System appears to be conversational AI requiring transparency disclosure"
            recommendations.append("Implement clear disclosure that users are interacting with AI")
        
        elif req_id == "art9" and ai_system.risk_mitigation:
            status = ComplianceStatus.PARTIALLY_COMPLIANT
            rationale = "Risk mitigation measures mentioned but require formal risk management system"
            recommendations.append("Formalize risk management system per Article 9 requirements")
        
        elif req_id == "gdpr_compliance" and any("personal" in dt.value for dt in ai_system.data_types):
            status = ComplianceStatus.REQUIRES_REVIEW
            rationale = "System processes personal data, requiring GDPR compliance assessment"
            recommendations.extend([
                "Conduct GDPR compliance assessment",
                "Implement data subject rights procedures",
                "Ensure lawful basis for processing"
            ])
        
        return RequirementAssessment(
            requirement_id=req_id,
            title=requirement["title"],
            description=requirement["description"], 
            status=status,
            rationale=rationale,
            recommendations=recommendations
        )
    
    async def _generate_recommendations(
        self,
        ai_system: AISystemDescription,
        assessments: List[RequirementAssessment]
    ) -> List[Recommendation]:
        """Generate prioritized compliance recommendations."""
        
        recommendations = []
        
        # Extract recommendations from assessments
        for assessment in assessments:
            if assessment.status in [ComplianceStatus.NON_COMPLIANT, ComplianceStatus.REQUIRES_REVIEW]:
                for rec_text in assessment.recommendations:
                    recommendations.append(Recommendation(
                        title=f"Address {assessment.title}",
                        description=rec_text,
                        priority="high" if assessment.status == ComplianceStatus.NON_COMPLIANT else "medium",
                        category="legal",
                        estimated_effort="2-4 weeks",
                        timeline="Before production deployment",
                        references=[assessment.requirement_id]
                    ))
        
        # Add general recommendations based on risk category
        if ai_system.domain in [AIApplicationDomain.HEALTHCARE, AIApplicationDomain.FINANCE]:
            recommendations.append(Recommendation(
                title="Conduct Domain-Specific Risk Assessment",
                description="Perform thorough risk assessment specific to healthcare/financial applications",
                priority="high",
                category="technical",
                estimated_effort="3-6 weeks", 
                timeline="Before beta testing",
                references=["art9"]
            ))
        
        return recommendations[:10]  # Limit to top 10 recommendations
    
    def _calculate_compliance_score(self, assessments: List[RequirementAssessment]) -> float:
        """Calculate overall compliance score from requirement assessments."""
        
        if not assessments:
            return 0.0
        
        total_weight = 0
        weighted_score = 0
        
        for assessment in assessments:
            # Weight mandatory requirements higher
            weight = 1.0  # Base weight
            
            if assessment.status == ComplianceStatus.COMPLIANT:
                score = 1.0
            elif assessment.status == ComplianceStatus.PARTIALLY_COMPLIANT:
                score = 0.5
            elif assessment.status == ComplianceStatus.NOT_APPLICABLE:
                continue  # Skip in calculation
            else:  # NON_COMPLIANT or REQUIRES_REVIEW
                score = 0.0
            
            weighted_score += score * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        return weighted_score / total_weight
    
    async def _generate_executive_summary(
        self,
        ai_system: AISystemDescription,
        risk_category: RiskCategory,
        assessments: List[RequirementAssessment],
        recommendations: List[Recommendation]
    ) -> str:
        """Generate executive summary of compliance assessment."""
        
        non_compliant_count = sum(1 for a in assessments if a.status == ComplianceStatus.NON_COMPLIANT)
        review_required_count = sum(1 for a in assessments if a.status == ComplianceStatus.REQUIRES_REVIEW)
        high_priority_recs = sum(1 for r in recommendations if r.priority == "high")
        
        summary = f"""
The AI system '{ai_system.name}' has been classified as {risk_category.value.upper()} risk under the EU AI Act.

COMPLIANCE STATUS:
- {len(assessments)} requirements assessed
- {non_compliant_count} non-compliant areas identified
- {review_required_count} areas requiring detailed review
- {high_priority_recs} high-priority recommendations

KEY FINDINGS:
The system operates in the {ai_system.domain.value} domain, which carries specific regulatory obligations. 
{"Immediate action is required to address compliance gaps before deployment." if non_compliant_count > 0 else "The system shows promise for compliance but requires formal assessment and documentation."}

NEXT STEPS:
Focus on high-priority recommendations first, particularly around {', '.join(r.category for r in recommendations[:3] if r.priority == "high")}.
Estimated timeline for achieving compliance: {self._estimate_compliance_time(recommendations)}.
        """
        
        return summary.strip()
    
    def _extract_key_risks(self, assessments: List[RequirementAssessment]) -> List[str]:
        """Extract key risks from requirement assessments."""
        
        risks = []
        
        for assessment in assessments:
            if assessment.status in [ComplianceStatus.NON_COMPLIANT, ComplianceStatus.REQUIRES_REVIEW]:
                risks.append(f"{assessment.title}: {assessment.rationale}")
        
        return risks[:5]  # Top 5 risks
    
    def _extract_immediate_actions(self, recommendations: List[Recommendation]) -> List[str]:
        """Extract immediate actions from recommendations."""
        
        immediate = []
        
        for rec in recommendations:
            if rec.priority in ["critical", "high"]:
                immediate.append(rec.title)
        
        return immediate[:5]  # Top 5 immediate actions
    
    def _estimate_compliance_time(self, recommendations: List[Recommendation]) -> str:
        """Estimate time to achieve compliance based on recommendations."""
        
        if not recommendations:
            return "1-2 weeks"
        
        high_priority_count = sum(1 for r in recommendations if r.priority in ["critical", "high"])
        
        if high_priority_count >= 5:
            return "3-6 months"
        elif high_priority_count >= 3:
            return "6-12 weeks"
        else:
            return "2-6 weeks"