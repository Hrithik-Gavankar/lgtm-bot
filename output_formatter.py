"""
Output Formatter Module

Formats review results for different output types (console, markdown, JSON).
"""

import json
from typing import Dict, List, Any
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

from review_engine import ReviewResult, ReviewStatus
from jira_parser import JiraTicketInfo
from pr_analyzer import PRDiff

class OutputFormatter:
    """Handles formatting of review results for different output types."""
    
    def __init__(self):
        """Initialize the formatter."""
        self.console = Console()
    
    def format_console_output(self, ticket_info: JiraTicketInfo, pr_diff: PRDiff, 
                            review_result: ReviewResult) -> None:
        """
        Format and display review results in the console using rich formatting.
        
        Args:
            ticket_info: Jira ticket information
            pr_diff: PR diff information  
            review_result: Review result to format
        """
        # Header
        self._print_header(ticket_info, pr_diff, review_result)
        
        # Summary
        self._print_summary(review_result)
        
        # Acceptance Criteria Analysis
        self._print_acceptance_criteria(review_result.acceptance_criteria_analysis)
        
        # Code Quality Issues
        if review_result.code_quality_issues:
            self._print_code_quality_issues(review_result.code_quality_issues)
        
        # Test Analysis
        self._print_test_analysis(review_result.test_analysis)
        
        # Suggestions and Requirements
        if review_result.suggestions or review_result.required_changes:
            self._print_recommendations(review_result.suggestions, review_result.required_changes)
        
        # Test Recommendations
        if review_result.recommended_tests:
            self._print_test_recommendations(review_result.recommended_tests)
        
        # Final LGTM Comment
        if review_result.lgtm_comment:
            self._print_lgtm_comment(review_result.lgtm_comment)
    
    def format_markdown_output(self, ticket_info: JiraTicketInfo, pr_diff: PRDiff, 
                             review_result: ReviewResult) -> str:
        """
        Format review results as markdown for GitHub comments or documentation.
        
        Args:
            ticket_info: Jira ticket information
            pr_diff: PR diff information
            review_result: Review result to format
            
        Returns:
            Formatted markdown string
        """
        lines = []
        
        # Header
        lines.append(f"# Code Review Results")
        lines.append(f"**Ticket:** [{ticket_info.ticket_key}] {ticket_info.summary}")
        lines.append(f"**PR:** #{pr_diff.pr_number} - {pr_diff.title}")
        lines.append(f"**Reviewed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # Status Badge
        status_emoji = {
            ReviewStatus.PASS: "✅",
            ReviewStatus.CONDITIONAL: "⚠️", 
            ReviewStatus.FAIL: "❌"
        }
        lines.append(f"## {status_emoji[review_result.status]} Review Status: {review_result.status.value.upper()}")
        lines.append(f"**Overall Score:** {review_result.overall_score:.1%}")
        lines.append("")
        
        # Summary
        lines.append("## 📋 Summary")
        lines.append(review_result.summary)
        lines.append("")
        
        # Acceptance Criteria
        if review_result.acceptance_criteria_analysis:
            lines.append("## 🎯 Acceptance Criteria Analysis")
            for i, ac in enumerate(review_result.acceptance_criteria_analysis, 1):
                status_icon = "✅" if ac["fulfilled"] else "❌"
                confidence = f"({ac['confidence']:.1%} confidence)"
                lines.append(f"### {i}. {status_icon} {ac['criterion']} {confidence}")
                
                if ac["evidence"]:
                    lines.append("**Evidence:**")
                    for evidence in ac["evidence"]:
                        lines.append(f"- {evidence}")
                
                if ac["gaps"]:
                    lines.append("**Gaps:**")
                    for gap in ac["gaps"]:
                        lines.append(f"- {gap}")
                
                if ac["reasoning"]:
                    lines.append(f"**Reasoning:** {ac['reasoning']}")
                
                lines.append("")
        
        # Code Quality Issues
        if review_result.code_quality_issues:
            lines.append("## 🔍 Code Quality Issues")
            for issue in review_result.code_quality_issues:
                lines.append(f"- **{issue.get('file', 'Unknown')}**: {issue.get('message', 'No message')}")
            lines.append("")
        
        # Test Analysis
        if review_result.test_analysis:
            lines.append("## 🧪 Test Analysis")
            test_icon = "✅" if review_result.test_analysis.get("has_test_files", False) else "❌"
            lines.append(f"{test_icon} **Test Coverage:** {review_result.test_analysis.get('recommendation', 'No analysis')}")
            
            if review_result.test_analysis.get("test_files"):
                lines.append("**Test Files:**")
                for test_file in review_result.test_analysis["test_files"]:
                    lines.append(f"- {test_file}")
            lines.append("")
        
        # Required Changes
        if review_result.required_changes:
            lines.append("## ❗ Required Changes")
            for change in review_result.required_changes:
                lines.append(f"- {change}")
            lines.append("")
        
        # Suggestions
        if review_result.suggestions:
            lines.append("## 💡 Suggestions for Improvement")
            for suggestion in review_result.suggestions:
                lines.append(f"- {suggestion}")
            lines.append("")
        
        # Recommended Tests
        if review_result.recommended_tests:
            lines.append("## 🧪 Recommended Test Cases")
            for test in review_result.recommended_tests:
                lines.append(f"- {test}")
            lines.append("")
        
        # LGTM Comment
        if review_result.lgtm_comment:
            lines.append("## 🚀 Final Verdict")
            lines.append(review_result.lgtm_comment)
            lines.append("")
        
        return "\n".join(lines)
    
    def format_json_output(self, ticket_info: JiraTicketInfo, pr_diff: PRDiff, 
                          review_result: ReviewResult) -> str:
        """
        Format review results as JSON for API consumption or data storage.
        
        Args:
            ticket_info: Jira ticket information
            pr_diff: PR diff information
            review_result: Review result to format
            
        Returns:
            Formatted JSON string
        """
        output = {
            "review_metadata": {
                "timestamp": datetime.now().isoformat(),
                "ticket_key": ticket_info.ticket_key,
                "ticket_summary": ticket_info.summary,
                "pr_number": pr_diff.pr_number,
                "pr_title": pr_diff.title,
                "pr_author": pr_diff.author
            },
            "review_result": {
                "status": review_result.status.value,
                "overall_score": review_result.overall_score,
                "summary": review_result.summary,
                "lgtm_comment": review_result.lgtm_comment
            },
            "analysis": {
                "acceptance_criteria": review_result.acceptance_criteria_analysis,
                "code_quality_issues": review_result.code_quality_issues,
                "test_analysis": review_result.test_analysis
            },
            "recommendations": {
                "suggestions": review_result.suggestions,
                "required_changes": review_result.required_changes,
                "recommended_tests": review_result.recommended_tests
            }
        }
        
        return json.dumps(output, indent=2, ensure_ascii=False)
    
    def _print_header(self, ticket_info: JiraTicketInfo, pr_diff: PRDiff, review_result: ReviewResult):
        """Print formatted header."""
        status_colors = {
            ReviewStatus.PASS: "green",
            ReviewStatus.CONDITIONAL: "yellow",
            ReviewStatus.FAIL: "red"
        }
        
        status_text = Text(f"Review Status: {review_result.status.value.upper()}", 
                          style=f"bold {status_colors[review_result.status]}")
        
        header_text = f"""
📋 **Ticket:** {ticket_info.ticket_key} - {ticket_info.summary}
🔀 **PR:** #{pr_diff.pr_number} - {pr_diff.title}
👤 **Author:** {pr_diff.author}
📊 **Score:** {review_result.overall_score:.1%}
"""
        
        panel = Panel(
            header_text + "\n" + str(status_text),
            title="🤖 LGTM Bot Review",
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        self.console.print()
    
    def _print_summary(self, review_result: ReviewResult):
        """Print formatted summary."""
        self.console.print(Markdown(f"## 📋 Summary\n{review_result.summary}"))
        self.console.print()
    
    def _print_acceptance_criteria(self, ac_analysis: List[Dict[str, Any]]):
        """Print acceptance criteria analysis table."""
        if not ac_analysis:
            return
        
        table = Table(title="🎯 Acceptance Criteria Analysis")
        table.add_column("Criterion", style="cyan", no_wrap=False, max_width=40)
        table.add_column("Status", justify="center")
        table.add_column("Confidence", justify="center")
        table.add_column("Notes", style="yellow", no_wrap=False, max_width=30)
        
        for ac in ac_analysis:
            status_icon = "✅" if ac["fulfilled"] else "❌"
            confidence = f"{ac['confidence']:.1%}"
            
            # Create notes from evidence and gaps
            notes = []
            if ac.get("evidence"):
                notes.extend([f"✓ {e[:50]}..." for e in ac["evidence"][:2]])
            if ac.get("gaps"):
                notes.extend([f"✗ {g[:50]}..." for g in ac["gaps"][:2]])
            
            notes_text = "\n".join(notes) if notes else "No details"
            
            table.add_row(
                ac["criterion"][:80] + ("..." if len(ac["criterion"]) > 80 else ""),
                status_icon,
                confidence,
                notes_text
            )
        
        self.console.print(table)
        self.console.print()
    
    def _print_code_quality_issues(self, issues: List[Dict[str, Any]]):
        """Print code quality issues."""
        if not issues:
            return
        
        self.console.print("[bold red]🔍 Code Quality Issues[/bold red]")
        
        for issue in issues:
            file_name = issue.get("file", "Unknown")
            message = issue.get("message", "No message")
            issue_type = issue.get("type", "unknown")
            
            self.console.print(f"  • [red]{file_name}[/red]: {message} ([dim]{issue_type}[/dim])")
        
        self.console.print()
    
    def _print_test_analysis(self, test_analysis: Dict[str, Any]):
        """Print test analysis."""
        if not test_analysis:
            return
        
        has_tests = test_analysis.get("has_test_files", False)
        icon = "✅" if has_tests else "❌"
        
        self.console.print(f"[bold]🧪 Test Analysis[/bold]")
        self.console.print(f"  {icon} Status: {test_analysis.get('recommendation', 'No analysis')}")
        
        if test_analysis.get("test_files"):
            self.console.print("  📁 Test Files:")
            for test_file in test_analysis["test_files"]:
                self.console.print(f"    • {test_file}")
        
        self.console.print()
    
    def _print_recommendations(self, suggestions: List[str], required_changes: List[str]):
        """Print suggestions and required changes."""
        if required_changes:
            self.console.print("[bold red]❗ Required Changes[/bold red]")
            for change in required_changes:
                self.console.print(f"  • {change}")
            self.console.print()
        
        if suggestions:
            self.console.print("[bold yellow]💡 Suggestions for Improvement[/bold yellow]")
            for suggestion in suggestions[:10]:  # Limit to avoid clutter
                self.console.print(f"  • {suggestion}")
            self.console.print()
    
    def _print_test_recommendations(self, test_recommendations: List[str]):
        """Print test recommendations."""
        if not test_recommendations:
            return
        
        self.console.print("[bold blue]🧪 Recommended Test Cases[/bold blue]")
        for test in test_recommendations:
            self.console.print(f"  • {test}")
        self.console.print()
    
    def _print_lgtm_comment(self, lgtm_comment: str):
        """Print LGTM comment in a special panel."""
        panel = Panel(
            lgtm_comment,
            title="🚀 Final Verdict",
            border_style="green",
            padding=(1, 2)
        )
        self.console.print(panel) 