# 🚀 LGTM Bot Integration Guide

Complete guide for integrating LGTM Bot with GitHub and Jira for automated code reviews.

## 📋 Prerequisites

- ✅ LGTM Bot code (already done!)
- ✅ GitHub repository (done - https://github.com/Hrithik-Gavankar/lgtm-bot)
- ✅ Ollama running with models (done - deepseek-r1:latest)
- 🔲 Jira instance access
- 🔲 GitHub Personal Access Token
- 🔲 Jira API Token

## Part 1: 🔑 Credential Setup

### Step 1.1: GitHub Personal Access Token

1. **Go to GitHub Settings**
   ```
   GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   ```

2. **Generate New Token**
   - Click "Generate new token (classic)"
   - Name: `LGTM Bot Access`
   - Expiration: Choose appropriate duration
   - **Required Scopes:**
     ```
     ✅ repo (Full control of private repositories)
     ✅ read:org (Read org and team membership)
     ✅ workflow (Update GitHub Action workflows)
     ```

3. **Save Token Securely**
   ```bash
   # Add to your environment
   export GITHUB_TOKEN="ghp_your_token_here"
   ```

### Step 1.2: Jira API Token

1. **Go to Atlassian Account Settings**
   ```
   https://id.atlassian.com/manage-profile/security/api-tokens
   ```

2. **Create API Token**
   - Click "Create API token"
   - Label: `LGTM Bot Integration`
   - Copy the generated token

3. **Set Environment Variables**
   ```bash
   export JIRA_USERNAME="your-email@company.com"
   export JIRA_TOKEN="your_jira_api_token"
   export JIRA_SERVER="https://your-company.atlassian.net"
   ```

## Part 2: 🎯 Jira Ticket Setup Example

### Step 2.1: Create a Sample Jira Ticket

Here's how to structure a Jira ticket for optimal LGTM Bot analysis:

**Example Ticket: PROJ-456**
```
Title: Implement User Authentication System

Description:
We need to implement a secure user authentication system for our web application.

Problem Description:
Currently, users cannot log in to access protected features. We need a robust authentication mechanism that supports both email/password login and includes proper security measures.

Acceptance Criteria:
- User can register with email and password
- User can login with valid credentials  
- Passwords are securely hashed using bcrypt
- JWT tokens are generated for authenticated sessions
- Invalid login attempts are properly handled
- Session tokens have appropriate expiration
- Login rate limiting is implemented

Technical Requirements:
- Use bcrypt for password hashing
- Implement JWT for session management
- Add input validation for all fields
- Include comprehensive error handling
- Write unit tests for all auth functions

Definition of Done:
- All acceptance criteria met
- Code reviewed and approved
- Unit tests written and passing
- Documentation updated
- Security review completed
```

### Step 2.2: Link PR to Jira Ticket

When creating PRs, use these linking methods:

**Method 1: PR Title/Description**
```markdown
Title: PROJ-456: Add JWT authentication system

Description:
Implements user authentication as specified in PROJ-456.

Resolves: https://your-company.atlassian.net/browse/PROJ-456

Changes:
- Added JWT token generation
- Implemented password hashing with bcrypt
- Created login/register endpoints
- Added input validation
- Included rate limiting middleware
```

**Method 2: Commit Messages**
```bash
git commit -m "feat(auth): implement JWT authentication for PROJ-456

- Add user registration endpoint
- Implement secure password hashing
- Create JWT token generation
- Add login rate limiting

Refs: PROJ-456"
```

**Method 3: Jira Comments**
```
Add PR link in Jira ticket comments:
"PR created: https://github.com/your-org/your-repo/pull/123"
```

## Part 3: 🏃‍♂️ Manual Workflow Example

### Step 3.1: Environment Setup

Create your environment file:
```bash
# Create .env file
cat > .env << EOF
# Jira Configuration
JIRA_USERNAME=your-email@company.com
JIRA_TOKEN=your_jira_api_token
JIRA_SERVER=https://your-company.atlassian.net

# GitHub Configuration
GITHUB_TOKEN=your_github_personal_access_token

# Ollama is configured - no API key needed!
EOF
```

### Step 3.2: Test Jira Connection

Test your Jira setup:
```bash
# Test with ticket analysis
python3 lgtm_bot.py analyze-ticket PROJ-456

# Should output:
# Ticket: PROJ-456
# Summary: Implement User Authentication System
# Status: In Progress
# Acceptance Criteria (7):
#   1. User can register with email and password
#   2. User can login with valid credentials
#   ...
```

### Step 3.3: Run Complete Review

Execute full review process:
```bash
# Option 1: Auto-find linked PRs
python3 lgtm_bot.py PROJ-456 --verbose

# Option 2: Specify PR explicitly  
python3 lgtm_bot.py PROJ-456 \
  --pr-url https://github.com/your-org/repo/pull/123 \
  --output markdown \
  --save-to review-PROJ-456.md

# Option 3: JSON for CI/CD
python3 lgtm_bot.py PROJ-456 \
  --pr-url https://github.com/your-org/repo/pull/123 \
  --output json \
  --save-to review-results.json
```

## Part 4: 🤖 CI/CD Integration

### Step 4.1: GitHub Actions Workflow

Create `.github/workflows/lgtm-review.yml`:

```yaml
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
```

### Step 4.2: Required GitHub Secrets

Add these secrets to your repository:

```
Repository Settings → Secrets and variables → Actions → New repository secret
```

**Required Secrets:**
```
JIRA_USERNAME = your-email@company.com
JIRA_TOKEN = your_jira_api_token  
JIRA_SERVER = https://your-company.atlassian.net
```

(GITHUB_TOKEN is automatically provided)

## Part 5: 🔄 Complete Workflow Example

### Step 5.1: Developer Workflow

1. **Create Jira Ticket** (PROJ-456)
2. **Create Feature Branch**
   ```bash
   git checkout -b feature/PROJ-456-user-auth
   ```

3. **Implement Code Changes**
   ```bash
   # Make your changes
   git add .
   git commit -m "feat(auth): implement user authentication for PROJ-456"
   git push origin feature/PROJ-456-user-auth
   ```

4. **Create Pull Request**
   - Title: `PROJ-456: Implement User Authentication System`
   - Link to Jira ticket in description

5. **LGTM Bot Automatically Reviews**
   - Extracts PROJ-456 from title
   - Fetches Jira ticket details
   - Analyzes PR against acceptance criteria
   - Posts review comment

### Step 5.2: Manual Review Example

Let's simulate a complete review:

```bash
# Simulate the complete workflow
echo "🎬 LGTM Bot Workflow Simulation"
echo "================================"

# 1. Test Ollama
python3 test_ollama.py

# 2. Analyze Jira ticket
echo "\n📋 Step 1: Analyzing Jira Ticket..."
python3 lgtm_bot.py analyze-ticket PROJ-456

# 3. Analyze PR
echo "\n🔍 Step 2: Analyzing GitHub PR..."  
python3 lgtm_bot.py analyze-pr https://github.com/your-org/repo/pull/123

# 4. Complete review
echo "\n🤖 Step 3: Running Complete Review..."
python3 lgtm_bot.py PROJ-456 \
  --pr-url https://github.com/your-org/repo/pull/123 \
  --output console

# 5. Generate reports
echo "\n📊 Step 4: Generating Reports..."
python3 lgtm_bot.py PROJ-456 \
  --pr-url https://github.com/your-org/repo/pull/123 \
  --output markdown \
  --save-to github-comment.md

python3 lgtm_bot.py PROJ-456 \
  --pr-url https://github.com/your-org/repo/pull/123 \
  --output json \
  --save-to ci-results.json

echo "\n✅ Workflow Complete!"
```

## Part 6: 📊 Monitoring & Analytics

### Step 6.1: Review Metrics Dashboard

Track your review metrics:

```bash
# Create metrics collection script
cat > collect_metrics.py << 'EOF'
#!/usr/bin/env python3
import json
import glob
from datetime import datetime
from collections import defaultdict

def analyze_reviews():
    metrics = {
        'total_reviews': 0,
        'pass_rate': 0,
        'avg_score': 0,
        'common_issues': defaultdict(int)
    }
    
    scores = []
    statuses = []
    
    for file in glob.glob('review-*.json'):
        with open(file) as f:
            review = json.load(f)
            
        scores.append(review['review_result']['overall_score'])
        statuses.append(review['review_result']['status'])
        
        for issue in review['analysis']['code_quality_issues']:
            metrics['common_issues'][issue['type']] += 1
    
    metrics['total_reviews'] = len(scores)
    metrics['pass_rate'] = statuses.count('pass') / len(statuses) if statuses else 0
    metrics['avg_score'] = sum(scores) / len(scores) if scores else 0
    
    print(f"📊 LGTM Bot Metrics")
    print(f"Total Reviews: {metrics['total_reviews']}")
    print(f"Pass Rate: {metrics['pass_rate']:.1%}")
    print(f"Average Score: {metrics['avg_score']:.1%}")
    print(f"Common Issues: {dict(metrics['common_issues'])}")

if __name__ == "__main__":
    analyze_reviews()
EOF

chmod +x collect_metrics.py
```

## Part 7: 🛠️ Troubleshooting

### Common Issues & Solutions

**Issue 1: "No linked PRs found"**
```bash
# Solution: Explicitly specify PR URL
python3 lgtm_bot.py PROJ-456 --pr-url https://github.com/org/repo/pull/123
```

**Issue 2: "Jira ticket not found"**
```bash
# Check credentials
echo $JIRA_USERNAME
echo $JIRA_TOKEN

# Test connection manually
curl -u "$JIRA_USERNAME:$JIRA_TOKEN" \
  "$JIRA_SERVER/rest/api/2/issue/PROJ-456"
```

**Issue 3: "GitHub API rate limit"**
```bash
# Check rate limit status
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/rate_limit
```

**Issue 4: "Ollama model not found"**
```bash
# Check available models
ollama list

# Pull required model
ollama pull deepseek-r1:latest
```

## 🎉 Success Checklist

- ✅ Credentials configured (Jira + GitHub)
- ✅ Ollama running with deepseek-r1:latest
- ✅ LGTM Bot can analyze Jira tickets
- ✅ LGTM Bot can analyze GitHub PRs  
- ✅ Complete review workflow working
- ✅ CI/CD integration configured
- ✅ GitHub Actions posting review comments
- ✅ Team trained on workflow

Your LGTM Bot is now fully integrated and ready for production use! 🚀 