#!/usr/bin/env python3
"""
Demo script showing LGTM Bot output with mock data.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from datetime import datetime

def demo_lgtm_output():
    """Show a realistic LGTM Bot output demo."""
    console = Console()
    
    # Header
    console.print()
    header_text = """
📋 **Ticket:** PROJ-123 - Implement user authentication system
🔀 **PR:** #456 - Add JWT authentication with password validation
👤 **Author:** developer-jane
📊 **Score:** 87.5%
🤖 **AI Model:** deepseek-r1:latest (Ollama)
"""
    
    status_text = Text("Review Status: PASS", style="bold green")
    
    panel = Panel(
        header_text + "\n" + str(status_text),
        title="🤖 LGTM Bot Review Results",
        border_style="blue",
        padding=(1, 2)
    )
    
    console.print(panel)
    console.print()
    
    # Summary
    console.print("## 📋 Summary", style="bold")
    console.print("**Review Status:** PASS")
    console.print("**Overall Score:** 87.5%")
    console.print("**Acceptance Criteria:** 3/3 fulfilled")
    console.print("**Code Quality Issues:** 2")
    console.print("**Test Coverage:** ✅")
    console.print()
    
    # Acceptance Criteria Table
    table = Table(title="🎯 Acceptance Criteria Analysis")
    table.add_column("Criterion", style="cyan", no_wrap=False, max_width=40)
    table.add_column("Status", justify="center")
    table.add_column("Confidence", justify="center")
    table.add_column("Notes", style="yellow", no_wrap=False, max_width=30)
    
    criteria = [
        ("User can login with valid credentials", "✅", "95%", "✓ JWT token generation\n✓ Login endpoint implemented"),
        ("Password validation implemented", "✅", "88%", "✓ bcrypt hashing\n✓ Strength validation"),
        ("Session management with tokens", "✅", "92%", "✓ Token refresh logic\n✓ Secure storage"),
    ]
    
    for criterion, status, confidence, notes in criteria:
        table.add_row(criterion, status, confidence, notes)
    
    console.print(table)
    console.print()
    
    # Code Quality Issues
    console.print("[bold yellow]💡 Suggestions for Improvement[/bold yellow]")
    console.print("  • auth.py: Line exceeds 120 characters (135 chars)")
    console.print("  • utils.py: Consider extracting password validation to separate function")
    console.print()
    
    # Test Analysis
    console.print("[bold]🧪 Test Analysis[/bold]")
    console.print("  ✅ Status: Good test coverage detected")
    console.print("  📁 Test Files:")
    console.print("    • test_auth.py")
    console.print("    • test_password_validation.py")
    console.print()
    
    # Recommended Tests
    console.print("[bold blue]🧪 Recommended Test Cases[/bold blue]")
    console.print("  • Test case for: User can login with valid credentials")
    console.print("  • Test case for: Password validation implemented")
    console.print("  • Edge case: Login with expired token")
    console.print()
    
    # Final Verdict
    lgtm_panel = Panel(
        "LGTM! ✅ Solid implementation that meets requirements with good practices.",
        title="🚀 Final Verdict",
        border_style="green",
        padding=(1, 2)
    )
    console.print(lgtm_panel)
    console.print()
    
    # What AI Analysis Found
    console.print("[bold]🧠 AI Analysis Highlights:[/bold]")
    console.print("  • [green]Security:[/green] Proper password hashing with bcrypt")
    console.print("  • [green]Performance:[/green] Efficient token validation")
    console.print("  • [green]Maintainability:[/green] Clean separation of concerns")
    console.print("  • [yellow]Suggestion:[/yellow] Add rate limiting for login attempts")
    console.print()

def demo_markdown_output():
    """Show what markdown output looks like."""
    markdown = """
# Code Review Results - MARKDOWN FORMAT
**Ticket:** [PROJ-123] Implement user authentication system  
**PR:** #456 - Add JWT authentication with password validation
**Reviewed:** 2024-01-15 14:30:25
**AI Model:** deepseek-r1:latest (Ollama)

## ✅ Review Status: PASS
**Overall Score:** 87.5%

## 🎯 Acceptance Criteria Analysis
### 1. ✅ User can login with valid credentials (95% confidence)
**Evidence:**
- JWT token generation implemented in auth.py
- Login endpoint accepts credentials and returns token

### 2. ✅ Password validation implemented (88% confidence)  
**Evidence:**
- Password hashing using bcrypt
- Input validation for password strength

### 3. ✅ Session management with tokens (92% confidence)
**Evidence:**
- Token refresh mechanism implemented
- Secure token storage

## 🔍 Code Quality Issues
- **auth.py**: Line exceeds 120 characters (135 chars)
- **utils.py**: Consider extracting password validation to separate function

## 🧪 Test Analysis
✅ **Test Coverage:** Good test coverage detected
**Test Files:**
- test_auth.py
- test_password_validation.py

## 🚀 Final Verdict
LGTM! ✅ Solid implementation that meets requirements with good practices.
"""
    
    print(markdown)

def demo_json_output():
    """Show what JSON output looks like."""
    import json
    
    json_output = {
        "review_metadata": {
            "timestamp": "2024-01-15T14:30:25",
            "ticket_key": "PROJ-123",
            "ticket_summary": "Implement user authentication system",
            "pr_number": 456,
            "pr_title": "Add JWT authentication with password validation",
            "pr_author": "developer-jane",
            "ai_model": "deepseek-r1:latest",
            "ai_provider": "ollama"
        },
        "review_result": {
            "status": "pass",
            "overall_score": 0.875,
            "summary": "**Review Status:** PASS\n**Overall Score:** 87.5%\n**Acceptance Criteria:** 3/3 fulfilled",
            "lgtm_comment": "LGTM! ✅ Solid implementation that meets requirements with good practices."
        },
        "analysis": {
            "acceptance_criteria": [
                {
                    "criterion": "User can login with valid credentials",
                    "fulfilled": True,
                    "confidence": 0.95,
                    "evidence": ["JWT token generation implemented in auth.py", "Login endpoint accepts credentials"],
                    "gaps": [],
                    "reasoning": "Clear implementation of authentication flow"
                }
            ],
            "code_quality_issues": [
                {"file": "auth.py", "type": "long_line", "message": "Line exceeds 120 characters (135 chars)"},
                {"file": "utils.py", "type": "refactor", "message": "Consider extracting password validation"}
            ],
            "test_analysis": {
                "has_test_files": True,
                "test_file_count": 2,
                "recommendation": "Good test coverage detected"
            }
        }
    }
    
    print(json.dumps(json_output, indent=2))

if __name__ == "__main__":
    import sys
    
    console = Console()
    console.print("🎭 LGTM Bot Output Demo", style="bold blue")
    console.print("=" * 40)
    console.print()
    
    if len(sys.argv) > 1 and sys.argv[1] == "markdown":
        console.print("📝 Markdown Output:", style="bold")
        console.print("-" * 20)
        demo_markdown_output()
    elif len(sys.argv) > 1 and sys.argv[1] == "json":
        console.print("📊 JSON Output:", style="bold")
        console.print("-" * 20)
        demo_json_output()
    else:
        console.print("🎨 Console Output (Default):", style="bold")
        console.print("-" * 30)
        demo_lgtm_output()
        
        console.print("\n💡 Try these other formats:")
        console.print("  • python3 demo_output.py markdown")
        console.print("  • python3 demo_output.py json") 