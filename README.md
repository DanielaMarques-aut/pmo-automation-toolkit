# PMO Automation Toolkit

> Automated portfolio monitoring, risk detection, and AI-powered reporting for project management offices.

Built by a Business Operations Specialist transitioning into AI & Automation — this toolkit replaces 45 minutes of manual reporting with a 10-second script.

---

## What It Does

| Feature | Description |
|---|---|
| 📊 **Risk Detection** | Scans project data and flags overdue or over-budget projects |
| 🤖 **AI Insights** | Uses Gemini API to generate executive summaries and mitigation plans |
| 📧 **Automated Alerts** | Sends email and Slack notifications only for *new* risks (no spam) |
| 📁 **Excel Reporting** | Generates colour-coded weekly PMO reports automatically |
| 🔒 **Audit Trail** | Full logging of every operation for compliance and debugging |

---

## Business Impact

- ⏱️ **Audit time reduced from 45 minutes to 10 seconds**
- 📉 **~3 hours/week saved** on manual report formatting
- ✅ **90% reduction in human error** through programmatic data validation
- 🔁 **Zero duplicate alerts** via persistent memory system (`alertas_enviados.json`)

---

## Architecture

The system is organised into three layers with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│         ANALYSIS LAYER (21 files)       │
│  Risk Detection · AI Insights           │
│  Data Aggregation · Visualisation       │
└────────────────────┬────────────────────┘
                     │ imports
┌────────────────────▼────────────────────┐
│         UTILS LAYER (18 files)          │
│  Config · Email · Gemini API            │
│  Logging · Backup · Notifications       │
└────────────────────┬────────────────────┘
                     │ imports
┌────────────────────▼────────────────────┐
│         SETUP LAYER (7 files)           │
│  Environment Validation · Pre-flight    │
│  AI Testing · Email Testing             │
└─────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites
- Python 3.12+
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/DanielaMarques-aut/pmo-automation-toolkit
cd pmo-automation-toolkit

# 2. Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r Requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your API keys (see Configuration section)

# 5. Validate environment
python Scripts/Setup/folder_setup.py

# 6. Run the main automation
python main.py
```

---

## Configuration

Copy `.env.example` to `.env` and fill in your credentials:

```env
GOOGLE_API_KEY=your_gemini_api_key
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_16_char_app_password
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your/webhook
```

> ⚠️ `.env` is in `.gitignore` and is **never committed**. Use Gmail App Passwords, not your regular password.

Get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com/app/apikeys) — no credit card required.

---

## Project Structure

```
pmo-automation-toolkit/
├── main.py                     # Main orchestrator
├── Requirements.txt
├── .env.example                # Credential template
│
├── Scripts/
│   ├── Analysis/               # Core business logic (21 files)
│   │   ├── PMO_Consolidated_Engine.py
│   │   ├── Data_Auditor.py
│   │   └── PMO_Visualizer_*.py
│   ├── Utils/                  # Shared utilities (18 files)
│   │   ├── config.py
│   │   ├── api_key.py          # Gemini integration
│   │   └── notifications.py
│   └── Setup/                  # Environment validation (7 files)
│
├── Data/
│   ├── Raw/                    # Input CSV files
│   └── Output/                 # Generated reports
│
├── Docs/                       # Technical documentation
└── Logs/                       # Execution logs
```

---

## How Risk Tracking Works

The system uses a **memory file** (`alertas_enviados.json`) to avoid sending duplicate alerts:

```
1. Detect current risks in the data
2. Load previously notified risks from memory
3. Calculate: new_risks = current - previous
4. Send alerts ONLY for new risks
5. Update memory file
```

This means your team gets notified once per risk — not every time the script runs.

---

## AI Integration

The Gemini API generates:
- **Executive summaries** from raw project data
- **3-step mitigation plans** for at-risk projects
- **Budget optimisation recommendations**

The integration uses exponential backoff (2s → 4s → 6s) for retries and fails gracefully — reports are generated even if the AI is unavailable.

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0-150458?logo=pandas&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Gemini_API-AI-4285F4?logo=google&logoColor=white)
![OpenPyXL](https://img.shields.io/badge/OpenPyXL-Excel-217346?logo=microsoftexcel&logoColor=white)

- **pandas** — data manipulation and aggregation
- **openpyxl** — Excel report formatting
- **google-generativeai** — Gemini AI integration
- **python-dotenv** — secure credential management
- **matplotlib** — dashboard visualisation
- **slack-sdk** — Slack webhook notifications

---

## Roadmap

- [x] Automated data aggregation and risk detection
- [x] Gemini AI integration for executive insights
- [x] Email + Slack notifications with deduplication
- [x] Excel report formatting and visualisation
- [ ] Web dashboard (real-time)
- [ ] PostgreSQL backend to replace CSV
- [ ] Scheduled runs via GitHub Actions

---

## Documentation

| File | Contents |
|---|---|
| [ARCHITECTURE.md](Docs/ARCHITECTURE.md) | System design, data flow, dependencies |
| [SETUP.md](Docs/SETUP.md) | Installation, troubleshooting |
| [API_INTEGRATION.md](Docs/API_INTEGRATION.md) | Gemini AI configuration and prompt engineering |
| [DATA_SCHEMA.md](Docs/DATA_SCHEMA.md) | CSV and Excel format specifications |

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

**Daniela Marques** · Business Operations Specialist → AI & Automation  
📍 Portugal · [LinkedIn]([https://www.linkedin.com/in/daniela-marques](https://www.linkedin.com/in/daniela-marques-7734276a/))
