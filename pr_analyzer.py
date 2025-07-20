"""
GitHub Pull Request Analyzer Module

Fetches and analyzes GitHub PR diffs for code review.
"""

import os
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from github import Github
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FileChange:
    """Represents a single file change in a PR."""
    filename: str
    status: str  # 'added', 'modified', 'removed'
    additions: int
    deletions: int
    changes: int
    patch: Optional[str]
    is_test_file: bool = False

@dataclass
class PRDiff:
    """Represents the complete diff of a pull request."""
    pr_number: int
    title: str
    description: str
    author: str
    state: str
    file_changes: List[FileChange]
    total_additions: int
    total_deletions: int
    total_files_changed: int
    base_branch: str
    head_branch: str
    created_at: str
    updated_at: str

class PRAnalyzer:
    """Handles GitHub PR fetching and analysis."""
    
    def __init__(self, token: str, test_patterns: List[str] = None):
        """
        Initialize GitHub client with token.
        
        Args:
            token: GitHub personal access token
            test_patterns: File patterns that indicate test files
        """
        self.github = Github(token)
        self.test_patterns = test_patterns or [
            "test_*.py", "*_test.py", "*.test.js", "*.spec.js",
            "*.test.ts", "*.spec.ts", "test/*.py", "tests/*.py",
            "__tests__/*", "spec/*"
        ]
    
    def get_pr_diff(self, pr_url: str) -> PRDiff:
        """
        Fetch and analyze a GitHub PR.
        
        Args:
            pr_url: GitHub PR URL (e.g., https://github.com/owner/repo/pull/123)
            
        Returns:
            PRDiff object with complete PR information
        """
        repo_name, pr_number = self._parse_pr_url(pr_url)
        
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            
            # Get file changes
            file_changes = []
            total_additions = 0
            total_deletions = 0
            
            for file in pr.get_files():
                is_test = self._is_test_file(file.filename)
                
                file_change = FileChange(
                    filename=file.filename,
                    status=file.status,
                    additions=file.additions,
                    deletions=file.deletions,
                    changes=file.changes,
                    patch=file.patch,
                    is_test_file=is_test
                )
                
                file_changes.append(file_change)
                total_additions += file.additions
                total_deletions += file.deletions
            
            return PRDiff(
                pr_number=pr_number,
                title=pr.title,
                description=pr.body or "",
                author=pr.user.login,
                state=pr.state,
                file_changes=file_changes,
                total_additions=total_additions,
                total_deletions=total_deletions,
                total_files_changed=len(file_changes),
                base_branch=pr.base.ref,
                head_branch=pr.head.ref,
                created_at=pr.created_at.isoformat(),
                updated_at=pr.updated_at.isoformat()
            )
            
        except Exception as e:
            logger.error(f"Failed to fetch PR {pr_url}: {e}")
            raise
    
    def _parse_pr_url(self, pr_url: str) -> Tuple[str, int]:
        """
        Parse GitHub PR URL to extract repo name and PR number.
        
        Args:
            pr_url: GitHub PR URL
            
        Returns:
            Tuple of (repo_name, pr_number)
        """
        # Pattern to match GitHub PR URLs
        pattern = r'https://github\.com/([^/]+/[^/]+)/pull/(\d+)'
        match = re.search(pattern, pr_url)
        
        if not match:
            raise ValueError(f"Invalid GitHub PR URL: {pr_url}")
        
        repo_name = match.group(1)
        pr_number = int(match.group(2))
        
        return repo_name, pr_number
    
    def _is_test_file(self, filename: str) -> bool:
        """
        Check if a file is a test file based on patterns.
        
        Args:
            filename: File path/name
            
        Returns:
            True if file appears to be a test file
        """
        filename_lower = filename.lower()
        
        for pattern in self.test_patterns:
            # Convert glob pattern to regex
            regex_pattern = pattern.replace('*', '.*').replace('?', '.')
            if re.search(regex_pattern, filename_lower):
                return True
        
        # Additional heuristics
        path_parts = filename_lower.split('/')
        test_indicators = ['test', 'tests', 'spec', 'specs', '__tests__']
        
        return any(indicator in path_parts for indicator in test_indicators)
    
    def analyze_code_quality(self, pr_diff: PRDiff, fail_keywords: List[str] = None) -> Dict[str, any]:
        """
        Analyze code quality issues in the PR.
        
        Args:
            pr_diff: PRDiff object to analyze
            fail_keywords: Keywords that indicate potential issues
            
        Returns:
            Dictionary with analysis results
        """
        fail_keywords = fail_keywords or ["TODO", "FIXME", "HACK", "console.log", "print("]
        
        issues = []
        test_coverage = self._analyze_test_coverage(pr_diff)
        code_smells = []
        
        for file_change in pr_diff.file_changes:
            if file_change.patch:
                # Check for fail keywords
                for keyword in fail_keywords:
                    if keyword.lower() in file_change.patch.lower():
                        issues.append({
                            "file": file_change.filename,
                            "type": "fail_keyword",
                            "keyword": keyword,
                            "message": f"Found '{keyword}' in {file_change.filename}"
                        })
                
                # Check for code smells
                smells = self._detect_code_smells(file_change)
                code_smells.extend(smells)
        
        return {
            "issues": issues,
            "test_coverage": test_coverage,
            "code_smells": code_smells,
            "summary": {
                "total_issues": len(issues),
                "has_tests": test_coverage["has_test_files"],
                "test_file_count": test_coverage["test_file_count"],
                "code_smell_count": len(code_smells)
            }
        }
    
    def _analyze_test_coverage(self, pr_diff: PRDiff) -> Dict[str, any]:
        """Analyze test coverage in the PR."""
        test_files = [f for f in pr_diff.file_changes if f.is_test_file]
        non_test_files = [f for f in pr_diff.file_changes if not f.is_test_file]
        
        # Calculate ratios
        test_to_code_ratio = len(test_files) / max(len(non_test_files), 1)
        
        return {
            "has_test_files": len(test_files) > 0,
            "test_file_count": len(test_files),
            "code_file_count": len(non_test_files),
            "test_to_code_ratio": test_to_code_ratio,
            "test_files": [f.filename for f in test_files],
            "recommendation": self._get_test_recommendation(test_to_code_ratio, len(test_files))
        }
    
    def _get_test_recommendation(self, ratio: float, test_count: int) -> str:
        """Get test coverage recommendation."""
        if test_count == 0:
            return "No tests found. Consider adding tests for the new functionality."
        elif ratio < 0.3:
            return "Low test coverage. Consider adding more comprehensive tests."
        elif ratio < 0.7:
            return "Moderate test coverage. Good, but could be improved."
        else:
            return "Good test coverage detected."
    
    def _detect_code_smells(self, file_change: FileChange) -> List[Dict[str, str]]:
        """Detect potential code smells in a file change."""
        smells = []
        
        if not file_change.patch:
            return smells
        
        patch_lines = file_change.patch.split('\n')
        
        # Check for added lines (start with +)
        added_lines = [line[1:] for line in patch_lines if line.startswith('+') and len(line) > 1]
        
        for i, line in enumerate(added_lines):
            line_stripped = line.strip()
            
            # Long lines
            if len(line) > 120:
                smells.append({
                    "file": file_change.filename,
                    "type": "long_line",
                    "line": i + 1,
                    "message": f"Line exceeds 120 characters ({len(line)} chars)"
                })
            
            # Deep nesting (simplified heuristic)
            indent_level = len(line) - len(line.lstrip())
            if indent_level > 24:  # More than 6 levels of 4-space indentation
                smells.append({
                    "file": file_change.filename,
                    "type": "deep_nesting",
                    "line": i + 1,
                    "message": "Deeply nested code detected"
                })
            
            # Commented out code (simplified detection)
            if line_stripped.startswith('//') or line_stripped.startswith('#'):
                if any(keyword in line_stripped.lower() for keyword in ['function', 'def ', 'class ', 'import']):
                    smells.append({
                        "file": file_change.filename,
                        "type": "commented_code",
                        "line": i + 1,
                        "message": "Potential commented out code"
                    })
            
            # Hardcoded strings/numbers (simplified detection)
            if re.search(r'["\'][^"\']{20,}["\']', line_stripped):
                smells.append({
                    "file": file_change.filename,
                    "type": "hardcoded_string",
                    "line": i + 1,
                    "message": "Long hardcoded string detected"
                })
        
        return smells

def create_pr_analyzer(test_patterns: List[str] = None) -> PRAnalyzer:
    """Factory function to create PRAnalyzer with environment variables."""
    token = os.getenv('GITHUB_TOKEN')
    
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable must be set")
    
    return PRAnalyzer(token, test_patterns) 