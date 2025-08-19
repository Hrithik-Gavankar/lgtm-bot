<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/3004d035-f353-492f-97e3-e933013d34f8" />

# LGTM Bot 🤖

An AI-powered code review bot that evaluates GitHub Pull Requests against Jira ticket requirements.

## Features

✅ **Jira Integration**: Extracts problem description, acceptance criteria, and linked PRs from Jira tickets  
🔍 **PR Analysis**: Analyzes GitHub PR diffs, code quality, and test coverage  
🧠 **AI-Powered Review**: Uses Claude/GPT to evaluate code against acceptance criteria  
📊 **Comprehensive Scoring**: Provides objective pass/fail status with detailed feedback  
🎨 **Multiple Output Formats**: Console (with colors), Markdown, and JSON outputs  
🔧 **Configurable**: Customizable review criteria and quality checks  

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd lgtm_bot

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy the example configuration and set up your environment:

```bash
# Copy configuration template
cp config.yaml.example config.yaml

# Set up environment variables
cp .env.example .env
```

Edit `.env` with your credentials:

```bash
# Jira Configuration
JIRA_USERNAME=your-email@company.com
JIRA_TOKEN=your-jira-api-token

# GitHub Configuration  
GITHUB_TOKEN=your-github-personal-access-token

# AI Provider (choose one)
ANTHROPIC_API_KEY=your-anthropic-api-key
# OR
OPENAI_API_KEY=your-openai-api-key
# OR use Ollama (local LLM) - no API key needed!
```

### 3. Using with Ollama (Local LLMs)

For privacy and offline use, you can use Ollama instead of cloud AI providers:

```bash
# Install and start Ollama (if not already done)
# Visit: https://ollama.ai for installation instructions

# Pull a model (choose one)
ollama pull llama3.2:latest     # General purpose, good balance
ollama pull llama3.2:3b         # Smaller, faster model  
ollama pull deepseek-r1:latest  # Good for code review

# Copy the Ollama configuration
cp config-ollama.yaml config.yaml

# Test Ollama connectivity (optional but recommended)
python test_ollama.py

# Edit config.yaml to specify your model
# Then run normally - no API keys needed!
```

### 4. Basic Usage

```bash
# Review a PR using linked PRs from Jira ticket
python lgtm_bot.py PROJ-123

# Review a specific PR
python lgtm_bot.py PROJ-123 --pr-url https://github.com/org/repo/pull/456

# Generate markdown report
python lgtm_bot.py PROJ-123 --output markdown --save-to review.md

# JSON output for CI/CD integration
python lgtm_bot.py PROJ-123 --output json --save-to review.json

# Use specific Ollama model
python lgtm_bot.py PROJ-123 --config config-ollama.yaml
```

## How It Works

The LGTM Bot follows a comprehensive 3-step review process:

### Step 1: Jira Ticket Analysis
- Extracts **problem description** from ticket description
- Identifies **acceptance criteria** using intelligent parsing
- Finds **linked PRs** from comments, description, and issue links

### Step 2: PR Code Analysis  
- Fetches PR diff and metadata from GitHub API
- Analyzes **code quality** (fail keywords, code smells, line length)
- Evaluates **test coverage** (identifies test files, calculates ratios)
- Performs **structural analysis** (file changes, additions/deletions)

### Step 3: AI-Powered Review
- Uses Claude/GPT to evaluate code against each acceptance criterion
- Performs intelligent **security and performance review**
- Generates **actionable feedback** and improvement suggestions
- Calculates **objective score** (0-100%) based on multiple factors

## Scoring Algorithm

The bot calculates an overall score using weighted factors:

- **Acceptance Criteria** (40%): How well the PR fulfills ticket requirements
- **Code Quality** (30%): Issues, code smells, and fail keywords  
- **Test Coverage** (20%): Presence and adequacy of tests
- **AI Assessment** (10%): Security, performance, and maintainability

**Review Status:**
- ✅ **PASS** (≥80%): Ready to merge
- ⚠️ **CONDITIONAL** (60-79%): Needs minor improvements  
- ❌ **FAIL** (<60%): Requires significant changes

## Command Line Interface

### Main Review Command

```bash
python lgtm_bot.py JIRA_TICKET [OPTIONS]

Options:
  --pr-url TEXT          PR URL to review (can be used multiple times)
  --output [console|markdown|json]  Output format (default: console)
  --save-to PATH         Save output to file
  --config PATH          Configuration file path (default: config.yaml)
  --verbose              Enable verbose logging
```

### Utility Commands

```bash
# Analyze Jira ticket only
python lgtm_bot.py analyze-ticket PROJ-123

# Analyze GitHub PR only  
python lgtm_bot.py analyze-pr https://github.com/org/repo/pull/456
```

## Configuration

The `config.yaml` file allows customization of review behavior:

```yaml
jira:
  server: "https://your-company.atlassian.net"

ai:
  provider: "anthropic"  # "anthropic", "openai", or "ollama"
  model: "claude-3-sonnet-20240229"  # or "gpt-4" or "llama3.2:latest"
  base_url: ""  # For ollama: "http://localhost:11434/v1"

review:
  criteria:
    - "Fulfills acceptance criteria"
    - "Proper error handling"
    - "Adequate test coverage"
    - "Clean code practices"
    - "Security considerations"
    
  fail_keywords:
    - "TODO"
    - "FIXME"
    - "HACK"
    - "console.log"
    - "print("
    
  test_patterns:
    - "test_*.py"
    - "*_test.py"
    - "*.test.js"
    - "*.spec.js"
```

## Output Examples

### Console Output
Rich, colorized terminal output with tables and panels:

```
🤖 LGTM Bot Review
┌─────────────────────────────────────────────────────────┐
│ 📋 Ticket: PROJ-123 - Implement user authentication     │
│ 🔀 PR: #456 - Add JWT authentication system            │
│ 👤 Author: developer                                    │
│ 📊 Score: 87.5%                                         │
│ Review Status: PASS                                      │
└─────────────────────────────────────────────────────────┘

🎯 Acceptance Criteria Analysis
┌──────────────────────────────────┬─────────┬────────────┐
│ Criterion                        │ Status  │ Confidence │
├──────────────────────────────────┼─────────┼────────────┤
│ User can login with JWT tokens   │   ✅    │    95%     │
│ Password validation implemented  │   ✅    │    88%     │
└──────────────────────────────────┴─────────┴────────────┘
```

### Markdown Output
Perfect for GitHub PR comments:

```markdown
# Code Review Results
**Ticket:** [PROJ-123] Implement user authentication  
**PR:** #456 - Add JWT authentication system
**Reviewed:** 2024-01-15 14:30:25

## ✅ Review Status: PASS
**Overall Score:** 87.5%

## 🎯 Acceptance Criteria Analysis
### 1. ✅ User can login with JWT tokens (95% confidence)
**Evidence:**
- JWT token generation implemented in auth.py
- Login endpoint accepts credentials and returns token

### 2. ✅ Password validation implemented (88% confidence)  
**Evidence:**
- Password hashing using bcrypt
- Input validation for password strength
```

### JSON Output
Structured data for CI/CD integration:

```json
{
  "review_metadata": {
    "timestamp": "2024-01-15T14:30:25",
    "ticket_key": "PROJ-123",
    "pr_number": 456,
    "pr_author": "developer"
  },
  "review_result": {
    "status": "pass",
    "overall_score": 0.875,
    "lgtm_comment": "LGTM! ✅ Solid implementation that meets requirements."
  },
  "analysis": {
    "acceptance_criteria": [...],
    "code_quality_issues": [...],
    "test_analysis": {...}
  }
}
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: LGTM Bot Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          
      - name: Install LGTM Bot
        run: |
          pip install -r requirements.txt
          
      - name: Run Review
        env:
          JIRA_USERNAME: ${{ secrets.JIRA_USERNAME }}
          JIRA_TOKEN: ${{ secrets.JIRA_TOKEN }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python lgtm_bot.py ${{ github.event.pull_request.title }} \
            --pr-url ${{ github.event.pull_request.html_url }} \
            --output json --save-to review.json
            
      - name: Comment PR
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const review = JSON.parse(fs.readFileSync('review.json', 'utf8'));
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## LGTM Bot Review\n\n**Status:** ${review.review_result.status.toUpperCase()}\n**Score:** ${Math.round(review.review_result.overall_score * 100)}%\n\n${review.review_result.lgtm_comment || 'See full report for details.'}`
            });
```

## API Credentials Setup

### Jira API Token
1. Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Create an API token
3. Use your email as username and token as password

### GitHub Personal Access Token  
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate token with `repo` scope
3. For private repositories, ensure token has appropriate permissions

### AI Provider API Keys

**Anthropic (Claude):**
1. Sign up at [Anthropic Console](https://console.anthropic.com/)
2. Generate API key from dashboard

**OpenAI (GPT):**
1. Sign up at [OpenAI Platform](https://platform.openai.com/)
2. Generate API key from API keys section

**Ollama (Local LLMs):**
1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull desired models: `ollama pull llama3.2:latest`
3. Ensure Ollama is running: `ollama serve` (usually auto-starts)
4. No API key required - runs completely offline!

## Troubleshooting

### Common Issues

**"Missing environment variables"**
```bash
# Ensure all required variables are set
export JIRA_USERNAME="your-email@company.com"
export JIRA_TOKEN="your-api-token" 
export GITHUB_TOKEN="your-github-token"
export ANTHROPIC_API_KEY="your-anthropic-key"
```

**"No linked PRs found"**
```bash
# Explicitly specify PR URL
python lgtm_bot.py PROJ-123 --pr-url https://github.com/org/repo/pull/456
```

**"Jira ticket not found"**
```bash
# Use full ticket URL or check permissions
python lgtm_bot.py https://company.atlassian.net/browse/PROJ-123
```

**"AI API rate limits"**
- Reduce frequency of reviews
- Consider using OpenAI instead of Anthropic (or vice versa)
- Check API usage quotas
- **Recommended**: Use Ollama for unlimited local reviews!

**"Ollama connection failed"**
```bash
# Check if Ollama is running
ollama list

# Start Ollama service if needed
ollama serve

# Test connection
curl http://localhost:11434/api/version
```

### Debug Mode

```bash
# Enable verbose logging for debugging
python lgtm_bot.py PROJ-123 --verbose
```

## Architecture

The bot is modular and extensible:

```
lgtm_bot/
├── lgtm_bot.py          # Main CLI application
├── jira_parser.py       # Jira API integration
├── pr_analyzer.py       # GitHub PR analysis  
├── review_engine.py     # AI-powered review logic
├── output_formatter.py  # Output formatting
├── config.yaml          # Configuration
└── requirements.txt     # Dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details. 
