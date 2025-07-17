#!/bin/bash
echo "🔧 LGTM Bot Setup Guide"
echo "======================"
echo
echo "📋 Required Environment Variables:"
echo
echo "# Jira Setup:"
echo "export JIRA_USERNAME='your-email@company.com'"
echo "export JIRA_TOKEN='your-jira-api-token'"
echo
echo "# GitHub Setup:"  
echo "export GITHUB_TOKEN='your-github-personal-access-token'"
echo
echo "# Ollama is already configured - no API keys needed! 🎉"
echo
echo "📖 How to get these credentials:"
echo
echo "1. 🏢 Jira API Token:"
echo "   - Go to: https://id.atlassian.com/manage-profile/security/api-tokens"
echo "   - Create API token"
echo "   - Use your email as username, token as password"
echo
echo "2. 🐙 GitHub Personal Access Token:"
echo "   - Go to: GitHub Settings → Developer settings → Personal access tokens"
echo "   - Generate token with 'repo' scope"
echo "   - For private repos, ensure proper permissions"
echo
echo "3. 🚀 Once set up, run:"
echo "   python3 lgtm_bot.py PROJ-123 --pr-url https://github.com/org/repo/pull/456"
echo
