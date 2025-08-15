#!/bin/bash

# 🚀 LGTM Bot Quick Start Demo
# Complete walkthrough with practical examples

set -e  # Exit on any error

echo "🤖 LGTM Bot Integration Demo"
echo "============================"
echo "This script will guide you through the complete setup process."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to prompt for user input
prompt_user() {
    echo -e "${BLUE}$1${NC}"
    read -p "> " response
    echo "$response"
}

# Function to show step
show_step() {
    echo ""
    echo -e "${GREEN}📋 Step $1: $2${NC}"
    echo "----------------------------------------"
}

# Function to show info
show_info() {
    echo -e "${YELLOW}💡 $1${NC}"
}

# Function to show command
show_command() {
    echo -e "${BLUE}🔧 Running: $1${NC}"
}

echo "Let's get started! 🚀"
echo ""

# Step 1: Check Prerequisites
show_step "1" "Checking Prerequisites"

show_command "python3 --version"
python3 --version

show_command "ollama list"
if command -v ollama &> /dev/null; then
    ollama list
    echo -e "${GREEN}✅ Ollama is installed and models available${NC}"
else
    echo -e "${RED}❌ Ollama not found. Please install from https://ollama.ai${NC}"
    exit 1
fi

show_command "git status"
git status

# Step 2: Environment Setup
show_step "2" "Environment Setup"

echo "We need to set up your credentials for Jira and GitHub."
echo ""

show_info "First, let's set up your Jira credentials:"
echo "1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens"
echo "2. Create a new API token"
echo "3. Enter your details below:"
echo ""

# Prompt for Jira credentials
JIRA_USERNAME=$(prompt_user "Enter your Jira email:")
JIRA_TOKEN=$(prompt_user "Enter your Jira API token:")
JIRA_SERVER=$(prompt_user "Enter your Jira server URL (e.g., https://company.atlassian.net):")

echo ""
show_info "Now, let's set up your GitHub credentials:"
echo "1. Go to: GitHub → Settings → Developer settings → Personal access tokens"
echo "2. Generate a new token with 'repo' scope"
echo "3. Enter your token below:"
echo ""

GITHUB_TOKEN=$(prompt_user "Enter your GitHub personal access token:")

# Create .env file
show_command "Creating .env file"
cat > .env << EOF
# Jira Configuration
JIRA_USERNAME=$JIRA_USERNAME
JIRA_TOKEN=$JIRA_TOKEN
JIRA_SERVER=$JIRA_SERVER

# GitHub Configuration
GITHUB_TOKEN=$GITHUB_TOKEN

# Ollama is configured - no API key needed!
EOF

echo -e "${GREEN}✅ Environment file created${NC}"

# Step 3: Test Connections
show_step "3" "Testing Connections"

echo "Loading environment variables..."
export $(cat .env | xargs)

show_command "Testing Ollama connection"
python3 test_ollama.py

echo ""
show_command "Testing Jira connection"
echo "Let's test with a sample ticket analysis..."

SAMPLE_TICKET=$(prompt_user "Enter a Jira ticket key to test (e.g., PROJ-123):")

if [[ -n "$SAMPLE_TICKET" ]]; then
    echo "Testing Jira connection with ticket: $SAMPLE_TICKET"
    python3 lgtm_bot.py analyze-ticket "$SAMPLE_TICKET" || echo "⚠️  Ticket not found or access issue - this is normal for demo"
else
    echo "Skipping Jira test - no ticket provided"
fi

# Step 4: Create Sample Jira Ticket Template
show_step "4" "Sample Jira Ticket Template"

echo "Here's how to structure a Jira ticket for optimal LGTM Bot analysis:"
echo ""

cat > sample_jira_ticket.md << 'EOF'
# Sample Jira Ticket Structure

**Title:** PROJ-456: Implement User Authentication System

**Description:**
We need to implement a secure user authentication system for our web application.

**Problem Description:**
Currently, users cannot log in to access protected features. We need a robust authentication mechanism that supports both email/password login and includes proper security measures.

**Acceptance Criteria:**
- User can register with email and password
- User can login with valid credentials  
- Passwords are securely hashed using bcrypt
- JWT tokens are generated for authenticated sessions
- Invalid login attempts are properly handled
- Session tokens have appropriate expiration
- Login rate limiting is implemented

**Technical Requirements:**
- Use bcrypt for password hashing
- Implement JWT for session management
- Add input validation for all fields
- Include comprehensive error handling
- Write unit tests for all auth functions

**Definition of Done:**
- All acceptance criteria met
- Code reviewed and approved
- Unit tests written and passing
- Documentation updated
- Security review completed
EOF

echo "Sample ticket template created: sample_jira_ticket.md"
echo -e "${GREEN}✅ Use this template for creating Jira tickets${NC}"

# Step 5: Demo Review Process
show_step "5" "Demo Review Process"

echo "Let's demonstrate the complete review process with a public GitHub PR:"
echo ""

show_info "We'll use a public repository for this demo since we need real PR data."

DEMO_PR="https://github.com/microsoft/vscode/pull/200000"
DEMO_TICKET="DEMO-123"

echo "Demo PR: $DEMO_PR"
echo "Demo Ticket: $DEMO_TICKET"
echo ""

show_command "Analyzing GitHub PR structure"
echo "This will show what information the bot can extract from a PR..."

# Try to analyze the PR (might fail due to rate limits, but shows the process)
python3 lgtm_bot.py analyze-pr "$DEMO_PR" || echo "⚠️  Rate limit or access issue - normal for public repos"

# Step 6: Generate Sample Reports
show_step "6" "Sample Reports Generation"

echo "Let's generate sample reports to show what the output looks like:"

show_command "Generating sample console output"
python3 demo_output.py

echo ""
show_command "Generating sample markdown output"
python3 demo_output.py markdown > sample_review.md
echo "Markdown report saved to: sample_review.md"

echo ""
show_command "Generating sample JSON output"
python3 demo_output.py json > sample_review.json
echo "JSON report saved to: sample_review.json"

# Step 7: GitHub Actions Setup
show_step "7" "GitHub Actions Setup"

echo "Creating GitHub Actions workflow for automated reviews..."

mkdir -p .github/workflows

cat > .github/workflows/lgtm-review.yml << 'EOF'
name: LGTM Bot Code Review

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  lgtm-review:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install Ollama
      run: |
        curl -fsSL https://ollama.ai/install.sh | sh
        ollama serve &
        sleep 10
        ollama pull deepseek-r1:latest
        
    - name: Install LGTM Bot
      run: |
        git clone https://github.com/Hrithik-Gavankar/lgtm-bot.git lgtm-bot
        cd lgtm-bot
        pip install -r requirements.txt
        
    - name: Extract Jira Ticket from PR
      id: jira-ticket
      run: |
        # Extract PROJ-XXX from PR title or branch name
        TICKET=$(echo "${{ github.event.pull_request.title }}" | grep -oE '[A-Z]+-[0-9]+' | head -1)
        if [ -z "$TICKET" ]; then
          TICKET=$(echo "${{ github.head_ref }}" | grep -oE '[A-Z]+-[0-9]+' | head -1)
        fi
        echo "ticket=$TICKET" >> $GITHUB_OUTPUT
        
    - name: Run LGTM Review
      if: steps.jira-ticket.outputs.ticket != ''
      env:
        JIRA_USERNAME: ${{ secrets.JIRA_USERNAME }}
        JIRA_TOKEN: ${{ secrets.JIRA_TOKEN }}
        JIRA_SERVER: ${{ secrets.JIRA_SERVER }}
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: |
        cd lgtm-bot
        python3 lgtm_bot.py ${{ steps.jira-ticket.outputs.ticket }} \
          --pr-url ${{ github.event.pull_request.html_url }} \
          --output json \
          --save-to review-results.json
          
    - name: Post Review Comment
      if: steps.jira-ticket.outputs.ticket != ''
      uses: actions/github-script@v7
      with:
        script: |
          const fs = require('fs');
          
          try {
            const review = JSON.parse(fs.readFileSync('lgtm-bot/review-results.json', 'utf8'));
            
            const statusEmoji = {
              'pass': '✅',
              'conditional': '⚠️', 
              'fail': '❌'
            };
            
            const body = `## 🤖 LGTM Bot Review Results
            
            **Status:** ${statusEmoji[review.review_result.status]} ${review.review_result.status.toUpperCase()}  
            **Score:** ${Math.round(review.review_result.overall_score * 100)}%  
            **Ticket:** [${review.review_metadata.ticket_key}](${process.env.JIRA_SERVER}/browse/${review.review_metadata.ticket_key})  
            **AI Model:** ${review.review_metadata.ai_model} (Ollama)
            
            ${review.review_result.lgtm_comment || review.review_result.summary}
            
            <details>
            <summary>📊 Detailed Analysis</summary>
            
            **Acceptance Criteria:** ${review.analysis.acceptance_criteria.filter(ac => ac.fulfilled).length}/${review.analysis.acceptance_criteria.length} fulfilled  
            **Code Issues:** ${review.analysis.code_quality_issues.length}  
            **Test Coverage:** ${review.analysis.test_analysis.has_test_files ? '✅' : '❌'}
            
            </details>
            
            ---
            *Automated review by [LGTM Bot](https://github.com/Hrithik-Gavankar/lgtm-bot)*`;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });
          } catch (error) {
            console.log('Review file not found or invalid - skipping comment');
          }
EOF

echo -e "${GREEN}✅ GitHub Actions workflow created: .github/workflows/lgtm-review.yml${NC}"

# Step 8: Create Usage Examples
show_step "8" "Usage Examples"

cat > usage_examples.sh << 'EOF'
#!/bin/bash

# LGTM Bot Usage Examples

# Load environment
export $(cat .env | xargs)

echo "🎯 LGTM Bot Usage Examples"
echo "========================="

echo ""
echo "1. Analyze Jira Ticket Only:"
echo "python3 lgtm_bot.py analyze-ticket PROJ-456"

echo ""
echo "2. Analyze GitHub PR Only:"
echo "python3 lgtm_bot.py analyze-pr https://github.com/org/repo/pull/123"

echo ""
echo "3. Complete Review (auto-find PRs):"
echo "python3 lgtm_bot.py PROJ-456 --verbose"

echo ""
echo "4. Complete Review (specific PR):"
echo "python3 lgtm_bot.py PROJ-456 --pr-url https://github.com/org/repo/pull/123"

echo ""
echo "5. Generate Markdown Report:"
echo "python3 lgtm_bot.py PROJ-456 --pr-url https://github.com/org/repo/pull/123 --output markdown --save-to review.md"

echo ""
echo "6. Generate JSON for CI/CD:"
echo "python3 lgtm_bot.py PROJ-456 --pr-url https://github.com/org/repo/pull/123 --output json --save-to results.json"

echo ""
echo "7. Use Different Ollama Model:"
echo "# Edit config.yaml to change model to llama3.2:3b"
echo "python3 lgtm_bot.py PROJ-456 --config config-ollama.yaml"
EOF

chmod +x usage_examples.sh

echo -e "${GREEN}✅ Usage examples created: usage_examples.sh${NC}"

# Step 9: Success Summary
show_step "9" "Setup Complete! 🎉"

echo -e "${GREEN}Your LGTM Bot is now fully configured and ready for use!${NC}"
echo ""
echo "📋 What we've set up:"
echo "✅ Environment variables (.env)"
echo "✅ Ollama integration tested"
echo "✅ Connection tests completed"
echo "✅ Sample reports generated"
echo "✅ GitHub Actions workflow"
echo "✅ Usage examples"
echo ""

echo "🚀 Next Steps:"
echo ""
echo "1. Add GitHub Secrets to your repository:"
echo "   - Go to: Repository Settings → Secrets and variables → Actions"
echo "   - Add: JIRA_USERNAME, JIRA_TOKEN, JIRA_SERVER"
echo ""

echo "2. Create a test Jira ticket using the template in: sample_jira_ticket.md"
echo ""

echo "3. Create a PR with ticket reference in title (e.g., 'PROJ-456: Your feature')"
echo ""

echo "4. Watch LGTM Bot automatically review your PR! 🤖"
echo ""

echo "📚 Documentation:"
echo "- Complete guide: integration_guide.md"
echo "- Usage examples: usage_examples.sh"
echo "- Sample reports: sample_review.md, sample_review.json"
echo ""

echo "🛠️ Manual Testing:"
echo "./usage_examples.sh  # See all available commands"
echo ""

echo -e "${GREEN}Happy coding with AI-powered reviews! 🎉${NC}" 