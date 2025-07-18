"""
Jira Ticket Parser Module

Extracts problem description, acceptance criteria, and linked PRs from Jira tickets.
"""

import re
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from jira import JIRA
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class JiraTicketInfo:
    """Structured representation of extracted Jira ticket information."""
    ticket_key: str
    problem_description: str
    acceptance_criteria: List[str]
    linked_prs: List[str]
    summary: str
    status: str
    priority: str
    issue_type: str

class JiraParser:
    """Handles Jira API integration and ticket parsing."""
    
    def __init__(self, server: str, username: str, token: str):
        """Initialize Jira client with credentials."""
        self.server = server
        self.username = username
        self.token = token
        self.jira = None
        self._connect()
    
    def _connect(self):
        """Establish connection to Jira."""
        try:
            self.jira = JIRA(
                server=self.server,
                basic_auth=(self.username, self.token)
            )
            logger.info(f"Connected to Jira server: {self.server}")
        except Exception as e:
            logger.error(f"Failed to connect to Jira: {e}")
            raise
    
    def extract_ticket_info(self, ticket_url_or_key: str) -> JiraTicketInfo:
        """
        Extract structured information from a Jira ticket.
        
        Args:
            ticket_url_or_key: Jira ticket URL or key (e.g., 'PROJ-123')
            
        Returns:
            JiraTicketInfo object with extracted data
        """
        # Extract ticket key from URL if provided
        ticket_key = self._extract_ticket_key(ticket_url_or_key)
        
        try:
            issue = self.jira.issue(ticket_key)
            
            # Extract basic info
            summary = issue.fields.summary
            description = issue.fields.description or ""
            status = issue.fields.status.name
            priority = issue.fields.priority.name if issue.fields.priority else "Unknown"
            issue_type = issue.fields.issuetype.name
            
            # Extract problem description and acceptance criteria
            problem_description, acceptance_criteria = self._parse_description(description)
            
            # Find linked PRs
            linked_prs = self._find_linked_prs(issue)
            
            return JiraTicketInfo(
                ticket_key=ticket_key,
                problem_description=problem_description,
                acceptance_criteria=acceptance_criteria,
                linked_prs=linked_prs,
                summary=summary,
                status=status,
                priority=priority,
                issue_type=issue_type
            )
            
        except Exception as e:
            logger.error(f"Failed to extract ticket info for {ticket_key}: {e}")
            raise
    
    def _extract_ticket_key(self, ticket_url_or_key: str) -> str:
        """Extract ticket key from URL or return as-is if already a key."""
        # Pattern to match Jira ticket keys (PROJECT-123 format)
        key_pattern = r'([A-Z]+-\d+)'
        match = re.search(key_pattern, ticket_url_or_key)
        
        if match:
            return match.group(1)
        else:
            raise ValueError(f"Could not extract ticket key from: {ticket_url_or_key}")
    
    def _parse_description(self, description: str) -> Tuple[str, List[str]]:
        """
        Parse ticket description to extract problem description and acceptance criteria.
        
        Args:
            description: Raw ticket description text
            
        Returns:
            Tuple of (problem_description, acceptance_criteria_list)
        """
        if not description:
            return "No description provided", []
        
        # Common patterns for acceptance criteria sections
        ac_patterns = [
            r'(?i)acceptance\s+criteria:?\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'(?i)definition\s+of\s+done:?\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'(?i)success\s+criteria:?\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'(?i)requirements:?\s*(.*?)(?=\n\n|\n[A-Z]|$)',
        ]
        
        acceptance_criteria = []
        problem_description = description
        
        # Try to find acceptance criteria
        for pattern in ac_patterns:
            match = re.search(pattern, description, re.DOTALL)
            if match:
                ac_text = match.group(1).strip()
                # Split by bullet points or numbered lists
                criteria_items = re.split(r'\n[\s]*[\*\-\+\d+\.]\s*', ac_text)
                acceptance_criteria = [item.strip() for item in criteria_items if item.strip()]
                
                # Remove AC section from problem description
                problem_description = description[:match.start()].strip()
                break
        
        # Look for bullet points or numbered lists anywhere in description if no explicit AC section
        if not acceptance_criteria:
            bullet_patterns = [
                r'\n[\s]*[\*\-\+]\s+(.+?)(?=\n|$)',
                r'\n[\s]*\d+[\.)\s]+(.+?)(?=\n|$)',
            ]
            
            for pattern in bullet_patterns:
                matches = re.findall(pattern, description)
                if len(matches) >= 2:  # At least 2 items suggest it's a list
                    acceptance_criteria = [match.strip() for match in matches]
                    break
        
        return problem_description, acceptance_criteria
    
    def _find_linked_prs(self, issue) -> List[str]:
        """
        Find linked pull requests in the issue.
        
        Args:
            issue: Jira issue object
            
        Returns:
            List of PR URLs
        """
        linked_prs = []
        
        # Check issue links for PR references
        if hasattr(issue.fields, 'issuelinks'):
            for link in issue.fields.issuelinks:
                # Check both inward and outward links
                linked_issue = getattr(link, 'inwardIssue', None) or getattr(link, 'outwardIssue', None)
                if linked_issue:
                    summary = linked_issue.fields.summary
                    # Look for PR patterns in linked issue summaries
                    pr_urls = self._extract_pr_urls_from_text(summary)
                    linked_prs.extend(pr_urls)
        
        # Check comments for PR references
        try:
            comments = self.jira.comments(issue)
            for comment in comments:
                pr_urls = self._extract_pr_urls_from_text(comment.body)
                linked_prs.extend(pr_urls)
        except Exception as e:
            logger.warning(f"Could not fetch comments: {e}")
        
        # Check description for PR references
        description = issue.fields.description or ""
        pr_urls = self._extract_pr_urls_from_text(description)
        linked_prs.extend(pr_urls)
        
        return list(set(linked_prs))  # Remove duplicates
    
    def _extract_pr_urls_from_text(self, text: str) -> List[str]:
        """Extract GitHub PR URLs from text."""
        if not text:
            return []
        
        # Pattern to match GitHub PR URLs
        pr_pattern = r'https://github\.com/[\w\-\.]+/[\w\-\.]+/pull/\d+'
        matches = re.findall(pr_pattern, text)
        
        return matches

def create_jira_parser() -> JiraParser:
    """Factory function to create JiraParser with environment variables."""
    server = os.getenv('JIRA_SERVER', 'https://your-company.atlassian.net')
    username = os.getenv('JIRA_USERNAME')
    token = os.getenv('JIRA_TOKEN')
    
    if not username or not token:
        raise ValueError("JIRA_USERNAME and JIRA_TOKEN environment variables must be set")
    
    return JiraParser(server, username, token) 