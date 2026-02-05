# Claude Implementation Guide - EU AI Act Compliance Bot

**Project:** EU AI Act Compliance Bot  
**Agent:** Claude Code  
**Implementation Partner:** Autonomous development system

## Project Overview

This project builds an automated EU AI Act compliance assessment tool. As Claude Code, you are responsible for implementing the technical architecture outlined in `ADR.md`.

## Your Role

You are the **primary development agent** for this project. Your responsibilities include:

1. **Code Generation:** Write all application code following best practices
2. **Architecture Implementation:** Translate ADR decisions into working code
3. **Documentation:** Maintain comprehensive docs and comments
4. **Testing:** Implement unit tests and integration tests
5. **Iteration:** Continuously improve based on testing and feedback

## Development Workflow

### Phase-Based Development
Follow the phases defined in ADR.md:
- **Phase 1:** Foundation & Analysis Engine
- **Phase 2:** Web Interface
- **Phase 3:** Advanced Features  
- **Phase 4:** Market Launch

### Sprint Structure
- **Sprint Length:** 1 week
- **Demo Day:** Every Friday
- **Retrospective:** Continuous improvement notes in `PROGRESS.md`

### Code Standards

**Python (Backend):**
```python
# Use type hints everywhere
def analyze_ai_system(description: str, risk_threshold: float) -> ComplianceReport:
    """Analyze AI system for EU AI Act compliance.
    
    Args:
        description: Technical description of the AI system
        risk_threshold: Risk assessment threshold (0.0-1.0)
        
    Returns:
        ComplianceReport with recommendations and risk assessment
    """
    pass

# Use dataclasses for structured data
@dataclass
class ComplianceReport:
    system_id: str
    risk_category: RiskCategory
    recommendations: List[str]
    compliance_score: float
    generated_at: datetime
```

**TypeScript (Frontend):**
```typescript
// Use strict TypeScript
interface AISystemInput {
  name: string;
  description: string;
  domain: AIApplicationDomain;
  dataTypes: DataType[];
  deploymentContext: DeploymentContext;
}

// Use React functional components with hooks
const ComplianceAnalyzer: React.FC<Props> = ({ onAnalysisComplete }) => {
  const [analysis, setAnalysis] = useState<ComplianceReport | null>(null);
  // Implementation
};
```

### File Structure
```
eu-ai-act-bot/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   └── services/
│   ├── tests/
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── lib/
│   │   └── types/
│   ├── public/
│   └── package.json
├── docs/
├── scripts/
├── ADR.md
├── claude.md
├── README.md
└── PROGRESS.md
```

## Core Implementation Requirements

### 1. EU AI Act Knowledge Base

**Objective:** Create searchable, semantic knowledge base of EU AI Act requirements

**Implementation approach:**
```python
class EUAIActKnowledgeBase:
    """Vector-based knowledge base for EU AI Act requirements."""
    
    def __init__(self, vector_db: VectorDB):
        self.vector_db = vector_db
        self.embeddings_model = "text-embedding-ada-002"  # or similar
    
    async def query_requirements(self, query: str) -> List[Requirement]:
        """Find relevant requirements for given query."""
        embeddings = await self.embed_text(query)
        results = await self.vector_db.similarity_search(embeddings, k=10)
        return [self.parse_requirement(r) for r in results]
    
    async def get_risk_category_rules(self, domain: str) -> List[RiskRule]:
        """Get risk categorization rules for specific AI application domain."""
        pass
```

### 2. Compliance Analysis Engine

**Objective:** Analyze AI systems against EU AI Act requirements using Claude

**Key components:**
- Risk categorization (Unacceptable, High, Limited, Minimal Risk)
- Requirement mapping
- Recommendation generation
- Compliance scoring

**Claude Integration:**
```python
class ComplianceAnalyzer:
    """Core analysis engine using Claude for compliance assessment."""
    
    def __init__(self, claude_client: AnthropicClient, knowledge_base: EUAIActKnowledgeBase):
        self.claude = claude_client
        self.kb = knowledge_base
    
    async def analyze_system(self, ai_system: AISystemDescription) -> ComplianceReport:
        """
        Perform comprehensive compliance analysis.
        
        Steps:
        1. Extract key features from system description
        2. Query relevant EU AI Act requirements
        3. Use Claude to assess compliance and risks
        4. Generate actionable recommendations
        """
        # Get relevant requirements
        requirements = await self.kb.query_requirements(ai_system.description)
        
        # Build analysis prompt
        prompt = self._build_analysis_prompt(ai_system, requirements)
        
        # Get Claude assessment
        analysis = await self.claude.complete(prompt)
        
        # Structure results
        return self._parse_compliance_report(analysis)
```

### 3. Web Interface Requirements

**Technology:** Next.js 14 + TypeScript + Tailwind + shadcn/ui

**Key pages:**
- Landing page with clear value proposition
- AI system input form (multi-step wizard)
- Compliance analysis dashboard
- Report generation and export
- User authentication and project management

**Component structure:**
```typescript
// Main analysis flow
<ComplianceWizard onComplete={handleAnalysisComplete}>
  <SystemDescriptionStep />
  <TechnicalDetailsStep />
  <DeploymentContextStep />
  <ReviewStep />
</ComplianceWizard>

// Results dashboard
<ComplianceDashboard report={complianceReport}>
  <RiskOverview />
  <RequirementsChecklist />
  <RecommendationsList />
  <ComplianceTimeline />
  <ExportOptions />
</ComplianceDashboard>
```

## Prompt Engineering Guidelines

### Analysis Prompts
Create structured prompts for compliance analysis:

```python
COMPLIANCE_ANALYSIS_PROMPT = """
You are an expert EU AI Act compliance advisor. Analyze the following AI system for regulatory compliance.

AI SYSTEM DETAILS:
{system_description}

RELEVANT EU AI ACT REQUIREMENTS:
{requirements_context}

ANALYSIS FRAMEWORK:
1. RISK CATEGORIZATION
   - Assess if system falls under: Unacceptable, High, Limited, or Minimal Risk
   - Provide specific reasoning based on EU AI Act Article 5-7

2. REQUIREMENT COMPLIANCE
   - Map system against applicable requirements
   - Identify compliance gaps and risks

3. RECOMMENDATIONS
   - Provide specific, actionable steps for compliance
   - Prioritize by impact and implementation difficulty

Format your response as structured JSON matching the ComplianceReport schema.
"""
```

## Testing Strategy

### Unit Tests
- Test all compliance logic with known cases
- Mock Claude API responses for consistent testing
- Test edge cases and error conditions

### Integration Tests
- End-to-end analysis workflows
- API endpoint testing
- Frontend user workflows

### Compliance Accuracy Tests
- Validate against legal expert assessments
- Test with real-world AI system examples
- Monitor for false positives/negatives

## Development Priorities

### Week 1: Foundation
1. **Day 1-2:** Set up project structure, basic FastAPI backend
2. **Day 3-4:** Implement EU AI Act knowledge base ingestion
3. **Day 5-7:** Create basic compliance analysis with Claude integration

### Week 2: Core Logic
1. **Day 1-2:** Refine analysis prompts and accuracy
2. **Day 3-4:** Build comprehensive test suite
3. **Day 5-7:** CLI tool for testing and validation

### Continuous Tasks
- **Daily:** Git commits with descriptive messages
- **Weekly:** Update PROGRESS.md with achievements and learnings
- **Bi-weekly:** Security and dependency updates

## Success Criteria

### Technical Quality
- [ ] 90%+ test coverage on core logic
- [ ] <500ms API response times
- [ ] Comprehensive error handling
- [ ] Security best practices implemented

### Compliance Accuracy
- [ ] Risk categorization accuracy >95%
- [ ] Recommendation relevance >90%
- [ ] No critical compliance misses in testing

### User Experience
- [ ] Intuitive workflow (complete analysis in <5 minutes)
- [ ] Clear, actionable recommendations
- [ ] Professional report generation

## Resources and References

### EU AI Act Documentation
- Official EU AI Act text and annexes
- Implementation guidelines (as published)
- Risk assessment frameworks

### Technical Resources
- Claude API documentation and best practices
- FastAPI and Next.js documentation
- Vector database integration guides

### Compliance Resources
- Legal tech best practices
- Regulatory compliance frameworks
- AI governance standards

## Next Actions

1. **Immediate:** Create GitHub repository and initial commit
2. **This week:** Implement Phase 1 foundation components
3. **Ongoing:** Maintain development log in PROGRESS.md

---

**Remember:** This is a high-value, time-sensitive project with significant market opportunity. Focus on shipping working software quickly while maintaining quality standards. The EU AI Act deadline creates urgency - companies need this tool NOW.