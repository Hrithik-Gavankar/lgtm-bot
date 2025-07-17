"""
AI-Powered Review Engine

Evaluates PR code against Jira acceptance criteria using AI for intelligent analysis.
"""

import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

from jira_parser import JiraTicketInfo
from pr_analyzer import PRDiff

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReviewStatus(Enum):
    """Review result status."""
    PASS = "pass"
    FAIL = "fail"
    CONDITIONAL = "conditional"

@dataclass
class ReviewResult:
    """Complete review result."""
    status: ReviewStatus
    overall_score: float  # 0.0 to 1.0
    lgtm_comment: Optional[str]
    summary: str
    acceptance_criteria_analysis: List[Dict[str, Any]]
    code_quality_issues: List[Dict[str, Any]]
    test_analysis: Dict[str, Any]
    suggestions: List[str]
    required_changes: List[str]
    recommended_tests: List[str]

class ReviewEngine:
    """AI-powered code review engine."""
    
    def __init__(self, provider: str = "anthropic", model: str = None, api_key: str = None, base_url: str = None):
        """
        Initialize AI client.
        
        Args:
            provider: AI provider ("anthropic", "openai", or "ollama")
            model: Model name
            api_key: API key for the provider (not needed for ollama)
            base_url: Base URL for the provider (for ollama: http://localhost:11434/v1)
        """
        self.provider = provider.lower()
        self.model = model
        self.base_url = base_url
        self.api_key = api_key or self._get_api_key()
        self.client = self._initialize_client()
    
    def _get_api_key(self) -> str:
        """Get API key from environment variables."""
        if self.provider == "anthropic":
            return os.getenv("ANTHROPIC_API_KEY") or ""
        elif self.provider == "openai":
            return os.getenv("OPENAI_API_KEY") or ""
        elif self.provider == "ollama":
            return "ollama"  # Ollama doesn't require an API key
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    def _initialize_client(self):
        """Initialize the AI client."""
        if self.provider == "anthropic":
            if not HAS_ANTHROPIC:
                raise ImportError("anthropic package not installed")
            return anthropic.Anthropic(api_key=self.api_key)
        elif self.provider == "openai":
            if not HAS_OPENAI:
                raise ImportError("openai package not installed")
            return openai.OpenAI(api_key=self.api_key)
        elif self.provider == "ollama":
            if not HAS_OPENAI:
                raise ImportError("openai package not installed (required for ollama compatibility)")
            # Use OpenAI client with custom base URL for Ollama
            base_url = self.base_url or "http://localhost:11434/v1"
            return openai.OpenAI(
                api_key="ollama",  # Ollama doesn't require a real API key
                base_url=base_url
            )
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    def review_pr(self, ticket_info: JiraTicketInfo, pr_diff: PRDiff, 
                  code_quality_analysis: Dict[str, Any]) -> ReviewResult:
        """
        Perform comprehensive PR review against ticket requirements.
        
        Args:
            ticket_info: Jira ticket information
            pr_diff: PR diff information
            code_quality_analysis: Code quality analysis results
            
        Returns:
            Complete review result
        """
        logger.info(f"Starting review for PR #{pr_diff.pr_number} against ticket {ticket_info.ticket_key}")
        
        # Analyze acceptance criteria fulfillment
        ac_analysis = self._analyze_acceptance_criteria(ticket_info, pr_diff)
        
        # Perform AI-powered code review
        ai_review = self._ai_code_review(ticket_info, pr_diff)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(ac_analysis, code_quality_analysis, ai_review)
        
        # Determine status
        status = self._determine_status(overall_score, ac_analysis, code_quality_analysis)
        
        # Generate recommendations
        suggestions = self._generate_suggestions(ac_analysis, code_quality_analysis, ai_review)
        required_changes = self._identify_required_changes(ac_analysis, code_quality_analysis)
        recommended_tests = self._recommend_tests(ticket_info, pr_diff, code_quality_analysis)
        
        # Generate LGTM comment
        lgtm_comment = self._generate_lgtm_comment(status, overall_score) if status == ReviewStatus.PASS else None
        
        # Create summary
        summary = self._create_summary(status, overall_score, ac_analysis, code_quality_analysis)
        
        return ReviewResult(
            status=status,
            overall_score=overall_score,
            lgtm_comment=lgtm_comment,
            summary=summary,
            acceptance_criteria_analysis=ac_analysis,
            code_quality_issues=code_quality_analysis.get("issues", []),
            test_analysis=code_quality_analysis.get("test_coverage", {}),
            suggestions=suggestions,
            required_changes=required_changes,
            recommended_tests=recommended_tests
        )
    
    def _analyze_acceptance_criteria(self, ticket_info: JiraTicketInfo, pr_diff: PRDiff) -> List[Dict[str, Any]]:
        """Analyze how well the PR fulfills acceptance criteria."""
        ac_analysis = []
        
        for i, criterion in enumerate(ticket_info.acceptance_criteria):
            # Use AI to analyze each criterion
            analysis = self._ai_analyze_criterion(criterion, pr_diff)
            
            ac_analysis.append({
                "criterion": criterion,
                "fulfilled": analysis.get("fulfilled", False),
                "confidence": analysis.get("confidence", 0.5),
                "evidence": analysis.get("evidence", []),
                "gaps": analysis.get("gaps", []),
                "reasoning": analysis.get("reasoning", "")
            })
        
        return ac_analysis
    
    def _ai_analyze_criterion(self, criterion: str, pr_diff: PRDiff) -> Dict[str, Any]:
        """Use AI to analyze if a specific criterion is fulfilled."""
        prompt = self._build_criterion_analysis_prompt(criterion, pr_diff)
        
        try:
            response = self._call_ai(prompt)
            return self._parse_criterion_response(response)
        except Exception as e:
            logger.error(f"AI analysis failed for criterion: {e}")
            return {
                "fulfilled": False,
                "confidence": 0.0,
                "evidence": [],
                "gaps": [f"Analysis failed: {str(e)}"],
                "reasoning": "Could not analyze due to AI service error"
            }
    
    def _ai_code_review(self, ticket_info: JiraTicketInfo, pr_diff: PRDiff) -> Dict[str, Any]:
        """Perform AI-powered general code review."""
        prompt = self._build_code_review_prompt(ticket_info, pr_diff)
        
        try:
            response = self._call_ai(prompt)
            return self._parse_code_review_response(response)
        except Exception as e:
            logger.error(f"AI code review failed: {e}")
            return {
                "security_issues": [],
                "performance_concerns": [],
                "maintainability_issues": [],
                "positive_aspects": [],
                "overall_assessment": "Review failed due to AI service error"
            }
    
    def _build_criterion_analysis_prompt(self, criterion: str, pr_diff: PRDiff) -> str:
        """Build prompt for analyzing a specific acceptance criterion."""
        # Get relevant file changes (limit to avoid token limits)
        relevant_changes = []
        for file_change in pr_diff.file_changes[:10]:  # Limit to first 10 files
            if file_change.patch:
                relevant_changes.append(f"File: {file_change.filename}\n{file_change.patch[:1000]}")  # Limit patch size
        
        changes_text = "\n\n".join(relevant_changes)
        
        return f"""
You are a senior code reviewer analyzing a pull request against specific acceptance criteria.

**Acceptance Criterion to Evaluate:**
{criterion}

**Pull Request Information:**
- Title: {pr_diff.title}
- Description: {pr_diff.description[:500]}...
- Files Changed: {pr_diff.total_files_changed}
- Additions: +{pr_diff.total_additions}, Deletions: -{pr_diff.total_deletions}

**Code Changes (relevant excerpts):**
{changes_text}

**Instructions:**
Analyze whether this pull request fulfills the specific acceptance criterion above.

Respond in JSON format:
{{
    "fulfilled": true/false,
    "confidence": 0.0-1.0,
    "evidence": ["specific evidence from code that supports fulfillment"],
    "gaps": ["specific missing elements or concerns"],
    "reasoning": "detailed explanation of your analysis"
}}

Be specific and reference actual code changes where possible.
"""
    
    def _build_code_review_prompt(self, ticket_info: JiraTicketInfo, pr_diff: PRDiff) -> str:
        """Build prompt for general code review."""
        return f"""
You are a senior software engineer performing a comprehensive code review.

**Context:**
- Jira Ticket: {ticket_info.ticket_key} - {ticket_info.summary}
- Problem: {ticket_info.problem_description[:300]}
- PR: #{pr_diff.pr_number} - {pr_diff.title}

**Key Areas to Review:**
1. Security vulnerabilities
2. Performance implications  
3. Code maintainability and readability
4. Error handling
5. Edge cases
6. Architecture decisions

**Files Changed:** {[f.filename for f in pr_diff.file_changes[:10]]}

Provide a structured analysis in JSON format:
{{
    "security_issues": ["list of security concerns"],
    "performance_concerns": ["list of performance issues"], 
    "maintainability_issues": ["list of maintainability problems"],
    "positive_aspects": ["list of good practices found"],
    "overall_assessment": "summary assessment"
}}

Focus on actionable feedback and specific improvements.
"""
    
    def _call_ai(self, prompt: str) -> str:
        """Call the AI service with the given prompt."""
        if self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model or "claude-3-sonnet-20240229",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        
        elif self.provider in ["openai", "ollama"]:
            # Default models for each provider
            default_model = "gpt-4" if self.provider == "openai" else "llama3.2:latest"
            model_name = self.model or default_model
            
            response = self.client.chat.completions.create(
                model=model_name,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content or ""
        
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    def _parse_criterion_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for criterion analysis."""
        try:
            import json
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback parsing
            return {
                "fulfilled": "fulfilled" in response.lower(),
                "confidence": 0.5,
                "evidence": [],
                "gaps": ["Could not parse AI response"],
                "reasoning": response[:200] + "..."
            }
    
    def _parse_code_review_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for code review."""
        try:
            import json
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "security_issues": [],
                "performance_concerns": [],
                "maintainability_issues": [],
                "positive_aspects": [],
                "overall_assessment": response[:200] + "..."
            }
    
    def _calculate_overall_score(self, ac_analysis: List[Dict], code_quality: Dict, ai_review: Dict) -> float:
        """Calculate overall review score (0.0 to 1.0)."""
        # Acceptance criteria score (40% weight)
        ac_score = 0.0
        if ac_analysis:
            fulfilled_count = sum(1 for ac in ac_analysis if ac["fulfilled"])
            confidence_avg = sum(ac["confidence"] for ac in ac_analysis) / len(ac_analysis)
            ac_score = (fulfilled_count / len(ac_analysis)) * confidence_avg
        
        # Code quality score (30% weight)
        quality_score = 1.0
        total_issues = code_quality.get("summary", {}).get("total_issues", 0)
        if total_issues > 0:
            quality_score = max(0.0, 1.0 - (total_issues * 0.1))  # Reduce by 10% per issue
        
        # Test coverage score (20% weight)
        test_score = 1.0 if code_quality.get("summary", {}).get("has_tests", False) else 0.3
        
        # AI review score (10% weight)
        ai_score = 0.8  # Default decent score if AI review works
        ai_issues = len(ai_review.get("security_issues", [])) + len(ai_review.get("performance_concerns", []))
        if ai_issues > 0:
            ai_score = max(0.0, 0.8 - (ai_issues * 0.1))
        
        # Weighted average
        overall_score = (ac_score * 0.4) + (quality_score * 0.3) + (test_score * 0.2) + (ai_score * 0.1)
        return min(1.0, max(0.0, overall_score))
    
    def _determine_status(self, overall_score: float, ac_analysis: List[Dict], code_quality: Dict) -> ReviewStatus:
        """Determine the review status based on analysis."""
        # Critical failures
        if code_quality.get("summary", {}).get("total_issues", 0) > 5:
            return ReviewStatus.FAIL
        
        unfulfilled_critical = sum(1 for ac in ac_analysis if not ac["fulfilled"] and ac["confidence"] > 0.7)
        if unfulfilled_critical > 0:
            return ReviewStatus.FAIL
        
        # Pass threshold
        if overall_score >= 0.8:
            return ReviewStatus.PASS
        elif overall_score >= 0.6:
            return ReviewStatus.CONDITIONAL
        else:
            return ReviewStatus.FAIL
    
    def _generate_suggestions(self, ac_analysis: List[Dict], code_quality: Dict, ai_review: Dict) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []
        
        # From acceptance criteria
        for ac in ac_analysis:
            if not ac["fulfilled"] and ac["gaps"]:
                suggestions.extend(ac["gaps"])
        
        # From code quality
        for smell in code_quality.get("code_smells", []):
            suggestions.append(f"{smell['file']}: {smell['message']}")
        
        # From AI review
        suggestions.extend(ai_review.get("maintainability_issues", []))
        suggestions.extend(ai_review.get("performance_concerns", []))
        
        return suggestions[:10]  # Limit to top 10
    
    def _identify_required_changes(self, ac_analysis: List[Dict], code_quality: Dict) -> List[str]:
        """Identify required changes for approval."""
        required = []
        
        # Critical AC failures
        for ac in ac_analysis:
            if not ac["fulfilled"] and ac["confidence"] > 0.8:
                required.append(f"Must fulfill: {ac['criterion']}")
        
        # Critical quality issues
        critical_issues = [issue for issue in code_quality.get("issues", []) 
                          if issue.get("type") == "fail_keyword"]
        if critical_issues:
            required.append("Remove debugging/temporary code (TODO, FIXME, console.log, etc.)")
        
        return required
    
    def _recommend_tests(self, ticket_info: JiraTicketInfo, pr_diff: PRDiff, code_quality: Dict) -> List[str]:
        """Recommend specific test cases."""
        recommendations = []
        
        if not code_quality.get("test_coverage", {}).get("has_test_files", False):
            recommendations.append("Add unit tests for the main functionality")
        
        # Based on acceptance criteria
        for criterion in ticket_info.acceptance_criteria:
            recommendations.append(f"Test case for: {criterion[:50]}...")
        
        # Based on file changes
        for file_change in pr_diff.file_changes:
            if not file_change.is_test_file and file_change.status == "added":
                recommendations.append(f"Add tests for new file: {file_change.filename}")
        
        return recommendations[:5]  # Limit to top 5
    
    def _generate_lgtm_comment(self, status: ReviewStatus, score: float) -> Optional[str]:
        """Generate LGTM comment for approved PRs."""
        if status != ReviewStatus.PASS:
            return None
        
        if score >= 0.95:
            return "LGTM! 🚀 Excellent implementation that fully meets requirements with great code quality."
        elif score >= 0.85:
            return "LGTM! ✅ Solid implementation that meets requirements with good practices."
        else:
            return "LGTM! ✅ Implementation meets requirements."
    
    def _create_summary(self, status: ReviewStatus, score: float, ac_analysis: List[Dict], code_quality: Dict) -> str:
        """Create a summary of the review."""
        fulfilled_ac = sum(1 for ac in ac_analysis if ac["fulfilled"])
        total_ac = len(ac_analysis)
        
        summary_parts = [
            f"**Review Status:** {status.value.upper()}",
            f"**Overall Score:** {score:.1%}",
            f"**Acceptance Criteria:** {fulfilled_ac}/{total_ac} fulfilled",
            f"**Code Quality Issues:** {code_quality.get('summary', {}).get('total_issues', 0)}",
            f"**Test Coverage:** {'✅' if code_quality.get('summary', {}).get('has_tests', False) else '❌'}"
        ]
        
        return "\n".join(summary_parts)

def create_review_engine(provider: str = "anthropic", model: str = None, base_url: str = None) -> ReviewEngine:
    """Factory function to create ReviewEngine with environment configuration."""
    return ReviewEngine(provider=provider, model=model, base_url=base_url) 