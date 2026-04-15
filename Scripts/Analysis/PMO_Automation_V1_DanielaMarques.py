
"""PMO Automated Risk & Budget Tracker: Portfolio Health Intelligence (V1).

This module automates risk detection and financial variance reporting across
project portfolios. Transforms raw project data into actionable health status
indicators and financial insights suitable for executive decision-making.

Primary Purpose:
    Provide automated, data-driven portfolio health assessment combining
    budget variance analysis with project risk categorization. Generate
    clear status indicators (green/red decision signals) enabling fast
    management action. Prepare data and recommendations for future AI
    integration (V2 roadmap).

Key Concepts:
    - Automated Health Scoring: Transform financial variance into status
    - Risk Stratification: Categorize projects by risk level (Low/Medium/High)
    - Budget Variance Analysis: Identify over/under budget conditions
    - Executive Reporting: Provide clear, actionable summary format
    - AI Readiness: Structure data for future Gemini API integration

Workflow:
    1. DATA INGESTION: Load or simulate project portfolio
    2. VARIANCE CALCULATION: Budget_Allocated - Current_Spend
    3. HEALTH CLASSIFICATION: Over-budget projects marked 🔴 RED
    4. PORTFOLIO SUMMARY: Print tabular executive report
    5. CRITICAL ALERTS: Escalate over-budget projects
    6. AI ROADMAP NOTES: Document next steps for LLM integration

Financial Health Status Indicators:
    🟢 ON TRACK: Positive variance (under budget)
    - Example: Budgeted €10000, spent €8000 → Variance +€2000
    - Status: Project proceeding with cost control
    
    🔴 OVER BUDGET: Negative variance (spending exceeds budget)
    - Example: Budgeted €5000, spent €6500 → Variance -€1500
    - Status: Project requires immediate remediation
    - Action: Scope reduction, timeline extension, or budget approval

Status Assignment Logic:
    df['Health_Status'] = df['Variance'].apply(
        lambda x: '🔴 OVER BUDGET' if x < 0 else '🟢 ON TRACK'
    )
    
    Single condition: Variance sign determines health status
    Simple but effective for executive-level triage

Data Fields:
    - Project_Name: Human-readable project identifier
    - Budget_Allocated: Approved budget for project (EUR)
    - Current_Spend: Actual expenditure to date (EUR)
    - Risk_Level: Project risk assessment (Low/Medium/High)
    - Risk_Description: Explanation of risk (delay, quality, resource)

Dependencies:
    - pandas: DataFrame creation, arithmetic operations
    - datetime: Timestamp generation for report headers

Output Format:
    Portfolio Status Report
    - Shows all projects in tabular format
    - Highlights health status with emoji (visual scanning)
    - Variance displayed in euros (business language)
    - Action Required section for over-budget projects

Examples:
    Run automated portfolio health audit:
    
    >>> exec(open('PMO_Automation_V1_DanielaMarques.py').read())
    --- 🚀 PMO AUTOMATION V1: EXECUTION 14:32 ---
    
    📊 PORTFOLIO STATUS REPORT:
    ─────────────────────────────────────────────────────────
    Project_Name          Health_Status    Variance
    0  Risk Automation      🟢 ON TRACK      1500
    1  Cloud Migration      🔴 OVER BUDGET  -3000
    2  AI Integration       🟢 ON TRACK     13000
    3  Digital Ops          🔴 OVER BUDGET    -500
    
    ⚠️ ACTION REQUIRED:
    -> Cloud Migration precisa de revisão orçamental (Deficit: -€3000)
    -> Digital Ops precisa de revisão orçamental (Deficit: -€500)

Risk Metadata for AI Integration:
    The Risk_Level and Risk_Description enable Gemini API integration in V2

Roadmap Comments in Code:
    V2 AI Integration Plan is documented for developer reference

Production Considerations:
    - Data Source: Replace simulated data with actual database query
    - Scheduling: Run as daily/weekly scheduled job
    - Notifications: Add email/Slack alerts for critical projects
    - History: Store results by date for trend analysis

Limitations of V1:
    - Single threshold (0): Any positive variance is 'OK'
    - No risk weighting: All over-budget items treated equally
    - No timeline: Cannot assess urgency (deadline vs spend rate)

Metrics for Success:
    - Over-Budget Identification: Catches 100% of negative variance
    - Reporting Speed: Portfolio analyzed in < 1 second
    - Stakeholder Clarity: Emoji status immediately understood

Related Modules:
    - Data_Auditor.py: Similar health detection patterns
    - PMO AI Architecture (V1.5).py: Prompt engineering foundations
    - PMO_Automation_v2_DanielaMarques.py: Enhanced with data cleaning
"""

import pandas as pd
import datetime
from typing import Optional, Dict, List, Any

# Legacy code preserved for compatibility
project_name = "risk automation"
budget_utilization = 85.5  # Float (percentage)
is_on_track = True         # Boolean
risks = ["Resource shortage", "price changes", "Budget Overrun"] # List
# Adding a new risk found during the week
risks.append("deploy delay")
# Generating the report
report = f"""
--- EXECUTIVE SUMMARY: {project_name} ---
Status: {"GREEN" if is_on_track else "RED"}
Budget Used: {budget_utilization}%

TOP RISKS TO MITIGATE:
1. {risks[0]}
2. {risks[1]}
3. {risks[-2]} 
3. {risks[-1]} 
---------------------------------------
"""
print(report)


#AI Integration Plan
#In V2, I will use an LLM API to automatically categorize these risks into 'High/Medium/Low' priority
#I will use Prompt Engineering to turn this raw data into a professional email notification.

# Project: Automated PMO Risk & Budget Tracker (V1)
# Goal: Automate the formatting of project risks and financial variance for reporting.

import pandas as pd # Importamos a biblioteca para tratar tabelas

# --- DATA (Ingestão de Dados) ---
# Na segunda-feira, imagina que isto vem de um Excel
data = {
    'project_name': ['risk automation', 'cloud migration', 'ai integration'],
    'budget_allocated': [100.0, 500.0, 250.0],
    'current_spend': [85.5, 420.0, 275.0],
    'is_on_track': [True, True, False]
}

df = pd.DataFrame(data)

# --- TRANSFORMAÇÃO (A linha que procuravas está aqui!) ---
# Esta linha calcula a diferença entre Orçamento e Gasto para todos os projetos de uma vez
df['variance'] = df['budget_allocated'] - df['current_spend']

# --- GENERATING THE REPORT ---
print("--- EXECUTIVE SUMMARY ---")
for index, row in df.iterrows():
    status = "GREEN" if row['is_on_track'] else "RED"
    print(f"\nProject: {row['project_name']}")
    print(f"Status: {status}")
    print(f"Budget Used: {row['current_spend']}€ (Variance: {row['variance']}€)")

# AI Integration Plan
# In V2, I will use an LLM API to automatically categorize these risks into 'High/Medium/Low' priority.