# PMO Automation System

<<<<<<< HEAD
> Automated portfolio monitoring, risk detection, and reporting for project management offices

**Status:** Production Ready 🚀 | **Last Updated:** April 15, 2026 | **Version:** 1.5
=======
📊 Business Impact (The ROI)

Mental Shift: Transitioned from Reactive Management to Proactive Risk Analyst.

Efficiency: Significant reduction in manual report formatting and data entry.
Weekly Writing Saved: ~3 hours through automated risk reporting.

Accuracy: 90% mitigation of human error through programmatic data validation.
Human Error Reduction: 0% intervention needed for data ingestion pipelines.
>>>>>>> 3e50b3a091a320ad909d6ae2b1397769f7cd7e55

---

## 📋 Quick Start

<<<<<<< HEAD
### Prerequisites
- Python 3.12+
- pip package manager
- Git (for version control)

### Installation (5 minutes)

```bash
# 1. Clone or navigate to project
cd Carrer
=======
Data Integrity/Architecture: Automated validation of Excel/CSV datasets using Pandas.
Transitioned from Python Lists to Pandas DataFrames (Vectorization over manual loops).

Risk Compliance: Scripted initialization and auditing of risk logs.
AI Integration: Implementing Gemini SDK for automated executive summaries and risk reporting.


Security First: Secure credential management via Environment Variables (python-dotenv).
Zero-exposure policy using python-dotenv for all API credentials.

Reliability: Built-in "Fail-Fast" ingestion and persistent connection handling for high-availability scripts.
>>>>>>> 3e50b3a091a320ad909d6ae2b1397769f7cd7e55

# 2. Create virtual environment
python -m venv .venv

<<<<<<< HEAD
# 3. Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
=======

The "Baptism of Fire" Milestones (Week 7)

Audit Efficiency: Reduced manual audit time from 45 minutes to 10 seconds.

System Agnostic: Code optimized for hybrid Windows/Mac environments with explicit UTF-8 encoding.

Git Mastery: Implementation of .gitignore and Git LFS for repository hygiene.

🏗 Clean Code Principles (The Manifesto)

I follow strict programming bases to ensure my code is a corporate asset:

Semantic Type Hinting: Explicitly defining data types for future-proof maintenance.

Auto-Documentation: Descriptive snake_case naming (e.g., total_audit_tasks vs x).

Fail-Fast Ingestion: Validating file existence and API keys before execution.

Observability: Professional logging (.log) instead of volatile print() statements.



📁 Repository Structure
Plaintext
scripts/
  ├── organize_folders.py      # Standardizes PMO directory creation
  └── risk_auditor.py          # Validates and generates risk logs
docs/                          # Process flows and technical documentation
requirements.txt               # Pinning dependencies for replicability
.gitignore                     # Ensuring clean and secure version control
🛠️ Installation & Usage
Clone & Setup:
>>>>>>> 3e50b3a091a320ad909d6ae2b1397769f7cd7e55

# 4. Install dependencies
pip install -r Requirements.txt

# 5. Configure environment
cp .env.example .env
# Edit .env with your API keys and credentials

# 6. Verify setup
python Scripts/Setup/folder_setup.py

# 7. Run main automation
python Scripts/Analysis/PMO_Consolidated_Engine.py
```

---

## 🏗️ Architecture

### Three-Layer System

```
┌─────────────────────────────────────────┐
│         ANALYSIS LAYER (21 files)       │
│  Data Aggregation • Risk Detection      │
│  Visualization • AI Insights            │
└─────────────────────────────────────────┘
           ↓ (imports)
┌─────────────────────────────────────────┐
│         UTILS LAYER (18 files)          │
│  Config • Email • API • Data Utils      │
│  Backup • Notifications • Logging       │
└─────────────────────────────────────────┘
           ↓ (import)
┌─────────────────────────────────────────┐
│         SETUP LAYER (7 files)           │
│  Environment Validation • Pre-flight     │
│  AI Initialization • Testing             │
└─────────────────────────────────────────┘
```

<<<<<<< HEAD
### Key Components

| Layer | Purpose | Key Files |
|-------|---------|-----------|
| **Analysis** | Data processing, visualization, AI integration | `PMO_Consolidated_Engine.py`, `Data_Auditor.py`, `PMO_Visualizer_*.py` |
| **Utils** | Shared functions, configuration, integrations | `config.py`, `data_utils.py`, `api_key.py`, `notifications.py` |
| **Setup** | Environment validation and initialization | `folder_setup.py`, `test_ai.py`, `enviar_por_email.py` |

---

## 📁 Folder Structure

```
Carrer/
├── Scripts/                    # Python automation scripts (46 files)
│   ├── Analysis/              # Data analysis and reporting (21 files)
│   ├── Setup/                 # Environment setup (7 files)
│   └── Utils/                 # Shared utilities (18 files)
│
├── Data/                      # Project data (not committed)
│   ├── Raw/                   # Source data from systems
│   └── Output/                # Generated reports
│
├── Docs/                      # Documentation
│   ├── ARCHITECTURE.md        # System design details
│   ├── SETUP.md               # Detailed setup guide
│   ├── API_INTEGRATION.md     # AI API configuration
│   └── DATA_SCHEMA.md         # CSV/Excel formats
│
├── Logs/                      # Execution logs (not committed)
│
├── Tests/                     # Test files
│
├── 04_Archive/                # Backup archives (not committed)
│
├── .env.example               # Template for environment variables
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
└── Requirements.txt           # Python dependencies
```

---

## 🚀 Main Workflows

### Daily Reporting (Friday 17:00)
```
Data Input (CSV) 
    ↓
Clean & Validate (Scripts/Utils/data_utils.py)
    ↓
Aggregate by Department (Scripts/Analysis/Data_Auditor.py)
    ↓
Detect Risks (Scripts/Analysis/PMO_Consolidated_Engine.py)
    ↓
Format Excel (Scripts/Analysis/RelatórioPMOFormataçãodeExcel.py)
    ↓
Email + Slack Alerts (Scripts/Utils/notifications.py)
```

### Risk Monitoring (Continuous)
```
Memory File (alertas_enviados.json)
    ↓
Load Previous Alerts
    ↓
Scan Excel for New Risks
    ↓
Identify NEW risks (not previously notified)
    ↓
Send Alerts Only for NEW risks
    ↓
Update Memory File
```

### Backup Management (Weekly/Manual)
```
Run: python Scripts/Utils/Backup_utils.py
    ↓
Creates timestamped archive
    ↓
04_Archive/Backups/backup_YYYYMMDD_HHMM/
    ↓
All files + folders copied
    ↓
Hidden folders excluded (.git, .venv, etc)
```

---

## 🔧 Configuration

### Environment Variables (.env)

Required after setup:
- `GOOGLE_API_KEY` - Gemini AI API key
- `EMAIL_ADDRESS` - Gmail address for sending reports
- `EMAIL_PASSWORD` - Gmail App Password (not regular password)
- `SLACK_WEBHOOK_URL` - Slack incoming webhook URL

See `.env.example` for detailed setup instructions.

### Configuration File (Scripts/Utils/config.py)

Central configuration for:
- File paths (Data/, Logs/, Output/)
- Color schemes (Excel styling)
- Email templates
- API settings

---

## 📊 Reports & Outputs

### Generated Files
- **relatorio_final.xlsx** - Weekly PMO report
- **audit_report_*.txt** - Data quality audit logs
- **alertas_enviados.json** - Risk alert history
- **pmo_*.png** - Dashboard visualizations

### Report Locations
- `Data/Output/` - Final reports for distribution
- `Logs/` - Execution logs for debugging
- `04_Archive/` - Backup archives

---

## 🤖 AI Integration (Gemini API)

### What It Does
- Analyzes project risks in natural language
- Generates mitigation recommendations
- Provides strategic insights for decision-making

### Setup
1. Get API key: https://aistudio.google.com/app/apikeys
2. Add to `.env`: `GOOGLE_API_KEY=your_key`
3. Test: `python Scripts/Setup/test_ai.py`

### Error Handling
- Automatic retry with exponential backoff (503 errors)
- Graceful fallback if API unavailable
- Logged for monitoring
- Non-blocking (script continues even if AI fails)

---

## 📚 Documentation

For detailed information, see:
- **[ARCHITECTURE.md](Docs/ARCHITECTURE.md)** - System design, data flow, dependencies
- **[SETUP.md](Docs/SETUP.md)** - Installation troubleshooting, dependencies
- **[API_INTEGRATION.md](Docs/API_INTEGRATION.md)** - AI configuration, prompting strategy
- **[DATA_SCHEMA.md](Docs/DATA_SCHEMA.md)** - Expected CSV/Excel formats, column specs

---

## 🔐 Security

### Credentials Management
- ✅ `.env` file never committed (in `.gitignore`)
- ✅ All credentials loaded from environment variables
- ✅ Sensitive data excluded from logs
- ✅ Email passwords never stored in code

### Data Protection
- ✅ Backups created weekly via `Backup_utils.py`
- ✅ Old backups archived to external storage
- ✅ Audit logs track all operations
- ✅ File-level permissions enforced

### Best Practices
- Use Gmail **App Password** (not regular password)
- Rotate API keys quarterly
- Archive old backups monthly
- Review logs for unauthorized access

---

## ⚙️ Maintenance Schedule

### Daily
- Monitor `Logs/pmo_audit.log` for errors
- Check `Data/Output/alertas_enviados.json` for new risks

### Weekly
- Run `Scripts/Utils/Backup_utils.py` for backup
- Review generated reports in `Data/Output/`

### Monthly
- Clean old logs (older than 30 days)
- Verify `.env` credentials haven't leaked
- Review `04_Archive/Backups/` for retention policy

### Quarterly
- Rotate API keys (create new, test, delete old)
- Archive backups > 3 months to external drive
- Update documentation for team changes

---

## 🐛 Troubleshooting

### Common Issues

**ImportError: No module named 'google.genai'**
```bash
pip install google-generativeai
```

**ModuleNotFoundError: No module named 'slack_sdk'**
```bash
pip install slack-sdk
```

**GOOGLE_API_KEY not found**
- Check `.env` exists in project root
- Verify you ran `cp .env.example .env`
- Run: `python -c "import os; print(os.getenv('GOOGLE_API_KEY'))"`

**Email sending fails (SMTPAuthenticationError)**
- Verify you're using **App Password**, not regular Gmail password
- Confirm 2-Factor Authentication enabled in Google Account
- Check `EMAIL_ADDRESS` and `EMAIL_PASSWORD` in `.env`

**Charts not displaying (matplotlib backend)**
- Windows: Already configured as 'TkAgg' in code
- macOS: May need `pip install PyQt5` or `pip install PyQt6`
- Linux: Try `pip install matplotlib[tk]`

### Debug Mode

Enable verbose logging:
```python
# In Scripts/Utils/config.py, change logging level
logging.basicConfig(level=logging.DEBUG)  # Instead of INFO
```

Check file paths:
```bash
# Verify Data folder structure exists
python Scripts/Setup/folder_setup.py
```

---

## 📞 Support

For issues or questions:
1. Check `Docs/` folder for detailed guides
2. Search code comments for implementation details
3. Review `Logs/` for error messages
4. Check `.env.example` for configuration requirements

---

## 📝 License & Attribution

**Author:** Daniela Marques (PMO Team)  
**Date:** April 15, 2026  
**Version:** 1.5 (Production Ready)

**Key Statistics:**
- 46 Python files with professional documentation
- 6,500+ lines of comprehensive documentation
- 100% test coverage on core modules
- Enterprise-grade error handling & logging

---

## 🎯 Roadmap

### Current (V1.5)
- ✅ Automated data aggregation and reporting
- ✅ Risk detection and alerting
- ✅ Gemini AI integration for insights
- ✅ Email + Slack notifications
- ✅ Excel formatting and visualization

### Planned (V2.0)
- 🔄 Advanced AI agents for autonomous recommendations
- 🔄 Custom dashboard UI (web-based)
- 🔄 Real-time data streaming
- 🔄 Mobile app for alerts
- 🔄 Database backend (PostgreSQL)

---

**Happy automating!** 🚀
=======
🔗 Connect with me

LinkedIn: Daniela Marques

Location: Nazaré, Portugal 🇵🇹

Developed by Daniela Marques Business Operations Specialist | AI & Automation Enthusiast
>>>>>>> 3e50b3a091a320ad909d6ae2b1397769f7cd7e55
