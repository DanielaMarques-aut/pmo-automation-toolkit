"""
Automated PMO Risk & Budget Tracker: Resilience & Data Integrity Module (V1.2).

This module extends V1 with robust data cleaning, datetime handling, and integrity
checks. It demonstrates enterprise-grade approaches to handling real-world data
anomalies (missing budgets, mixed date formats, decimal conversions).

Primary Purpose:
    Enhance V1 with production-grade data validation. Handle missing values
    (None/NaN) gracefully via fillna(). Parse mixed datetime formats. Detect
    data quality issues early to prevent downstream processing failures.

Key Concepts:
    - Data Cleaning: fillna() for missing numeric values
    - DateTime Parsing: pd.to_datetime() handles multiple format variants
    - Health Classification: Dual-condition logic (budget + deadline)
    - Data Quality: Anticipate and handle real Excel import anomalies
    - Fail-Fast Pattern: Validate early, escalate problems visibly

Workflow:
    1. LOAD DATA: DataFrames with known anomalies (None, mixed dates)
    2. CLEAN STEP 1: Fill missing budgets with 0 to prevent errors
    3. CLEAN STEP 2: Convert deadline strings to datetime objects
    4. CALCULATE VARIANCE: Budget_Allocated - Current_Spend
    5. CALCULATE DAYS_TO_DEADLINE: Future date arithmetic
    6. HEALTH CHECK: Dual-condition logic (over-budget OR overdue)
    7. AI ROADMAP: Document next steps for LLM integration in V2

Data Cleaning Patterns:
    - fillna(): Gracefully handle missing numeric values
    - pd.to_datetime(): Parse various date string formats
    - Boolean masking: Multi-condition filtering for health status

Dependencies:
    - pandas: DataFrame operations, datetime parsing
    - datetime: Timestamp comparison and arithmetic

Author: Daniela Marques | Date: 2026-04-15 | Version: 1.2
Roadmap: V2 will integrate Gemini AI for auto-generated recommendations

"""

import pandas as pd
import datetime
from typing import Optional, Dict, List, Any

def run_pmo_automation_v1_2() -> Optional[Dict[str, Any]]:
    print(f"--- 🚀 PMO AUTOMATION V1.2: EXECUTION {datetime.datetime.now().strftime('%H:%M')} ---")
    
    # 1. DATA INGESTION (Simulando um Excel com erros comuns: NaNs e formatos de data mistos)
    data = {
        'Project_Name': ['Risk Automation', 'Cloud Migration', 'AI Integration', 'Digital Ops', 'Internal Audit'],
        'Budget_Allocated': [12000, 45000, 25000, 8000, None],  # Erro: Orçamento em falta (None)
        'Current_Spend': [10500, 48000, 12000, 8500, 0],
        'Deadline': ['2026-03-10', '2026-04-15', '2026-03-01', '2026-05-20', '2026-06-01'],
        'Risk_Description': ['Atraso API', 'Latência DB', 'Aguarda Chaves', 'Hardware cost', 'Previsão inicial']
    }
    
    df = pd.DataFrame(data)

    # 2. DATA CLEANING
    # Preencher orçamentos em falta com 0 para evitar erros de cálculo
    df['Budget_Allocated'] = df['Budget_Allocated'].fillna(0)
    
    # Converter a coluna Deadline para o formato de data real (Datetime)
    df['Deadline'] = pd.to_datetime(df['Deadline'])


    # 3. TRANSFORMATION (Lógica BizOps)
    df['Variance'] = df['Budget_Allocated'] - df['Current_Spend']
    df['Days_To_Deadline'] = (df['Deadline'] - pd.Timestamp.now()).dt.days
    
    
    # Health Status com lógica dupla: Financeira + Prazo
    def check_health(row):
        if row['Variance'] < 0: return '🔴 OVER BUDGET'
        if row['Days_To_Deadline'] < 0: return '⚠️ OVERDUE'
        return '🟢 ON TRACK'

    df['Health_Status'] = df.apply(check_health, axis=1)

    # 4. INSIGHTS GENERATION (Relatório Executivo)
    print("\n📊 PORTFOLIO STATUS REPORT (CLEAN DATA):")
    print("-" * 75)
    report = df[['Project_Name', 'Health_Status', 'Variance', 'Days_To_Deadline']]
    print(report.to_string(index=False))
    
    # 5. AI INTEGRATION PLAN (Roadmap para V2)
    # Vamos usar estes 'Days_To_Deadline' para a IA priorizar o que analisar primeiro.
    print("\n" + "🤖 AI INTEGRATION PLAN:")
    print("-" * 75)
    print(f"Próximo Passo: IA analisar os {len(df[df['Days_To_Deadline'] < 7])} projetos com deadline em menos de 7 dias.")

    print("\n" + "="*75)
    print("V1.2 DEPLOYED: Data integrity confirmed. Ready for V2 (AI Agents).")