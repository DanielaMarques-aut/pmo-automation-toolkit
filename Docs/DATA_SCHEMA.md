# Data Schema & Format Guide

Complete reference for CSV and Excel file formats used by the PMO Automation System.

---

## 📊 Overview

All data files follow specific schemas to ensure compatibility with the automation scripts. This guide defines:
- Expected file formats (CSV, Excel)
- Required and optional columns
- Data types and validation rules
- Example data for testing

---

## 📥 Input Data: CSV Files

### Location
```
Data/Raw/
├── dados_pmo_segunda.csv    (Main project data)
├── project_status.csv        (Project status & deadlines)
└── projects.csv              (Project portfolio)
```

### File 1: Project Hours Data (dados_pmo_segunda.csv)

**Purpose:** Timesheet and hour allocation data

**Required Columns:**

| Column | Data Type | Example | Notes |
|--------|-----------|---------|-------|
| **id** | Integer | 1001 | Unique employee ID |
| **Nome** | String | Maria Silva | Employee name |
| **Departamento** | String | TI | Department (TI, HR, Ops, etc.) |
| **H reportadas** | String or Float | 40h or 40 | Hours completed this period |
| **H a reportar** | String or Float | 40h or 40 | Hours expected for period |
| **Status** | String | Validado | Status classification |

**Example CSV Content:**
```csv
id,Nome,Departamento,H reportadas,H a reportar,Status
1001,Maria Silva,TI,40h,40h,Validado
1002,João Santos,HR,35,40,Pendente
1003,Ana Costa,TI,40h,40h,Validado
1004,Pedro Nunes,Ops,45h,40h,Atenção
1005,Rita Dias,HR,38,40,Pendente
```

**Data Type Notes:**
- Hours can be numeric (40) or string with suffix (40h, 40hrs)
- Script automatically converts to numeric via `pd.to_numeric(errors='coerce')`
- If conversion fails, marked as NaN (missing)

**Column Variations (Script Handles Both):**
- "H reportadas" or "Hours_Reported" or "HorasReportadas"
- "Departamento" or "Department" or "Dept"
- Column names are case-sensitive; use exact spelling or the script won't find them

---

### File 2: Project Status Data (project_status.csv)

**Purpose:** Project timeline, budget, and completion tracking

**Required Columns:**

| Column | Data Type | Example | Notes |
|--------|-----------|---------|-------|
| **Task_ID** | String | PROJ-001 | Unique project identifier |
| **Task_Name** / **ProjectName** | String | Cloud Migration | Project or task name |
| **Status** | String | Delayed | In Progress, Completed, Delayed |
| **Deadline** | Date | 2026-04-15 | Format: YYYY-MM-DD |
| **Budget_Allocated** | Float | 45000 | Budget in EUR |
| **Actual_Spent** | Float | 48000 | Actual spending in EUR |
| **Manager** | String | João Santos | Responsible manager |

**Example CSV Content:**
```csv
Task_ID,Task_Name,Status,Deadline,Budget_Allocated,Actual_Spent,Manager
PROJ-001,Cloud Migration,In Progress,2026-04-15,45000,48000,João Santos
PROJ-002,Risk Automation,Completed,2026-04-01,12000,10500,Maria Silva
PROJ-003,AI Integration,In Progress,2026-05-20,25000,12000,Ana Costa
PROJ-004,Legacy Update,Delayed,2026-06-01,8000,8500,Pedro Nunes
```

**Date Format:** Must be YYYY-MM-DD or format compatible with `pd.to_datetime()`

**Accepted Formats:**
- 2026-04-15 ✅ (ISO format, preferred)
- 15/04/2026 ✅ (European format)
- April 15, 2026 ✅ (English format)
- 2026-04-15 10:30:00 ✅ (With time)

---

### File 3: Project Portfolio (projects.csv)

**Purpose:** High-level project overview and resource allocation

**Required Columns:**

| Column | Data Type | Example | Notes |
|--------|-----------|---------|-------|
| **ProjectName** | String | Digital Transformation | Project name (can be long) |
| **Budget** | Float | 100000 | Total project budget |
| **Manager** | String | Daniela Marques | Project owner |
| **Priority** | String | High | Priority level |
| **Risk_Level** | String | Medium | Assessed risk level |

**Example CSV Content:**
```csv
ProjectName,Budget,Manager,Priority,Risk_Level
Digital Transformation,100000,Daniela Marques,High,Medium
Infrastructure Upgrade,50000,João Santos,High,Low
Security Audit,25000,Ana Costa,Medium,Medium
Legacy System Maintenance,15000,Pedro Nunes,Low,High
```

---

## 📤 Output Data: Excel Files

### Location
```
Data/Output/
├── relatorio_final.xlsx               (Main report)
├── relatorio_final_sexta.xlsx         (Friday report)
├── audit_report_2026-04-15_10-30.txt (Audit log)
└── alertas_enviados.json              (Risk tracking)
```

### File 1: Main Report (relatorio_final.xlsx)

**Purpose:** Formatted Excel report for stakeholder distribution

**Sheets:**
1. **Summary** (Index 0)
   - Overview statistics
   - Key metrics (total budget, projects, risks)
   
2. **Details** (Index 1)
   - Project-by-project breakdown
   - Status, budget variance, deadlines
   
3. **Risks** (Index 2)
   - High-risk projects highlighted
   - Red color coding for visual impact

**Column Structure:**

| Column | Format | Example |
|--------|--------|---------|
| A | Project Name | Cloud Migration |
| B | Status | Delayed |
| C | Budget Variance | -€3,000 |
| D | Days to Deadline | -5 (overdue) |
| E | Risk Level | 🔴 High |

**Formatting:**
- **Header Row:** Dark blue background, white text, bold
- **Risk Rows:** Red background if variance < 0 or overdue
- **Normal Rows:** White background, black text
- **Column Width:** Auto-fitted for readability

**Example (Visual):**
```
┌─────────────────────────────────────────────────────┐
│ PROJECT PORTFOLIO SUMMARY                           │
├─────────────────┬──────────┬──────────┬─────────────┤
│ Project         │ Status   │ Variance │ Days Left   │
├─────────────────┼──────────┼──────────┼─────────────┤
│ Cloud Migration │ Delayed  │ -€3,000  │ -5 (RED)    │
│ Risk Automation │ On Track │ +€1,500  │ 8           │
│ AI Integration  │ At Risk  │ +€13,000 │ 35          │
└─────────────────┴──────────┴──────────┴─────────────┘
```

---

### File 2: Risk Tracking JSON (alertas_enviados.json)

**Purpose:** Memory file tracking which risks have been notified (prevents duplicate alerts)

**Format:**
```json
{
  "2026-04-15": [
    "Cloud Migration",
    "Legacy System"
  ],
  "2026-04-14": [
    "Risk Automation",
    "Database Optimization"
  ]
}
```

**Structure:**
- **Keys:** Dates when alerts were sent (YYYY-MM-DD format)
- **Values:** Array of risk names that were notified

**How It Works:**
1. Script runs and finds current risks: ["Cloud Migration", "Legacy System", "New Risk"]
2. Loads memory file and checks 2026-04-14: ["Risk Automation", "Database Optimization"]
3. Compares: New risks = ["New Risk"]
4. Sends alert ONLY for "New Risk"
5. Updates memory: Adds "New Risk" and today's date

**Update Mechanism:**
```python
# Load previous alerts
previous = load_memory()  # {"2026-04-14": [...]}

# Find new risks
current_risks = detect_risks()  # ["Cloud Migration", "New Risk"]
old_risks = previous.get("2026-04-14", [])
new_risks = set(current_risks) - set(old_risks)

# Send alerts only for new ones
for risk in new_risks:
    send_alert(risk)

# Update memory
memory["2026-04-15"] = current_risks
save_memory(memory)
```

---

## 📝 CSV Data Entry Rules

### Column Names (Case Sensitive)

**Recommended Column Names:**

| Portuguese | English | Accepted Variants |
|------------|---------|-------------------|
| Nome | Name | Nome |
| Departamento | Department | Dept, Depart |
| Horas | Hours | H reportadas, HorasReportadas |
| Status | Status | Estado |
| DataVencimento | Deadline | Data, Prazo |

**If Using Different Names:**
Update `Scripts/Utils/config.py`:
```python
# Default column mappings
COLUMNS = {
    "name_col": "Nome",
    "hours_col": "H reportadas",
    "status_col": "Status"
}

# Change to your column names:
COLUMNS = {
    "name_col": "Employee",
    "hours_col": "HoursWorked",
    "status_col": "TaskStatus"
}
```

---

### Data Type Rules

**Numeric Columns (Budget, Hours):**
- Accept: `40`, `40.0`, `40.5`
- Accept: `"40.5h"`, `"40h"`, `"40 hours"`
- Script strips non-numeric chars except decimal point
- Missing/invalid values → NaN (handled as 0 or excluded)

**Date Columns (Deadline, StartDate):**
- Accept: `2026-04-15`, `04/15/2026`, `April 15, 2026`
- Format: Any format recognized by `pd.to_datetime()`
- Script converts all to datetime objects
- Sorting/comparison: Works automatically after conversion

**String Columns (Name, Status):**
- Accept: Any text
- Script auto-strips whitespace
- Case-sensitive: "In Progress" ≠ "in progress"
- For filtering, use exact case match

**Special Values:**
- Empty cells: Treated as NaN (missing value)
- Space-only cells: Treated as empty
- Error values: Can cause conversion failures
  - Solution: Check for non-numeric characters in Numeric columns

---

## ✅ Data Validation Rules

The system validates data during import:

### Rule 1: No Empty Required Columns
```python
if df[required_col].isna().any():
    raise ValueError(f"Missing values in {required_col}")
```

### Rule 2: Numeric Conversion
```python
# Handles "40h" → 40
df['hours'] = pd.to_numeric(df['hours'].str.replace('h', ''), errors='coerce')
# errors='coerce': Bad values → NaN (silent)
# errors='raise': Bad values → Exception (loud)
```

### Rule 3: Date Parsing
```python
df['deadline'] = pd.to_datetime(df['deadline'])
# Handles multiple formats automatically
```

### Rule 4: Duplicate Headers
```python
# If CSV has "Status" twice, second one becomes "Status.1"
# Script filters out rows where Task_ID == 'Task_ID' (duplicate headers)
df_clean = df[df['Task_ID'] != 'Task_ID']
```

---

## 🧪 Test Data

### Minimal Test CSV (copy to Data/Raw/test.csv)

```csv
id,Nome,Departamento,H reportadas,H a reportar,Status
1001,João Silva,TI,40,40,Validado
1002,Maria Santos,HR,35,40,Pendente
1003,Pedro Costa,TI,40,40,Validado
1004,Ana Nunes,Ops,45,40,Atenção
1005,Rita Dias,HR,38,40,Verificar
```

### Minimal Test Project CSV

```csv
Task_ID,Task_Name,Status,Deadline,Budget_Allocated,Actual_Spent,Manager
PROJ-001,Cloud Migration,In Progress,2026-04-15,45000,48000,João Silva
PROJ-002,Risk Automation,Completed,2026-04-01,12000,10500,Maria Santos
PROJ-003,AI Integration,In Progress,2026-05-20,25000,12000,Ana Nunes
```

### Test Command

```bash
# Run with test data
python Scripts/Analysis/Data_Auditor.py
# Reads from Data/Raw/ (change filename if needed)
# Outputs to Data/Output/ and Logs/

# Check results
cat Logs/pmo_audit.log          # See what happened
ls Data/Output/relatorio_final.*  # Check outputs
```

---

## 🔄 Data Import Best Practices

### 1. CSV Export from Excel

```
1. Open Excel file with your data
2. File → Save As
3. Format: "CSV (Comma delimited) (.csv)"
4. Save to: Data/Raw/dados.csv
5. Copy to Data/Raw/ folder
6. Run automation
```

**Important:** Don't convert in Excel → CSV, it may change formats!

### 2. CSV from Google Sheets

```
1. Open Google Sheet
2. File → Download → CSV
3. Rename if needed
4. Move to Data/Raw/
5. Run automation
```

### 3. CSV from Database

```python
# SQL Server / Oracle / PostgreSQL
import pandas as pd

# Query directly
df = pd.read_sql("SELECT * FROM projects", connection)

# Save as CSV
df.to_csv('Data/Raw/projects.csv', index=False)

# Verify
print(df.head())
```

---

## 🚨 Common Data Issues & Fixes

### Issue 1: Dates Not Recognized

**Symptom:**
```
ValueError: time data '15-04-2026' does not match format '%Y-%m-%d'
```

**Fix:**
Make sure dates are in one of these formats:
- `2026-04-15` ✅ (ISO - preferred)
- `04/15/2026` ✅
- `April 15, 2026` ✅

Convert in Excel before export:
```excel
=TEXT(A1, "YYYY-MM-DD")  # Converts to ISO format
```

### Issue 2: Numeric Columns Contains Text

**Symptom:**
```
Budget column has values like "€45,000" or "45K"
```

**Fix:**
Remove currency symbols and letters:
- Before: `€45,000`
- After: `45000`

In Excel:
```excel
=VALUE(SUBSTITUTE(SUBSTITUTE(A1, "€", ""), ",", ""))
```

### Issue 3: Duplicate Column Names

**Symptom:**
```
FileNotFoundError: Column 'Status' appears twice
```

**Fix:**
Check CSV headers, remove duplicates:
```csv
# ❌ WRONG
Status,Name,Status

# ✅ CORRECT
Status,Name,Priority
```

### Issue 4: Extra Whitespace

**Symptom:**
```
Status ' In Progress' not recognized (has leading space)
```

**Fix:**
Script auto-strips whitespace (should work), but manually clean in Excel:
```excel
=TRIM(A1)  # Removes leading/trailing spaces
```

### Issue 5: Wrong Column Names

**Symptom:**
```
KeyError: 'Name' column not found
```

**Check:** Column is actually named something else:
- "Employee" instead of "Name"
- "Dept" instead of "Departamento"
- "Budget" instead of "Budget_Allocated"

**Fix:** Use exact column names, or update Scripts/Utils/config.py

---

## 📚 Reference

**Pandas to_numeric():**
```python
pd.to_numeric(df['hours'], errors='coerce')
# errors='coerce': Convert unparseable values to NaN
# errors='raise': Raise exception on unparseable values (default)
```

**Pandas to_datetime():**
```python
pd.to_datetime(df['deadline'])
# Auto-detects format: DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD, etc.
```

**Export to CSV:**
```python
df.to_csv('output.csv', index=False)  # Don't include row numbers
```

---

## 🎯 Quick Checklist

Before running automation:

- [ ] CSV files in `Data/Raw/` folder
- [ ] Column names match expected (or config.py updated)
- [ ] No duplicate column names
- [ ] Dates in standard format (YYYY-MM-DD or similar)
- [ ] No currency symbols in numeric columns
- [ ] No extra spaces in text columns
- [ ] No blank rows at top of CSV
- [ ] First row contains headers (column names)
- [ ] No merged cells in Excel source
- [ ] Saved as CSV (comma-separated), not XLSX

---

**Good luck with your data!** 📊
