# Gemini AI Integration Guide

Complete guide to setting up, configuring, and using Google's Gemini AI API in the PMO Automation System.

---

## 🤖 What is Gemini AI?

Gemini is Google's generative AI model that can:
- **Analyze** project risks and financial data
- **Recommend** mitigation strategies
- **Generate** actionable insights from raw numbers
- **Explain** complex project situations in natural language

**In this system:** Gemini analyzes project summaries and provides strategic PMO recommendations.

---

## 📋 Prerequisites

- Google account (Gmail or Google Workspace)
- Internet connection
- No credit card required (free tier available)

---

## 🔑 Step 1: Obtain Gemini API Key

### Option A: Google AI Studio (Free, No Card Required)

This is the **recommended** approach for development:

```
1. Go to: https://aistudio.google.com/app/apikeys
2. Sign in with your Google account
3. Click "Create API Key"
4. Choose "Create API key in new project" or existing project
5. Copy the API key (starts with "AI...")
6. Store in .env: GOOGLE_API_KEY=AIzaSy...
```

**Limits (Free Tier):**
- 60 requests per minute
- No credit card required
- Suitable for daily/weekly batch processing

### Option B: Google Cloud Console (Flexible, May Require Card)

For production scaling:

```
1. Go to: https://console.cloud.google.com
2. Create new project or select existing
3. Enable "Generative Language API"
4. Create service account
5. Create JSON key
6. Use key in .env
```

**Advantages:**
- Higher rate limits (scalable)
- Pay-as-you-go pricing ($0.00375 per 1K input tokens)
- Better for production systems

---

## 🔐 Step 2: Add API Key to .env

### Option A: First Time Setup

```bash
# Copy template
cp .env.example .env

# Edit .env (use your editor)
code .env
```

Add your API key:
```
GOOGLE_API_KEY=AIzaSy_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Option B: Update Existing .env

Open `.env` and change:
```
GOOGLE_API_KEY=AIzaSy_old_key_here
# TO:
GOOGLE_API_KEY=AIzaSy_new_key_here
```

### Option C: Verify It's Set

```bash
# Test API key is loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GOOGLE_API_KEY'))"

# Should print your API key (if configured)
AIzaSy_XXXXXXXXXX...
```

---

## ✅ Step 3: Test API Connection

### Run Test Script

```bash
python Scripts/Setup/test_ai.py
```

**Expected Output:**
```
Gemini AI Status Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ API key found in .env
✓ Gemini client initialized
✓ Attempting connection to API...
✓ Connected successfully!

Available Models:
  - gemini-pro
  - gemini-pro-vision
  - gemini-flash-latest

✓ System ready for AI integration
```

**Troubleshooting:**

If you see errors:
```
❌ GOOGLE_API_KEY not found in .env file
→ Check .env exists and has GOOGLE_API_KEY= entry

❌ API_KEY_NOT_VALID
→ Your API key format is wrong
→ Go back to aistudio.google.com and create a new one

❌ quota exceeded
→ You've made 60+ requests in 1 minute
→ Wait a minute, then retry
→ Consider Google Cloud Console for higher limits

❌ InternalServerError (503)
→ Temporary Google API outage
→ Code automatically retries after 2-4 seconds
→ No action needed
```

---

## 🎯 Understanding Prompt Engineering

### Core Concept

The quality of AI insights depends on **prompt quality** (how you ask the question).

**Poor Prompt:**
```
"Analyze the portfolio"
```
→ Vague, generic response

**Good Prompt:**
```
"Analyze the portfolio and recommend budget optimization strategies.
Current situation:
- IT Department: €66,500 spent of €65,000 budget (2% over)
- 5 projects overdue
- 2 projects at risk (red status)

Please provide 3 actionable recommendations."
```
→ Specific, context-rich, actionable response

### Prompt Engineering in Code

Look at `Scripts/Analysis/PMO AI Architecture (V1.5).py`:

```python
def criar_prompt_estrategico(nome_projeto, risco, variancia):
    """Build a strategic prompt for project analysis."""
    prompt = f"""
    Act as a senior PMO consultant. 
    
    Analyze this project:
    - Name: {nome_projeto}
    - Current Risk: {risco}
    - Budget Variance: {variancia}€
    
    Generate a 3-step mitigation plan.
    Focus on practical, immediate actions.
    """
    return prompt
```

**Key Elements:**
1. **Role assignment** - "Act as a senior PMO consultant"
2. **Context** - Structured data (project name, risk, variance)
3. **Specific request** - "3-step mitigation plan"
4. **Guardrails** - "Practical, immediate actions"

---

## 📝 Configurable Prompts

### Location: Scripts/Utils/api_key.py

The main prompt used for analysis:

```python
def get_ai_insight(summary_text: str) -> str:
    prompt = f"""
    Act as operations Director. Analyse this project summary and 
    provide a strategic recommendation in two sentences focused on 
    budget risk and resource allocation:
    {summary_text}
    """
    response = client.models.generate_content(model=model, contents=prompt)
    return response.text
```

### Customization Examples

**For Risk Analysis:**
```python
prompt = f"""
As a risk management expert, identify the top 3 risks in:
{project_data}

For each risk, suggest mitigation strategies.
"""
```

**For Budget Optimization:**
```python
prompt = f"""
As a finance director, analyze budget utilization:
{budget_data}

Recommend reallocation across departments to maximize efficiency.
"""
```

**For Executive Summary:**
```python
prompt = f"""
Create an executive summary (150 words) suitable for C-level management:
{full_analysis}

Focus on: strategic implications, financial impact, recommended actions.
"""
```

---

## 🔄 API Integration Workflow

### How Data Flows to Gemini

```
Raw Project Data (CSV)
    ↓
Clean & validate (Scripts/Utils/data_utils.py)
    ↓
Aggregate by department (Scripts/Analysis/Data_Auditor.py)
    ↓
Extract summary (Context Injection)
    ↓
Build prompt (criar_prompt_estrategico)
    ↓
Send to Gemini API (google.genai.models.generate_content)
    ↓
Wait for response (with timeout)
    ↓
Parse AI recommendation
    ↓
Inject into Excel report
    ↓
Email to stakeholders
```

### Code Example: get_ai_insight()

Located in `Scripts/Utils/api_key.py`:

```python
def get_ai_insight(summary_text: str, retries: int = 3) -> str:
    """
    Get AI recommendation with automatic retry on server errors.
    
    Args:
        summary_text: Structured project summary
        retries: Number of retry attempts (exponential backoff)
    
    Returns:
        str: AI recommendation or fallback message
    """
    for i in range(retries):
        try:
            # Send to Gemini API
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
            return response.text  # Success!
            
        except exceptions.InternalServerError:
            # Temporary error (503) - wait and retry
            wait = (i + 1) * 2  # 2s, 4s, 6s
            log.warning(f"API busy, retrying in {wait}s...")
            time.sleep(wait)
            
        except Exception as e:
            # Other errors - don't retry
            log.error(f"AI error: {e}")
            return "AI unavailable"  # Graceful fallback
    
    return "AI unavailable"  # All retries failed
```

**Key Features:**
- ✅ Exponential backoff (2s → 4s → 6s)
- ✅ Graceful fallback (report continues without AI)
- ✅ Structured error logging
- ✅ Non-blocking (email sent even if AI fails)

---

## 🔍 Rate Limits & Quotas

### Free Tier (aistudio.google.com)

| Metric | Limit |
|--------|-------|
| Requests per minute | 60 |
| Tokens per minute | 4,000,000 |
| Daily quota | None (but quota exceeded if >60 RPM) |

### How to Monitor

```python
# In your code, track API calls
api_call_count = 0

for project in projects:
    api_call_count += 1
    if api_call_count > 60:
        log.warning("Approaching rate limit!")
        time.sleep(60)  # Wait 1 minute
        api_call_count = 0
    
    insight = get_ai_insight(project)
```

### If You Hit the Limit

**Error Message:**
```
429 Resource Exhausted: Quota exceeded for rate limit
```

**Solution:**
```
1. Wait 60 seconds
2. Run again
3. For frequent calls, upgrade to Google Cloud Console:
   - Higher limits: 1,500+ requests per minute
   - Pay-as-you-go: ~$0.0001 per API call
```

---

## 🎛️ Advanced Configuration

### Change Model Used

The system uses `gemini-flash-latest` (fast, cost-effective).

To use a different model, edit `Scripts/Utils/api_key.py`:

```python
# Current (fast)
model = "gemini-flash-latest"

# Alternative (more detailed)
model = "gemini-pro"

# Alternative (vision - can analyze charts)
model = "gemini-pro-vision"
```

**Model Comparison:**

| Model | Speed | Power | Cost | Use Case |
|-------|-------|-------|------|----------|
| **flash** | ⚡ Fast | Medium | Cheap | Fast analysis, daily reports |
| **pro** | Slow | High | Medium | Complex analysis |
| **vision** | Very slow | High | High | Analyze images/charts |

### Adjust Retry Logic

Edit `Scripts/Utils/api_key.py` function parameters:

```python
# Default: 3 retries (6 seconds total)
insight = get_ai_insight(summary, retries=3)

# More patient: 5 retries (20 seconds total)
insight = get_ai_insight(summary, retries=5)

# Impatient: 1 retry (2 seconds total)
insight = get_ai_insight(summary, retries=1)
```

---

## 📊 Example Use Cases

### Use Case 1: Risk Analysis

```python
# Project summary
summary = f"""
Project: Cloud Migration
Status: At Risk
Budget: €45,000 allocated, €48,000 spent (€3,000 over)
Schedule: 5 days overdue
Risks: Database latency, resource shortage

Department Summary:
- IT: €48,500 spent
- Infrastructure: €2,400 spent
"""

# Get AI insight
insight = get_ai_insight(summary)
print(insight)

# Output might be:
# "Immediate action required: Database optimization could recover 
# 2 weeks schedule and reduce costs by €5,000. Recommend increasing 
# infrastructure support."
```

### Use Case 2: Executive Summary

```python
# Aggregate data
summary = f"""
Weekly Portfolio Status:
- 4 projects on track
- 2 projects delayed
- 1 project at high risk (over budget)
- Total budget variance: -€8,500 (over)

Department Allocation:
{dept_summary_table}

Key Risks:
- Resource shortage in IT
- Unexpected hardware costs
"""

# Generate executive summary
insight = get_ai_insight(summary)
# Use in report: report['Executive_Insight'] = insight
```

---

## 🐛 Debugging API Issues

### Verbose Logging

Edit `Scripts/Utils/api_key.py` to add logging:

```python
import logging
log = logging.getLogger("Gemini_API")
log.setLevel(logging.DEBUG)  # Show all messages

def get_ai_insight(summary: str) -> str:
    log.debug(f"Sending prompt ({len(summary)} chars)...")
    log.debug(f"Model: {model}")
    log.debug(f"API Key: {api_key[:20]}...")  # First 20 chars only
    
    try:
        response = client.models.generate_content(...)
        log.info(f"Response received ({len(response.text)} chars)")
        return response.text
    except Exception as e:
        log.error(f"API error: {e}", exc_info=True)
        return "Error"
```

### Test Minimal Prompt

```bash
python -c "
from Scripts.Utils.api_key import get_ai_insight
result = get_ai_insight('Hello, are you working?')
print(result)
"

# If this returns a response, API is working
# If not, check .env and API key
```

---

## 🔐 Security Best Practices

### 1. Never Log Your API Key

❌ **WRONG:**
```python
print(f"Using API key: {api_key}")  # Exposes credentials!
log.info(f"API key: {api_key}")     # Logged to file!
```

✅ **CORRECT:**
```python
log.info(f"API key: {api_key[:20]}...")  # Only first 20 chars
log.info("Using Gemini API")              # Generic message
```

### 2. Store in Environment Only

❌ **WRONG:**
```python
API_KEY = "AIzaSy_xxxxx"  # Hardcoded in code!
```

✅ **CORRECT:**
```python
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
```

### 3. Rotate Keys Quarterly

```bash
# 1. Go to aistudio.google.com
# 2. Delete old API key
# 3. Create new one
# 4. Update .env
# 5. Test: python Scripts/Setup/test_ai.py
# 6. Commit code (but NOT .env!)
```

### 4. Monitor Usage

```bash
# Check how many API calls you've made this month
# https://console.cloud.google.com/usage

# Set quota alerts:
# 1. IAM & Admin → Quotas
# 2. Select "Generative Language API"
# 3. Set alert at 80% of limit
```

---

## 📈 Upgrading to Production

When moving from free tier to production:

### Step 1: Set Up Google Cloud Billing

```
1. Go to https://console.cloud.google.com
2. Billing → Create billing account
3. Link credit card (required for production)
4. Set budget alerts: $10/month recommended
```

### Step 2: Create Service Account

```
1. IAM & Admin → Service Accounts
2. Create Service Account
3. Create JSON key
4. Download and secure the key file
```

### Step 3: Update .env

```bash
# Old (free tier)
GOOGLE_API_KEY=AIzaSy_xxx

# New (production with service account)
# Or:
GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
```

### Step 4: Update Code

```python
# Old (API key)
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# New (service account)
import google.auth
credentials, _ = google.auth.default()
client = genai.Client(credentials=credentials)
```

### Step 5: Monitor Costs

```
Expected costs (monthly):
- 60 requests/day × 30 days = 1,800 requests
- Average 500 tokens per request = 900,000 tokens
- Cost: 900,000 ÷ 1M × $0.075 = ~$0.07/month

Budget recommended: $10/month (gives 140x headroom)
```

---

## 📚 Resources

- **Gemini API Docs:** https://ai.google.dev/docs
- **Model Cards:** https://ai.google.dev/models
- **Pricing:** https://ai.google.dev/pricing
- **Status Page:** https://status.cloud.google.com/

---

## 🆘 Troubleshooting Summary

| Error | Cause | Fix |
|-------|-------|-----|
| `GOOGLE_API_KEY not found` | .env missing or empty | `cp .env.example .env` and fill key |
| `Invalid API Key` | Wrong format or expired | Get new key from aistudio.google.com |
| `quota exceeded (429)` | Too many requests | Wait 60 seconds, consider upgrade |
| `InternalServerError (503)` | Google API temporary outage | Automatic retry after 2-4 seconds |
| `Timeout` | Network or slow API | Check internet, try again |
| `403 Permission Denied` | API not enabled | Enable "Generative Language API" |

---

**Good luck with Gemini AI integration!** 🤖
