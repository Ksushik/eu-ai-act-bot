#!/usr/bin/env python3
"""
EU AI Act Compliance Bot - CLI Tool

Command-line interface for testing compliance analysis functionality.
"""

import asyncio
import json
import sys
from typing import Optional
import argparse
from datetime import datetime

from app.models.compliance import (
    AISystemDescription, 
    AIApplicationDomain,
    DataType,
    DeploymentContext
)
from app.services.compliance_analyzer import ComplianceAnalyzerService


def create_sample_systems():
    """Create sample AI systems for testing."""
    return {
        "chatbot": AISystemDescription(
            name="Customer Service Chatbot",
            description="AI-powered chatbot for customer service inquiries on e-commerce website. Uses natural language processing to understand customer questions and provide automated responses. Does not make financial decisions or access sensitive data.",
            domain=AIApplicationDomain.GENERAL_PURPOSE,
            ai_techniques=["Natural Language Processing", "Intent Classification", "Response Generation"],
            data_types=[DataType.TEXT_DOCUMENTS, DataType.PUBLIC_DATA],
            deployment_context=DeploymentContext.ONLINE_PLATFORM,
            target_users="Website visitors and customers",
            geographic_scope=["EU", "US"],
            estimated_users=10000,
            development_stage="production",
            vendor_info="Internal development team"
        ),
        
        "hiring": AISystemDescription(
            name="Resume Screening System", 
            description="AI system for automated resume screening and candidate ranking in recruitment process. Analyzes resumes, extracts skills and experience, scores candidates based on job requirements. Used to filter applications before human review.",
            domain=AIApplicationDomain.EMPLOYMENT,
            ai_techniques=["Text Analysis", "Machine Learning Classification", "Scoring Algorithms"],
            data_types=[DataType.PERSONAL_DATA, DataType.TEXT_DOCUMENTS],
            deployment_context=DeploymentContext.WORKPLACE,
            target_users="HR recruiters and hiring managers",
            geographic_scope=["EU"],
            estimated_users=500,
            development_stage="production",
            vendor_info="Third-party vendor: RecruitTech Solutions"
        ),
        
        "medical": AISystemDescription(
            name="Medical Image Analysis",
            description="AI system for analyzing medical images (X-rays, MRIs) to assist radiologists in detecting anomalies and potential diseases. Provides probability scores for various conditions but does not make final diagnostic decisions. Requires physician oversight for all outputs.",
            domain=AIApplicationDomain.HEALTHCARE,
            ai_techniques=["Computer Vision", "Deep Learning", "Medical Image Processing"],
            data_types=[DataType.HEALTH_DATA, DataType.AUDIO_VISUAL, DataType.PERSONAL_DATA],
            deployment_context=DeploymentContext.HEALTHCARE_FACILITY,
            target_users="Radiologists and medical professionals",
            geographic_scope=["EU"],
            estimated_users=200,
            development_stage="testing",
            vendor_info="MedAI Technologies",
            regulatory_context="CE marking process initiated, GDPR compliance reviewed",
            risk_mitigation="Human physician oversight required for all outputs, encrypted data storage, access logs maintained"
        )
    }


async def analyze_system(system_name: str, system: AISystemDescription, verbose: bool = False):
    """Analyze a single AI system and display results."""
    
    print(f"\n{'='*60}")
    print(f"ANALYZING: {system.name}")
    print(f"{'='*60}")
    
    if verbose:
        print(f"\nSYSTEM DETAILS:")
        print(f"Domain: {system.domain}")
        print(f"Description: {system.description[:200]}...")
        print(f"AI Techniques: {', '.join(system.ai_techniques)}")
        print(f"Data Types: {', '.join([dt.value for dt in system.data_types])}")
        print(f"Deployment: {system.deployment_context}")
    
    # Initialize analyzer
    analyzer = ComplianceAnalyzerService()
    
    # Perform analysis
    start_time = datetime.now()
    report = await analyzer.analyze_system(system)
    analysis_time = (datetime.now() - start_time).total_seconds()
    
    # Display results
    print(f"\nCOMPLIANCE ASSESSMENT RESULTS:")
    print(f"Risk Category: {report.risk_category.value.upper()}")
    print(f"Compliance Score: {report.compliance_score:.2f}")
    print(f"Analysis Time: {analysis_time:.2f} seconds")
    
    print(f"\nEXECUTIVE SUMMARY:")
    print(report.executive_summary)
    
    print(f"\nKEY RISKS ({len(report.key_risks)}):")
    for i, risk in enumerate(report.key_risks, 1):
        print(f"{i}. {risk}")
    
    print(f"\nIMMEDIATE ACTIONS ({len(report.immediate_actions)}):")
    for i, action in enumerate(report.immediate_actions, 1):
        print(f"{i}. {action}")
    
    if verbose:
        print(f"\nDETAILED REQUIREMENTS ({len(report.requirement_assessments)}):")
        for req in report.requirement_assessments:
            print(f"- {req.title}: {req.status.value}")
            print(f"  Rationale: {req.rationale}")
        
        print(f"\nRECOMMENDATIONS ({len(report.recommendations)}):")
        for rec in report.recommendations:
            print(f"- [{rec.priority.upper()}] {rec.title}")
            print(f"  {rec.description}")
            print(f"  Timeline: {rec.timeline}")
            print(f"  Effort: {rec.estimated_effort}")
    
    return report


async def main():
    """Main CLI function."""
    
    parser = argparse.ArgumentParser(description="EU AI Act Compliance Analysis CLI")
    parser.add_argument(
        "system",
        nargs="?",
        choices=["chatbot", "hiring", "medical", "all"],
        default="all",
        help="AI system to analyze (default: all)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output with detailed analysis"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )
    parser.add_argument(
        "--save",
        type=str,
        help="Save results to specified file"
    )
    
    args = parser.parse_args()
    
    # Create sample systems
    systems = create_sample_systems()
    
    print("EU AI Act Compliance Bot - CLI Testing Tool")
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    if args.system == "all":
        # Analyze all systems
        for system_name, system_desc in systems.items():
            report = await analyze_system(system_name, system_desc, args.verbose)
            results[system_name] = report
    else:
        # Analyze specific system
        if args.system in systems:
            report = await analyze_system(args.system, systems[args.system], args.verbose)
            results[args.system] = {args.system: report}
        else:
            print(f"Error: Unknown system '{args.system}'")
            return 1
    
    # Handle JSON output
    if args.json:
        json_results = {}
        for name, report in results.items():
            json_results[name] = {
                "system_id": report.system_id,
                "risk_category": report.risk_category.value,
                "compliance_score": report.compliance_score,
                "generated_at": report.generated_at.isoformat(),
                "key_risks": report.key_risks,
                "immediate_actions": report.immediate_actions,
                "estimated_compliance_time": report.estimated_compliance_time
            }
        
        json_output = json.dumps(json_results, indent=2)
        
        if args.save:
            with open(args.save, 'w') as f:
                f.write(json_output)
            print(f"\nResults saved to: {args.save}")
        else:
            print("\nJSON OUTPUT:")
            print(json_output)
    
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*60}")
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)