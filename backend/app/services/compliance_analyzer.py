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
        """Generate detailed, actionable compliance recommendations with implementation plans."""
        
        recommendations = []
        
        # Generate detailed recommendations based on specific requirements
        for assessment in assessments:
            if assessment.status in [ComplianceStatus.NON_COMPLIANT, ComplianceStatus.REQUIRES_REVIEW]:
                detailed_recs = self._get_detailed_requirement_plan(assessment, ai_system)
                recommendations.extend(detailed_recs)
        
        # Add domain-specific comprehensive recommendations
        domain_recs = self._get_domain_specific_recommendations(ai_system)
        recommendations.extend(domain_recs)
        
        # Sort by priority and return
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        recommendations.sort(key=lambda r: priority_order.get(r.priority, 4))
        
        return recommendations[:15]  # Return top 15 detailed recommendations
    
    def _get_detailed_requirement_plan(
        self, 
        assessment: RequirementAssessment, 
        ai_system: AISystemDescription
    ) -> List[Recommendation]:
        """Generate detailed implementation plan for specific requirement."""
        
        req_id = assessment.requirement_id
        recommendations = []
        
        # Article 9 - Risk Management System
        if req_id == "art9":
            recommendations.extend([
                Recommendation(
                    title="Establish Risk Management Framework",
                    description=f"""
STEP-BY-STEP IMPLEMENTATION:

1. RISK IDENTIFICATION (Week 1-2):
   • Document all potential risks for {ai_system.domain.value} AI systems
   • Identify bias, discrimination, privacy, security, and safety risks
   • Map risks to potential harms to individuals/groups
   • Tools needed: Risk assessment templates, stakeholder workshops
   
2. RISK ASSESSMENT (Week 2-3):
   • Quantify likelihood and severity of each identified risk
   • Use industry-standard risk scoring (1-5 scale)
   • Consider residual risks after current mitigation measures
   
3. RISK MITIGATION (Week 3-6):
   • Design specific controls for each high/medium risk
   • Implement technical measures (input validation, output filtering)
   • Establish procedural controls (human oversight, escalation)
   • Document all mitigation strategies
   
4. MONITORING & REVIEW (Ongoing):
   • Set up automated monitoring dashboards
   • Schedule quarterly risk reviews
   • Update risk assessment when system changes

DELIVERABLES:
   ✓ Risk Management Plan (30-50 pages)
   ✓ Risk Register with 20+ identified risks
   ✓ Mitigation Controls Matrix
   ✓ Monitoring Dashboard
   
ESTIMATED COST: €25,000-50,000
RESPONSIBLE: Chief Risk Officer + AI Team
EXTERNAL HELP: EU AI Act consultant (€150-300/hour, 40-60 hours)
                    """,
                    priority="critical",
                    category="governance",
                    estimated_effort="4-6 weeks",
                    timeline="Must complete before system deployment",
                    references=["art9"]
                ),
                Recommendation(
                    title="Risk Management System Audit",
                    description=f"""
THIRD-PARTY VALIDATION PLAN:

1. SELECT AUDITOR (Week 1):
   • Choose EU AI Act certified consultant
   • Ensure expertise in {ai_system.domain.value} domain
   • Verify ISO 27001/31000 risk management experience
   
2. AUDIT SCOPE (Week 2):
   • Review risk management documentation
   • Test risk identification completeness
   • Validate mitigation effectiveness
   • Check monitoring systems
   
3. REMEDIATION (Week 3-4):
   • Address audit findings
   • Update documentation gaps
   • Strengthen weak controls
   
EXPECTED FINDINGS:
   • 5-10 documentation gaps
   • 2-3 control weaknesses
   • Recommendations for improvement
   
COST BREAKDOWN:
   • Audit fees: €15,000-25,000
   • Remediation work: €10,000-15,000
   • Follow-up assessment: €5,000
                    """,
                    priority="high",
                    category="audit",
                    estimated_effort="3-4 weeks",
                    timeline="After risk framework completion",
                    references=["art9", "art43"]
                )
            ])
        
        # Article 10 - Data Governance
        elif req_id == "art10":
            recommendations.extend([
                Recommendation(
                    title="Comprehensive Data Governance Program",
                    description=f"""
DATA QUALITY IMPLEMENTATION ROADMAP:

PHASE 1 - DATA INVENTORY (Week 1-2):
   • Catalog all training/validation/test datasets
   • Document data sources, collection methods, dates
   • Map personal data elements (if any)
   • Assess data representative-ness for target population
   
PHASE 2 - BIAS TESTING (Week 3-4):
   • Statistical bias analysis across protected characteristics
   • Performance disparities testing (accuracy, false positive rates)
   • Intersectional bias analysis
   • Tools: Fairlearn, AI Fairness 360, custom analysis
   
PHASE 3 - DATA QUALITY CONTROLS (Week 4-6):
   • Data validation pipelines
   • Outlier detection systems  
   • Data drift monitoring
   • Version control for datasets
   
PHASE 4 - DOCUMENTATION (Week 6-8):
   • Data sheets for datasets (10-15 pages each)
   • Data lineage documentation
   • Bias testing reports
   • Data governance procedures
   
SPECIFIC FOR {ai_system.domain.value.upper()} DOMAIN:
   {"• Healthcare data anonymization (HIPAA + GDPR compliance)" if ai_system.domain.value == "healthcare" else ""}
   {"• Financial data protection (PCI DSS compliance)" if ai_system.domain.value == "finance" else ""}
   {"• Employment data bias testing (multiple protected classes)" if ai_system.domain.value == "employment" else ""}
   
DELIVERABLES:
   ✓ Data Governance Policy (20+ pages)
   ✓ Bias Testing Report with statistical analysis
   ✓ Data Quality Dashboard
   ✓ Dataset Documentation Package
   
BUDGET BREAKDOWN:
   • Data scientist time: €40,000-60,000
   • Bias testing tools: €10,000-15,000
   • External data audit: €20,000-30,000
   • Documentation: €5,000-10,000
   TOTAL: €75,000-115,000
                    """,
                    priority="critical", 
                    category="data",
                    estimated_effort="6-8 weeks",
                    timeline="Before model training completion",
                    references=["art10"]
                )
            ])
        
        # Article 52 - Transparency (for chatbots/conversational AI)
        elif req_id == "art52" and "chatbot" in ai_system.description.lower():
            recommendations.extend([
                Recommendation(
                    title="AI Disclosure Implementation - Complete UX Design",
                    description=f"""
TRANSPARENCY IMPLEMENTATION PLAN:

PHASE 1 - LEGAL COMPLIANCE (Week 1):
   • Draft disclosure text with legal team
   • Review GDPR Article 22 requirements
   • Ensure compliance with local consumer protection laws
   
PHASE 2 - UX DESIGN (Week 1-2):
   • Design clear, prominent AI disclosure
   • A/B test different disclosure formats
   • Ensure accessibility compliance (WCAG 2.1 AA)
   • Test with diverse user groups
   
DISCLOSURE EXAMPLES:
   🤖 "You're chatting with an AI assistant"
   ⚡ "This is an automated AI service" 
   💬 "AI-powered chat - human agents available if needed"
   
IMPLEMENTATION CHECKLIST:
   ✓ Disclosure appears within 3 seconds of interaction
   ✓ Visible on all conversation interfaces
   ✓ Available in multiple languages (if serving EU)
   ✓ Screen reader compatible
   ✓ Cannot be easily dismissed or hidden
   ✓ Includes option to speak with human (if applicable)
   
TECHNICAL IMPLEMENTATION:
   • Frontend: Add disclosure component to chat widget
   • Backend: Log disclosure acknowledgments  
   • Analytics: Track user response to disclosure
   • Testing: Automated compliance checks
   
COST BREAKDOWN:
   • UX design work: €3,000-5,000
   • Frontend development: €5,000-8,000
   • Legal review: €2,000-3,000
   • User testing: €2,000-3,000
   • TOTAL: €12,000-19,000
   
TIMELINE: 2 weeks (fast-track implementation possible)
RESPONSIBLE: Product + Legal + UX teams
                    """,
                    priority="high",
                    category="transparency",
                    estimated_effort="2 weeks",
                    timeline="Before customer-facing deployment",
                    references=["art52"]
                )
            ])
        
        # GDPR Compliance for AI
        elif req_id == "gdpr_compliance":
            recommendations.extend([
                Recommendation(
                    title="GDPR-AI Integration Compliance Program",
                    description=f"""
GDPR + AI ACT COMBINED COMPLIANCE:

PHASE 1 - DATA MAPPING (Week 1-2):
   • Map all personal data flows in AI system
   • Identify data controllers vs processors
   • Document international data transfers
   • Assess special category data usage
   
PHASE 2 - LEGAL BASIS ANALYSIS (Week 2-3):
   • Establish lawful basis for each processing activity
   • Document legitimate interests assessments (if applicable)
   • Review consent mechanisms (if consent-based)
   • Ensure Article 22 compliance for automated decisions
   
PHASE 3 - DATA SUBJECT RIGHTS (Week 3-5):
   • Implement right of access procedures
   • Design data portability mechanisms
   • Create erasure ("right to be forgotten") workflows
   • Handle rectification requests
   
PHASE 4 - ACCOUNTABILITY (Week 5-6):
   • Data Protection Impact Assessment (DPIA)
   • Processing records (Article 30)
   • Data processor agreements
   • Breach notification procedures
   
AI-SPECIFIC GDPR CONSIDERATIONS:
   • Algorithmic transparency requirements
   • Automated decision-making safeguards
   • Data minimization for AI training
   • Model explainability capabilities
   
DELIVERABLES:
   ✓ GDPR-AI Compliance Manual (40+ pages)
   ✓ Data Protection Impact Assessment
   ✓ Privacy Policy updates
   ✓ Data subject rights procedures
   ✓ Staff training materials
   
COST ESTIMATE:
   • Data protection lawyer: €25,000-40,000
   • Privacy engineer: €20,000-30,000
   • DPIA consultant: €10,000-15,000
   • Technical implementation: €15,000-25,000
   TOTAL: €70,000-110,000
                    """,
                    priority="critical",
                    category="privacy",
                    estimated_effort="5-6 weeks", 
                    timeline="Before processing any personal data",
                    references=["gdpr", "art22"]
                )
            ])
        
        return recommendations
    
    def _get_domain_specific_recommendations(self, ai_system: AISystemDescription) -> List[Recommendation]:
        """Generate recommendations specific to application domain."""
        
        domain_recs = []
        
        if ai_system.domain == AIApplicationDomain.EMPLOYMENT:
            domain_recs.extend([
                Recommendation(
                    title="Employment AI - Bias Mitigation & Fairness Testing",
                    description="""
EMPLOYMENT AI SPECIFIC COMPLIANCE:

BIAS TESTING REQUIREMENTS:
• Test for discrimination across protected characteristics:
  - Gender, race, age, disability status
  - Intersectional bias (e.g., age + gender)
  - Geographic bias (postal code discrimination)
  
FAIRNESS METRICS TO IMPLEMENT:
• Equal opportunity (false negative rate parity)
• Predictive parity (precision parity) 
• Calibration (outcome base rates)
• Individual fairness (similar candidates get similar scores)

AUDIT PROCEDURES:
• Monthly bias testing with new data
• Annual third-party fairness audit
• Candidate feedback collection & analysis
• Adverse impact analysis (80% rule)

TRANSPARENCY FOR CANDIDATES:
• Explain AI system use in job postings
• Provide meaningful information about decision factors
• Offer human review option
• Document appeals process

COST: €50,000-80,000 for comprehensive bias testing framework
TIMELINE: 3-4 months for full implementation
                    """,
                    priority="critical",
                    category="fairness",
                    estimated_effort="12-16 weeks",
                    timeline="Before any hiring decisions",
                    references=["art14", "gdpr_art22"]
                )
            ])
        
        elif ai_system.domain == AIApplicationDomain.HEALTHCARE:
            domain_recs.extend([
                Recommendation(
                    title="Healthcare AI - Clinical Validation & Safety",
                    description="""
HEALTHCARE AI COMPLIANCE PROGRAM:

CLINICAL VALIDATION:
• Design clinical studies for AI performance
• Statistical validation with diverse patient populations
• Comparison with standard of care
• Real-world evidence collection

MEDICAL DEVICE REGULATION (MDR):
• CE marking process (12-18 months)
• Clinical evidence requirements
• Post-market surveillance plan
• Risk management per ISO 14971

SAFETY REQUIREMENTS:
• Patient safety monitoring
• Adverse event reporting
• Clinical risk assessment
• Human oversight protocols

ESTIMATED COSTS:
• Clinical studies: €200,000-500,000
• CE marking process: €100,000-300,000
• Quality management system: €50,000-100,000

TIMELINE: 18-24 months for full market authorization
                    """,
                    priority="critical",
                    category="clinical",
                    estimated_effort="18-24 months",
                    timeline="Before clinical deployment",
                    references=["mdr", "art43"]
                )
            ])
        
        return domain_recs
    
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