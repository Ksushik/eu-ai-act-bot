"""
Test cases for EU AI Act Compliance Analyzer Service.
"""

import pytest
import asyncio
from datetime import datetime

from app.models.compliance import (
    AISystemDescription,
    RiskCategory,
    AIApplicationDomain,
    DataType,
    DeploymentContext,
    ComplianceStatus
)
from app.services.compliance_analyzer import ComplianceAnalyzerService


@pytest.fixture
def sample_chatbot():
    """Sample chatbot system for testing."""
    return AISystemDescription(
        name="Test Chatbot",
        description="A simple customer service chatbot that answers FAQ questions using natural language processing.",
        domain=AIApplicationDomain.GENERAL_PURPOSE,
        ai_techniques=["NLP", "Intent Classification"],
        data_types=[DataType.TEXT_DOCUMENTS],
        deployment_context=DeploymentContext.ONLINE_PLATFORM,
        target_users="Website visitors",
        geographic_scope=["EU"],
        development_stage="production"
    )


@pytest.fixture
def sample_hiring_system():
    """Sample hiring system for testing."""
    return AISystemDescription(
        name="Resume Screener",
        description="AI system that automatically screens resumes and ranks candidates for job openings based on qualifications and experience.",
        domain=AIApplicationDomain.EMPLOYMENT,
        ai_techniques=["Text Analysis", "Machine Learning"],
        data_types=[DataType.PERSONAL_DATA, DataType.TEXT_DOCUMENTS],
        deployment_context=DeploymentContext.WORKPLACE,
        target_users="HR recruiters",
        geographic_scope=["EU"],
        estimated_users=100,
        development_stage="production"
    )


@pytest.fixture
def analyzer():
    """Compliance analyzer service instance."""
    return ComplianceAnalyzerService()


class TestRiskCategorization:
    """Test risk categorization logic."""
    
    @pytest.mark.asyncio
    async def test_minimal_risk_chatbot(self, analyzer, sample_chatbot):
        """Test that basic chatbot is categorized as minimal risk."""
        risk = await analyzer._assess_risk_category(sample_chatbot)
        assert risk == RiskCategory.MINIMAL
    
    @pytest.mark.asyncio
    async def test_high_risk_employment(self, analyzer, sample_hiring_system):
        """Test that employment AI is categorized as high risk."""
        risk = await analyzer._assess_risk_category(sample_hiring_system)
        assert risk == RiskCategory.HIGH
    
    @pytest.mark.asyncio
    async def test_unacceptable_risk_social_scoring(self, analyzer):
        """Test that social scoring system is categorized as unacceptable."""
        social_scoring = AISystemDescription(
            name="Social Credit System",
            description="AI system for social scoring of citizens based on behavior and activities",
            domain=AIApplicationDomain.OTHER,
            ai_techniques=["Behavioral Analysis"],
            data_types=[DataType.BEHAVIORAL_DATA],
            deployment_context=DeploymentContext.PUBLIC_SPACE,
            target_users="Government",
            geographic_scope=["EU"],
            development_stage="concept"
        )
        
        risk = await analyzer._assess_risk_category(social_scoring)
        assert risk == RiskCategory.UNACCEPTABLE
    
    @pytest.mark.asyncio
    async def test_limited_risk_emotion_recognition(self, analyzer):
        """Test that emotion recognition is categorized as limited risk."""
        emotion_ai = AISystemDescription(
            name="Emotion Recognition App",
            description="Mobile app that uses emotion recognition to analyze user mood from photos",
            domain=AIApplicationDomain.SOCIAL_MEDIA,
            ai_techniques=["Computer Vision", "Emotion Recognition"],
            data_types=[DataType.AUDIO_VISUAL, DataType.BEHAVIORAL_DATA],
            deployment_context=DeploymentContext.MOBILE_APPLICATION,
            target_users="Mobile users",
            geographic_scope=["EU"],
            development_stage="development"
        )
        
        risk = await analyzer._assess_risk_category(emotion_ai)
        assert risk == RiskCategory.LIMITED


class TestComplianceAnalysis:
    """Test full compliance analysis workflow."""
    
    @pytest.mark.asyncio
    async def test_full_analysis_chatbot(self, analyzer, sample_chatbot):
        """Test complete analysis of chatbot system."""
        report = await analyzer.analyze_system(sample_chatbot)
        
        # Basic assertions
        assert report.system_id == sample_chatbot.id
        assert report.risk_category == RiskCategory.MINIMAL
        assert 0.0 <= report.compliance_score <= 1.0
        assert len(report.requirement_assessments) > 0
        assert len(report.recommendations) >= 0
        assert report.executive_summary is not None
        assert len(report.executive_summary) > 50  # Should be a substantial summary
        assert report.confidence_level in ["high", "medium", "low"]
    
    @pytest.mark.asyncio
    async def test_full_analysis_hiring_system(self, analyzer, sample_hiring_system):
        """Test complete analysis of high-risk hiring system."""
        report = await analyzer.analyze_system(sample_hiring_system)
        
        # High-risk systems should have more requirements
        assert report.risk_category == RiskCategory.HIGH
        assert len(report.requirement_assessments) > 3
        assert len(report.recommendations) > 0
        
        # Should have specific high-risk requirements
        requirement_ids = [req.requirement_id for req in report.requirement_assessments]
        assert "art9" in requirement_ids  # Risk management system
        assert "art13" in requirement_ids  # Transparency
        assert "art14" in requirement_ids  # Human oversight
    
    @pytest.mark.asyncio
    async def test_analysis_performance(self, analyzer, sample_chatbot):
        """Test that analysis completes within reasonable time."""
        start_time = datetime.now()
        report = await analyzer.analyze_system(sample_chatbot)
        analysis_time = (datetime.now() - start_time).total_seconds()
        
        # Analysis should complete within 5 seconds for testing
        assert analysis_time < 5.0
        assert report is not None


class TestRequirementAssessment:
    """Test requirement assessment logic."""
    
    @pytest.mark.asyncio
    async def test_get_applicable_requirements_minimal(self, analyzer, sample_chatbot):
        """Test requirements for minimal risk system."""
        requirements = await analyzer._get_applicable_requirements(
            sample_chatbot, RiskCategory.MINIMAL
        )
        
        # Minimal risk should have few requirements
        assert len(requirements) >= 1
        req_ids = [req["id"] for req in requirements]
        assert "gdpr_compliance" in req_ids
        assert "art9" not in req_ids  # High-risk requirement should not be present
    
    @pytest.mark.asyncio
    async def test_get_applicable_requirements_high(self, analyzer, sample_hiring_system):
        """Test requirements for high-risk system."""
        requirements = await analyzer._get_applicable_requirements(
            sample_hiring_system, RiskCategory.HIGH
        )
        
        # High-risk should have many requirements
        assert len(requirements) >= 6
        req_ids = [req["id"] for req in requirements]
        
        # Check for key high-risk requirements
        assert "art9" in req_ids   # Risk management
        assert "art10" in req_ids  # Data governance
        assert "art11" in req_ids  # Technical documentation
        assert "art12" in req_ids  # Record-keeping
        assert "art13" in req_ids  # Transparency
        assert "art14" in req_ids  # Human oversight


class TestRecommendationGeneration:
    """Test recommendation generation logic."""
    
    @pytest.mark.asyncio
    async def test_recommendation_prioritization(self, analyzer, sample_hiring_system):
        """Test that recommendations are properly prioritized."""
        report = await analyzer.analyze_system(sample_hiring_system)
        
        # Should have recommendations
        assert len(report.recommendations) > 0
        
        # Check priority levels
        priorities = [rec.priority for rec in report.recommendations]
        valid_priorities = {"critical", "high", "medium", "low"}
        assert all(p in valid_priorities for p in priorities)
        
        # High-risk systems should have high-priority recommendations
        assert any(p in ["critical", "high"] for p in priorities)
    
    @pytest.mark.asyncio
    async def test_immediate_actions_extraction(self, analyzer, sample_hiring_system):
        """Test extraction of immediate actions."""
        report = await analyzer.analyze_system(sample_hiring_system)
        
        # Should have immediate actions for high-risk system
        assert len(report.immediate_actions) > 0
        
        # Actions should be strings
        assert all(isinstance(action, str) for action in report.immediate_actions)
        assert all(len(action) > 10 for action in report.immediate_actions)


class TestComplianceScoring:
    """Test compliance scoring calculations."""
    
    def test_calculate_compliance_score_empty(self, analyzer):
        """Test compliance score with empty assessments."""
        score = analyzer._calculate_compliance_score([])
        assert score == 0.0
    
    def test_calculate_compliance_score_mixed(self, analyzer):
        """Test compliance score with mixed assessment results."""
        from app.models.compliance import RequirementAssessment
        
        assessments = [
            RequirementAssessment(
                requirement_id="req1",
                title="Test Requirement 1",
                description="Test",
                status=ComplianceStatus.COMPLIANT,
                rationale="Compliant"
            ),
            RequirementAssessment(
                requirement_id="req2", 
                title="Test Requirement 2",
                description="Test",
                status=ComplianceStatus.NON_COMPLIANT,
                rationale="Non-compliant"
            ),
            RequirementAssessment(
                requirement_id="req3",
                title="Test Requirement 3", 
                description="Test",
                status=ComplianceStatus.PARTIALLY_COMPLIANT,
                rationale="Partial"
            )
        ]
        
        score = analyzer._calculate_compliance_score(assessments)
        # Should be average: (1.0 + 0.0 + 0.5) / 3 = 0.5
        assert 0.4 <= score <= 0.6


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])