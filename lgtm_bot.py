#!/usr/bin/env python3
"""
LGTM Bot - AI-Powered Code Review Bot

Main entry point for the LGTM bot that reviews PRs against Jira ticket requirements.
"""

import os
import sys
import click
import yaml
import logging
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

from jira_parser import create_jira_parser, JiraTicketInfo
from pr_analyzer import create_pr_analyzer, PRDiff
from review_engine import create_review_engine, ReviewResult, ReviewStatus
from output_formatter import OutputFormatter

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LGTMBot:
    """Main LGTM Bot class that orchestrates the review process."""
    
    def __init__(self, config_file: str = "config.yaml"):
        """
        Initialize the LGTM bot with configuration.
        
        Args:
            config_file: Path to configuration file
        """
        self.config = self._load_config(config_file)
        self.formatter = OutputFormatter()
        self._validate_environment()
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {config_file}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file {config_file} not found, using defaults")
            return self._get_default_config()
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "jira": {
                "server": "https://your-company.atlassian.net"
            },
            "ai": {
                "provider": "anthropic",
                "model": "claude-3-sonnet-20240229",
                "base_url": None
            },
            "review": {
                "criteria": [
                    "Fulfills acceptance criteria",
                    "Proper error handling",
                    "Adequate test coverage",
                    "Clean code practices"
                ],
                "fail_keywords": ["TODO", "FIXME", "HACK", "console.log", "print("],
                "test_patterns": [
                    "test_*.py", "*_test.py", "*.test.js", "*.spec.js",
                    "*.test.ts", "*.spec.ts"
                ]
            }
        }
    
    def _validate_environment(self):
        """Validate that required environment variables are set."""
        required_vars = []
        
        # Check Jira credentials
        if not os.getenv("JIRA_USERNAME") or not os.getenv("JIRA_TOKEN"):
            required_vars.extend(["JIRA_USERNAME", "JIRA_TOKEN"])
        
        # Check GitHub credentials
        if not os.getenv("GITHUB_TOKEN"):
            required_vars.append("GITHUB_TOKEN")
        
        # Check AI credentials
        ai_provider = self.config.get("ai", {}).get("provider", "anthropic")
        if ai_provider == "anthropic" and not os.getenv("ANTHROPIC_API_KEY"):
            required_vars.append("ANTHROPIC_API_KEY")
        elif ai_provider == "openai" and not os.getenv("OPENAI_API_KEY"):
            required_vars.append("OPENAI_API_KEY")
        # Ollama doesn't require API keys, just needs to be running locally
        
        if required_vars:
            logger.error(f"Missing required environment variables: {', '.join(required_vars)}")
            logger.info("Please set these variables in your environment or .env file")
            sys.exit(1)
    
    def review_pr(self, jira_ticket: str, pr_urls: List[str] = None, 
                  output_format: str = "console", save_to: Optional[str] = None) -> ReviewResult:
        """
        Perform complete PR review against Jira ticket.
        
        Args:
            jira_ticket: Jira ticket URL or key
            pr_urls: List of PR URLs (if not provided, will look for linked PRs)
            output_format: Output format ("console", "markdown", "json")
            save_to: File path to save output (optional)
            
        Returns:
            Review result
        """
        logger.info(f"Starting review for ticket: {jira_ticket}")
        
        try:
            # Step 1: Extract Jira ticket information
            logger.info("Step 1: Extracting Jira ticket information...")
            jira_parser = create_jira_parser()
            ticket_info = jira_parser.extract_ticket_info(jira_ticket)
            
            logger.info(f"Found ticket: {ticket_info.ticket_key} - {ticket_info.summary}")
            logger.info(f"Acceptance criteria: {len(ticket_info.acceptance_criteria)} items")
            
            # Determine PR URLs to review
            if not pr_urls:
                if ticket_info.linked_prs:
                    pr_urls = ticket_info.linked_prs
                    logger.info(f"Found {len(pr_urls)} linked PRs")
                else:
                    logger.error("No PR URLs provided and no linked PRs found in ticket")
                    logger.info("Please provide PR URLs using --pr-url option")
                    sys.exit(1)
            
            # For now, review the first PR (could be extended to handle multiple)
            pr_url = pr_urls[0]
            logger.info(f"Reviewing PR: {pr_url}")
            
            # Step 2: Analyze PR diff
            logger.info("Step 2: Analyzing PR diff...")
            pr_analyzer = create_pr_analyzer(self.config["review"]["test_patterns"])
            pr_diff = pr_analyzer.get_pr_diff(pr_url)
            
            logger.info(f"PR #{pr_diff.pr_number}: {pr_diff.title}")
            logger.info(f"Files changed: {pr_diff.total_files_changed}")
            logger.info(f"Lines: +{pr_diff.total_additions}, -{pr_diff.total_deletions}")
            
            # Step 3: Perform code quality analysis
            logger.info("Step 3: Performing code quality analysis...")
            code_quality_analysis = pr_analyzer.analyze_code_quality(
                pr_diff, self.config["review"]["fail_keywords"]
            )
            
            # Step 4: Run AI-powered review
            logger.info("Step 4: Running AI-powered review...")
            ai_config = self.config["ai"]
            review_engine = create_review_engine(
                provider=ai_config["provider"],
                model=ai_config.get("model"),
                base_url=ai_config.get("base_url")
            )
            
            review_result = review_engine.review_pr(
                ticket_info, pr_diff, code_quality_analysis
            )
            
            logger.info(f"Review completed - Status: {review_result.status.value}")
            logger.info(f"Overall score: {review_result.overall_score:.1%}")
            
            # Step 5: Format and display results
            self._output_results(ticket_info, pr_diff, review_result, output_format, save_to)
            
            return review_result
            
        except Exception as e:
            logger.error(f"Review failed: {e}")
            raise
    
    def _output_results(self, ticket_info: JiraTicketInfo, pr_diff: PRDiff, 
                       review_result: ReviewResult, output_format: str, save_to: Optional[str]):
        """Output review results in the specified format."""
        if output_format == "console":
            self.formatter.format_console_output(ticket_info, pr_diff, review_result)
        
        elif output_format == "markdown":
            markdown_output = self.formatter.format_markdown_output(ticket_info, pr_diff, review_result)
            if save_to:
                with open(save_to, 'w') as f:
                    f.write(markdown_output)
                logger.info(f"Markdown output saved to {save_to}")
            else:
                print(markdown_output)
        
        elif output_format == "json":
            json_output = self.formatter.format_json_output(ticket_info, pr_diff, review_result)
            if save_to:
                with open(save_to, 'w') as f:
                    f.write(json_output)
                logger.info(f"JSON output saved to {save_to}")
            else:
                print(json_output)
        
        else:
            logger.error(f"Unknown output format: {output_format}")

# CLI Interface
@click.command()
@click.argument('jira_ticket', required=True)
@click.option('--pr-url', multiple=True, help='PR URL to review (can be used multiple times)')
@click.option('--output', '-o', default='console', 
              type=click.Choice(['console', 'markdown', 'json']),
              help='Output format')
@click.option('--save-to', '-s', help='Save output to file')
@click.option('--config', '-c', default='config.yaml', help='Configuration file path')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def main(jira_ticket: str, pr_url: tuple, output: str, save_to: Optional[str], 
         config: str, verbose: bool):
    """
    LGTM Bot - AI-Powered Code Review Bot
    
    Reviews GitHub PRs against Jira ticket requirements.
    
    JIRA_TICKET: Jira ticket URL or key (e.g., PROJ-123 or https://company.atlassian.net/browse/PROJ-123)
    
    Examples:
    
    \b
    # Review with linked PRs from ticket
    lgtm-bot PROJ-123
    
    \b
    # Review specific PR 
    lgtm-bot PROJ-123 --pr-url https://github.com/org/repo/pull/456
    
    \b
    # Generate markdown report
    lgtm-bot PROJ-123 --output markdown --save-to review.md
    
    \b
    # JSON output for CI/CD integration
    lgtm-bot PROJ-123 --output json --save-to review.json
    """
    
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        bot = LGTMBot(config)
        pr_urls = list(pr_url) if pr_url else None
        
        review_result = bot.review_pr(
            jira_ticket=jira_ticket,
            pr_urls=pr_urls,
            output_format=output,
            save_to=save_to
        )
        
        # Exit with appropriate code based on review result
        if review_result.status == ReviewStatus.PASS:
            sys.exit(0)
        elif review_result.status == ReviewStatus.CONDITIONAL:
            sys.exit(1)  # Warning - manual review needed
        else:
            sys.exit(2)  # Failure
            
    except KeyboardInterrupt:
        logger.info("Review cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

# Additional CLI commands
@click.group()
def cli():
    """LGTM Bot CLI - AI-Powered Code Review"""
    pass

@cli.command()
@click.argument('ticket')
def analyze_ticket(ticket: str):
    """Analyze a Jira ticket and extract information."""
    try:
        jira_parser = create_jira_parser()
        ticket_info = jira_parser.extract_ticket_info(ticket)
        
        print(f"Ticket: {ticket_info.ticket_key}")
        print(f"Summary: {ticket_info.summary}")
        print(f"Status: {ticket_info.status}")
        print(f"Priority: {ticket_info.priority}")
        print(f"Type: {ticket_info.issue_type}")
        print(f"\nProblem Description:")
        print(ticket_info.problem_description)
        print(f"\nAcceptance Criteria ({len(ticket_info.acceptance_criteria)}):")
        for i, criterion in enumerate(ticket_info.acceptance_criteria, 1):
            print(f"  {i}. {criterion}")
        print(f"\nLinked PRs ({len(ticket_info.linked_prs)}):")
        for pr in ticket_info.linked_prs:
            print(f"  - {pr}")
            
    except Exception as e:
        logger.error(f"Failed to analyze ticket: {e}")
        sys.exit(1)

@cli.command()
@click.argument('pr_url')
def analyze_pr(pr_url: str):
    """Analyze a GitHub PR and show diff information."""
    try:
        pr_analyzer = create_pr_analyzer()
        pr_diff = pr_analyzer.get_pr_diff(pr_url)
        
        print(f"PR #{pr_diff.pr_number}: {pr_diff.title}")
        print(f"Author: {pr_diff.author}")
        print(f"State: {pr_diff.state}")
        print(f"Base: {pr_diff.base_branch} -> Head: {pr_diff.head_branch}")
        print(f"Files changed: {pr_diff.total_files_changed}")
        print(f"Changes: +{pr_diff.total_additions}, -{pr_diff.total_deletions}")
        print(f"\nDescription:")
        print(pr_diff.description[:200] + "..." if len(pr_diff.description) > 200 else pr_diff.description)
        
        print(f"\nFiles:")
        for file_change in pr_diff.file_changes:
            test_indicator = " (test)" if file_change.is_test_file else ""
            print(f"  {file_change.status}: {file_change.filename}{test_indicator}")
            
    except Exception as e:
        logger.error(f"Failed to analyze PR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if running as main command or subcommand
    if len(sys.argv) > 1 and sys.argv[1] in ['analyze-ticket', 'analyze-pr']:
        cli()
    else:
        main() 