# Setup & Installation Guide

Complete step-by-step guide to install and configure the PMO Automation System.

---

## 📋 Prerequisites

Before starting, ensure you have:

- **Python 3.12+** - Download from [python.org](https://www.python.org/downloads/)
- **pip** - Comes with Python installation
- **Git** - For version control (optional but recommended)
- **Internet connection** - For downloading dependencies and API keys

### Check Your Setup

```bash
# Check Python version (should be 3.12 or higher)
python --version

# Check pip is installed
pip --version

# Check Git (optional)
git --version
```

---

## 🚀 Installation Steps

### Step 1: Clone or Navigate to Project

```bash
# If cloning from Git
git clone https://github.com/DanielaMarques-aut/pmo-automation-toolkit.git 
cd pmo-automation-toolkit



```

### Step 2: Create Virtual Environment

A virtual environment isolates project dependencies from your system Python.

```bash
# Windows
python -m venv .venv

# macOS / Linux
python3 -m venv .venv
```

**Result:** Creates `.venv/` folder (auto-added to `.gitignore`)

### Step 3: Activate Virtual Environment

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (Command Prompt)
.venv\Scripts\activate.bat

# macOS / Linux
source .venv/bin/activate
```

**Indicator:** Your terminal prompt changes to show `(.venv)` prefix

### Step 4: Install Dependencies

```bash
# Upgrade pip to latest version
pip install --upgrade pip

# Install all project dependencies from Requirements.txt
pip install -r Requirements.txt
```

**Expected Output:**
```
Successfully installed pandas-2.x.x
Successfully installed openpyxl-3.x.x
Successfully installed google-generativeai-0.x.x
...
Successfully installed 10+ packages
```

### Step 5: Configure Environment Variables

```bash
# Copy template to .env
cp .env.example .env

# Windows PowerShell (if above doesn't work)
Copy-Item .env.example .env
```

Now edit `.env` with your credentials:

```bash
# Open .env in your editor
notepad .env          # Windows
nano .env             # macOS/Linux
code .env             # VS Code
```

Fill in these values (see [API_INTEGRATION.md](API_INTEGRATION.md) for details):

```env
GOOGLE_API_KEY=your_api_key_from_aistudio
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_16_char_app_password
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your/hook/url
```

### Step 6: Verify Setup (Pre-flight Check)

```bash
# Create necessary folders
python Scripts/Setup/folder_setup.py

# Expected output:
# ✓ Data folder checked/created
# ✓ Logs folder checked/created
# ✓ 04_Archive folder checked/created
# ✓ Environment verified
```

### Step 7: Test AI Connection

```bash
# Test Gemini API
python Scripts/Setup/test_ai.py

# Expected output:
# ✓ API key found
# ✓ Attempting connection...
# ✓ Models available: gemini-pro, gemini-pro-vision
# ✓ System ready for AI integration
```

### Step 8: Test Email Configuration

```bash
# Test email sending
python Scripts/Setup/enviar_por_email.py

# Expected output:
# ✓ Email credentials found
# ✓ SMTP connection successful
# ✓ Test email sent to [your_email]
# Check your inbox to confirm receipt
```

---

## ✅ Verification Checklist

After setup, verify everything works:

```bash
# Run main automation
python Scripts/Analysis/PMO_Consolidated_Engine.py

# Check for successful output
ls Data/Output/relatorio_final.xlsx      # File created?
ls Logs/pmo_audit.log                   # Logs generated?

# Verify no errors
echo "Setup complete if you see no error messages above"
```

---

## 🔧 Dependency Details

### Core Dependencies (Required)

| Package | Purpose | Install | Version |
|---------|---------|---------|---------|
| **pandas** | Data manipulation, CSV/Excel I/O | Auto | >=2.0.0 |
| **openpyxl** | Excel file styling (PatternFill, Font) | Auto | >=3.1.0 |
| **google-generativeai** | Gemini AI API client | Auto | >=0.3.0 |
| **python-dotenv** | Load .env environment variables | Auto | >=1.0.0 |
| **matplotlib** | Dashboard visualization and charts | Auto | >=3.7.0 |
| **requests** | HTTP library for API calls | Auto | >=2.31.0 |
| **slack-sdk** | Slack integration (webhooks) | Auto | >=3.23.0 |

All installed via `pip install -r Requirements.txt`

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Python** | 3.12 | 3.12+ |
| **RAM** | 4 GB | 8 GB |
| **Disk** | 1 GB | 2 GB |
| **CPU** | Dual-core | Quad-core |

---

## ❌ Troubleshooting Common Issues

### Issue 1: ModuleNotFoundError after pip install

**Symptom:**
```
ModuleNotFoundError: No module named 'pandas'
```

**Solution:**
```bash
# 1. Verify you're in the virtual environment
# (Command prompt should show (.venv) prefix)

# 2. If not activated, activate it
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # macOS/Linux

# 3. Reinstall dependencies
pip install -r Requirements.txt
```

### Issue 2: GOOGLE_API_KEY not found error

**Symptom:**
```
❌ Error: GOOGLE_API_KEY not found in .env file
```

**Solution:**
```bash
# 1. Check .env exists in project root
ls .env                  # macOS/Linux
dir .env                 # Windows

# 2. If missing, create it
cp .env.example .env     # macOS/Linux
Copy-Item .env.example .env  # Windows PowerShell

# 3. Edit .env and add API key
# See SETUP.md step 5 and API_INTEGRATION.md

# 4. Test it works
python Scripts/Setup/test_ai.py
```

### Issue 3: Email sending fails (SMTPAuthenticationError)

**Symptom:**
```
SMTPAuthenticationError: (535, b'5.7.8 Username and password not accepted')
```

**Solution:**
```
IMPORTANT: Use Gmail APP PASSWORD, not your regular password!

Steps:
1. Go to myaccount.google.com
2. Enable 2-Factor Authentication (if not already done)
3. Search for "App passwords"
4. Create password for "Mail" → "Windows" (or your device)
5. Copy the 16-character password
6. Paste into .env EMAIL_PASSWORD field (no spaces)

Example:
EMAIL_PASSWORD=abcd efgh ijkl mnop  ← WRONG (has spaces)
EMAIL_PASSWORD=abcdefghijklmnop      ← CORRECT (no spaces)
```

### Issue 4: Charts not displaying (matplotlib)

**Symptom:**
```
No window opens when running PMO Visualizer scripts
```

**Solution (Windows - Usually pre-configured):**
```bash
# TkAgg backend is already configured in code
# Check if tkinter is available:
python -c "import tkinter; print('OK')"

# If not, install it (depends on your Python installation)
# Re-run Python installer and check "tcl/tk and IDLE"
```

**Solution (macOS):**
```bash
pip install PyQt5
# OR
pip install PyQt6
```

**Solution (Linux):**
```bash
pip install matplotlib[tk]
# Or install tkinter separately:
sudo apt-get install python3-tk
```

### Issue 5: Permission denied writing to Data/Output

**Symptom:**
```
PermissionError: [Errno 13] Permission denied: 'Data/Output/relatorio_final.xlsx'
```

**Solution:**
```bash
# 1. Make sure folder exists
python Scripts/Setup/folder_setup.py

# 2. Check file isn't open in Excel
# (Close Excel if relatorio_final.xlsx is open)

# 3. Check permissions (Linux/macOS)
chmod 755 Data/Output/
chmod 644 Data/Output/*

# 4. On Windows, check antivirus isn't blocking writes
```

### Issue 6: Python not found (Windows)

**Symptom:**
```
'python' is not recognized as an internal or external command
```

**Solution:**
```bash
# Method 1: Use full path
C:\Users\YourUsername\AppData\Local\Programs\Python\Python312\python.exe

# Method 2: Use python3 (if installed)
python3 --version

# Method 3: Add Python to PATH
# 1. Win + R → "envvars.exe"
# 2. New User variable: PYTHON_HOME = C:\...\Python312
# 3. Add to PATH: %PYTHON_HOME%
# 4. Restart terminal

# Method 4: Use Windows PowerShell 7+ (pre-includes Python)
```

### Issue 7: CSV not found (Data/Raw/ empty)

**Symptom:**
```
FileNotFoundError: CSVFile.csv not found in Data/Raw/
```

**Solution:**
```bash
# 1. Place your CSV files in Data/Raw/
# 2. Check file names match config.py settings
# 3. Verify CSV has expected columns:
#    - Project / ProjectName
#    - Horas / Hours
#    - Status
#    - Deadline or date columns
# 4. See DATA_SCHEMA.md for exact format requirements
```

---

## 🔄 Updating Dependencies

### Check for Updates

```bash
# Show which packages have newer versions
pip list --outdated
```

### Update Individual Package

```bash
pip install --upgrade pandas
pip install --upgrade google-generativeai
```

### Update All Dependencies

```bash
pip install --upgrade pip
pip install -r Requirements.txt --upgrade
```

### Lock Current Versions (Safe for Production)

```bash
# Create exact version list
pip freeze > requirements-lock.txt

# Later, restore exact same versions
pip install -r requirements-lock.txt
```

---

## 🔐 Security Best Practices

### Never Commit .env File

The `.env` file is in `.gitignore` and should NEVER be committed to Git:

```bash
# ✅ CORRECT (uses .env.example)
git status
# On branch main
# .env is not listed (protected by .gitignore)

# ❌ WRONG (would expose credentials)
git add .env
# Don't do this!
```

### Rotate Credentials Regularly

```bash
# Monthly: Update API keys
# 1. Create new API key at aistudio.google.com
# 2. Update .env with new key
# 3. Test with Scripts/Setup/test_ai.py
# 4. Delete old API key

# Quarterly: Update email passwords
# 1. Create new Gmail App Password
# 2. Update .env EMAIL_PASSWORD
# 3. Test with Scripts/Setup/enviar_por_email.py
# 4. Delete old app password
```

### Verify No Leaks

Before committing code:

```bash
# Check no credentials in Python files
grep -r "GOOGLE_API_KEY=" Scripts/
grep -r "EMAIL_PASSWORD=" Scripts/
# Should return nothing (credentials in .env only)

# Check no API keys in logs
grep -r "sk-" Logs/
# Should return nothing
```

---

## 📚 Next Steps

After successful setup:

1. **Read ARCHITECTURE.md** - Understand system design
2. **Read DATA_SCHEMA.md** - Set up your CSV files
3. **Read API_INTEGRATION.md** - Configure Gemini AI prompts
4. **Run daily reports** - See it in action
5. **Set up scheduling** - Run automatically (cron/Task Scheduler)

---

## 🆘 Still Having Issues?

1. **Check Logs** - Details in `Logs/pmo_audit.log`
2. **Run Setup Again** - `python Scripts/Setup/folder_setup.py`
3. **Review Error Messages** - Full stack trace shows the problem
4. **Search This Guide** - Use Ctrl+F to find your error message

---

## 📞 Getting Help

If you're still stuck:

1. Check the relevant .md file (ARCHITECTURE.md, API_INTEGRATION.md, etc.)
2. Review the error message carefully (copy-paste in search)
3. Check Python version matches requirement (Python 3.12+)
4. Verify all `.env` variables are filled correctly
5. Run setup scripts again to reset environment

**Good luck!** 🚀
