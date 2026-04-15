# System Architecture & Design

## Overview

This document describes the system architecture, data flow, and component relationships for the PMO Automation System.

---

## Architecture Layers

The system is organized into **three layers** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ANALYSIS LAYER (V1.5)                        │
│                   Data Processing & Reporting                   │
│  21 files: Aggregation, Auditing, Visualization, AI Integration │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                        (imports)
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    UTILS LAYER (Reusable)                       │
│               Configuration & Shared Services                    │
│   18 files: Config, Email, API, Data Ops, Notifications         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                        (imports)
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    SETUP LAYER (Initialization)                 │
│              Environment Validation & Pre-flight Checks          │
│    7 files: Folder Setup, AI Testing, Email Testing             │
└─────────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

#### 1. Analysis Layer (Scripts/Analysis/)
**Purpose:** Core business logic - data processing, risk detection, reporting

**21 Files:**
- **Data Aggregation** (V1.0, V1.1): Groupby operations, pivot tables
- **Data Auditor**: Project health assessment, overdue detection
- **PMO AI Architecture**: Prompt engineering foundation
- **PMO Visualizer** (V1.8 - V2.4): Dashboard generation, color-coded charts
- **PMO Automation** (V1, V1.2, V2.1): Risk tracking, budget monitoring
- **PMO Consolidated Engine**: Main orchestrator with Gemini AI
- **Relatório** (sexta, sexta 1.1, Formatação): Reporting pipelines

**Dependencies:**
- Imports: `Utils/config.py`, `Utils/data_utils.py`, `Utils/api_key.py`
- External: pandas, matplotlib, openpyxl, google.genai

**Data Inputs:**
- `Data/Raw/*.csv` (project data from source systems)
- `alertas_enviados.json` (risk memory file)

**Data Outputs:**
- `Data/Output/relatorio_final.xlsx` (weekly reports)
- `Data/Output/*.png` (dashboard visualizations)
- `Logs/pmo_audit.log` (audit trails)

#### 2. Utils Layer (Scripts/Utils/)
**Purpose:** Reusable functions, configuration, external integrations

**18 Files:**
- **config.py**: Centralized settings, file paths, color schemes
- **data_utils.py**: Memory I/O, data validation, normalization
- **api_key.py**: Gemini API client with exponential backoff
- **bar_graph_file.py**: Budget distribution charts
- **notifications.py**: Email sending via SMTP
- **notificaçao.py**: Slack integration via webhooks
- **excel_formatter.py**: OpenPyXL styling patterns
- **Backup_utils.py**: Timestamped backup operations
- Plus 10 more utility files (learning, archival, file organization)

**Characteristics:**
- NO business logic (generic, reusable)
- Heavy type hints and docstrings
- Error handling with logging
- Cross-module dependency: All importing modules depend on this

**Exports:**
- Functions: `get_ai_insight()`, `enviar_alerta_slack()`, `normalizar_status()`
- Configuration: `COR_ALVO`, `EMAIL_USER`, `ARQUIVO_EXCEL_FORMATADO`
- Memory operations: `carregar_memoria()`, `salvar_memoria()`

#### 3. Setup Layer (Scripts/Setup/)
**Purpose:** Environment validation before running Analysis

**7 Files:**
- **folder_setup.py**: Create Data/, Logs/, output directories
- **test_ai.py**: Gemini API connectivity validation
- **teste.py**: Verbose environment verification
- **enviar_por_email.py**: Email configuration tester
- **Relatório PMO - Formatação de Excel.py**: Excel styling setup
- **organizar_arquivos.py**: Project structure initialization

**Usage:**
- Run ONCE before first execution: `python Scripts/Setup/folder_setup.py`
- Run to debug environment: `python Scripts/Setup/test_ai.py`
- Run before email-dependent scripts: `python Scripts/Setup/enviar_por_email.py`

**Return Values:**
- Status dictionary: `{'folder_exists': True, 'ai_working': True, ...}`

---

## Data Flow Diagram

### Daily Reporting Workflow (Friday 17:00)

```
CSV Import
  ↓
Data Validation (data_utils.validate)
  ↓
Clean & Normalize (str.replace, pd.to_numeric)
  ↓
Aggregate by Department (groupby.sum)
  ↓
Detect Risks (boolean indexing)
  ↓
Load Historical Alerts (Memory file)
  ↓
Identify NEW Risks Only
  ↓
Format Excel (openpyxl styling)
  ↓
Generate Charts (matplotlib)
  ↓
Create Prompts (AI Architecture)
  ↓
Send Email (SMTP) + Slack (Webhook)
  ↓
Update Memory File
  ↓
Log Results (UTF-8 logging)
```

### AI Integration Flow

```
Structure Project Summary
  ↓                      (Context Injection)
  ↓
Send to Gemini API
  ↓                      (google.genai.models.generate_content)
  ↓
Wait for Response
  ↓                      (Retry with exponential backoff: 2s, 4s, 6s)
  ↓
Parse Recommendation
  ↓                      (Return str of AI_response.text)
  ↓
Inject into Report
  ↓
Email to Stakeholders
```

### Risk Tracking Flow

```
Scan Excel for Red Tasks
  ↓               (Task_ID, Task_Name, Status_Color)
  ↓
Extract Risk List
  ↓               (List of detected risks this run)
  ↓
Check Memory File (alertas_enviados.json)
  ↓               (Previous risks we already notified)
  ↓
Identify Differences
  ↓               (new_risks = current - memory)
  ↓
Send Alerts ONLY for NEW risks
  ↓               (Avoid notification spam)
  ↓
Update Memory File
  ↓               (Add new risks: memory += new_risks)
  ↓
Log Summary
  ↓               ("Sent 3 new alerts, 5 risks under monitoring")
```

---

## Core Concepts

### 1. Vectorization (Pandas optimization)

Instead of looping rows, apply operations to entire columns at C-speed:

```python
# ❌ SLOW (Python loop - slow)
for idx, row in df.iterrows():
    df.at[idx, 'variance'] = row['budget'] - row['spent']

# ✅ FAST (Vectorized - C-speed)
df['variance'] = df['budget'] - df['spent']
```

### 2. Context Injection (AI prompt engineering)

Send structured summaries instead of raw tables:

```python
# ❌ BAD (Raw data - confusing to AI)
prompt = f"Analyze this: {df.to_string()}"

# ✅ GOOD (Structured context)
prompt = f"""
Dept Summary: {dept_summary_dict}
Overdue Projects: {overdue_count}
Risk Level: {portfolio_risk}

Please recommend mitigation strategies.
"""
```

### 3. Fail-Safe Pattern (Error recovery)

Always save outputs before attempting interactive operations:

```python
# ✅ GOOD (Save first, display second)
plt.savefig("chart.png")      # Always succeeds
plt.show()                     # Might fail on headless systems
```

### 4. Memory System (Risk tracking)

JSON file tracks previously notified risks:

```
alertas_enviados.json:
{
  "2026-04-15": ["Project A", "Project B"],
  "2026-04-14": ["Project C"]
}

Current run finds: ["Project A", "Project B", "Project D"]
New risks: ["Project D"]          ← Only send alert for this
```

### 5. Atomic Operations (Backup safety)

`shutil.copytree()` is atomic: succeeds completely or fails completely:

```python
# ✅ SAFE (Atomic - either all copied or none)
shutil.copytree(source, target, dirs_exist_ok=True)

# ❌ UNSAFE (Partial copy possible)
for file in source.iterdir():
    shutil.copy(file, target)
```

---

## Module Dependencies

### Import Hierarchy

```
Scripts/Analysis/PMO_Consolidated_Engine.py
  ├─ import Scripts/Utils/config
  ├─ import Scripts/Utils/data_utils
  ├─ import Scripts/Utils/api_key
  │   └─ (calls get_ai_insight with exponential backoff)
  ├─ import Scripts/Utils/bar_graph_file
  ├─ import Scripts/Utils/notifications
  └─ import google.genai, pandas, pathlib

Scripts/Utils/api_key.py
  ├─ import google.genai
  ├─ import time (for backoff)
  └─ import os (environment variables)

Scripts/Setup/folder_setup.py
  ├─ import Scripts/Utils/config
  └─ import pathlib, pandas
```

### External Dependencies (Requirements.txt)

```
pandas>=2.0.0
openpyxl>=3.1.0
google-generativeai>=0.3.0
requests>=2.31.0
slack-sdk>=3.23.0
python-dotenv>=1.0.0
matplotlib>=3.7.0
```

---

## Execution Sequence

### First Run (Setup Phase)

```bash
1. python Scripts/Setup/folder_setup.py
   → Creates Data/, Logs/, 04_Archive/ directories
   → Returns status dictionary

2. python Scripts/Setup/test_ai.py
   → Validates .env has GOOGLE_API_KEY
   → Tests API connectivity
   → Lists available models

3. python Scripts/Setup/enviar_por_email.py
   → Tests email credentials
   → Sends test message
   → Confirms SMTP configuration
```

### Normal Operation (Analysis Phase)

```bash
1. python Scripts/Analysis/PMO_Consolidated_Engine.py
   → Import all Utils modules (config, api_key, notifications)
   → Load CSV from Data/Raw/
   → Validate and clean data
   → Aggregate by department
   → Detect risks (overdue, over-budget)
   → Get AI insights (via Gemini API with retries)
   → Format Excel report
   → Generate visualizations
   → Send email + Slack alerts
   → Log all results
   → Export to Data/Output/
```

### Maintenance (Backup Phase)

```bash
1. python Scripts/Utils/Backup_utils.py
   → Creates 04_Archive/Backups/backup_YYYYMMDD_HHMM/
   → Copies all files except .git, .venv
   → Excludes hidden folders (.*)
   → Skips large files (optional)
   → Returns backup location path
```

---

## Performance Characteristics

### Time Complexity

| Operation | Time | Scaling |
|-----------|------|---------|
| Load CSV (1000 rows) | 50ms | O(n) |
| Groupby aggregation | 10ms | O(n) |
| Risk detection | 5ms | O(n) |
| Email sending | 2000ms | O(1) constant |
| Gemini API call | 1000ms | O(1) constant |
| Full report generation | 3000ms | O(n) total |

### Storage Requirements

| Component | Size | Notes |
|-----------|------|-------|
| Scripts/ (all 46 files) | 2.5 MB | Source code only |
| Data/Raw/ (historical) | 500 MB | Grows yearly |
| Logs/ (monthly) | 100 MB | Rotated monthly |
| 04_Archive/Backups | 500 MB | 1-2 backups |
| **Total** | **~1.1 GB** | Manageable |

---

## Error Handling Strategy

### Fail-Fast Pattern (Errors stop early)

```python
# 1. Validate inputs immediately
if not file.exists():
    raise FileNotFoundError(f"Cannot find {file}")

# 2. Log and exit on critical errors
if not api_key:
    log.error("GOOGLE_API_KEY not found")
    exit(1)
```

### Graceful Degradation Pattern (Some failures non-blocking)

```python
# AI failures don't stop report generation
try:
    ai_insight = get_ai_insight(summary)
except Exception as e:
    log.warning(f"AI unavailable: {e}")
    ai_insight = "AI insights unavailable"

# Report continues with or without AI
report.include(ai_insight)
```

### Retry Pattern (Transient failures recover)

```python
# Exponential backoff for API transients
for attempt in range(3):
    try:
        response = api.call()
        return response
    except InternalServerError:
        wait = (attempt + 1) * 2  # 2s, 4s, 6s
        time.sleep(wait)
    except Exception:
        raise  # Non-transient errors fail immediately
```

---

## Security Architecture

### Credential Isolation

```
.env (NOT committed)
  ↓
load_dotenv() in Setup
  ↓
os.getenv() in Scripts
  ↓
Never logged or printed
```

### Data Protection

- ✅ Backups created automatically (weekly)
- ✅ Logs stored locally (not uploaded)
- ✅ Email passwords in .env only
- ✅ API keys in environment single source of truth

### Audit Trail

Every operation logged to `Logs/pmo_audit.log`:
```
2026-04-15 14:30:00 - INFO - Started PMO analysis
2026-04-15 14:30:05 - INFO - Loaded 250 rows from CSV
2026-04-15 14:30:06 - INFO - Found 8 overdue projects
2026-04-15 14:30:07 - INFO - 3 new risks detected
2026-04-15 14:30:10 - INFO - Email sent successfully
```

---

## Scalability Considerations

### Current Limits (V1.5)

- CSV size: Up to 10,000 rows (5 seconds)
- Projects: Up to 500 in portfolio
- Email recipients: Single address (broadcast)
- Slack channels: Single webhook

### Scaling Roadmap (V2.0+)

- **Database**: Replace CSV with PostgreSQL (10x data)
- **API**: RESTful endpoints for external consumption
- **UI**: Web dashboard (real-time updates)
- **Scale**: Distributed processing (Celery tasks)
- **Notifications**: Multi-recipient, filtered alerts

---

## Related Documentation

- [SETUP.md](SETUP.md) - Installation and troubleshooting
- [API_INTEGRATION.md](API_INTEGRATION.md) - AI configuration
- [DATA_SCHEMA.md](DATA_SCHEMA.md) - CSV/Excel formats
