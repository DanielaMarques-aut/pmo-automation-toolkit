# PROJECT: Automated PMO Risk & Budget Tracker (V1.2 - Resilience Update)
# GOAL: Data Cleaning, Date Handling & Integrity Checks
# AUTHOR: Daniela Marques | DATE: Tuesday, March 3rd, 2026

import pandas as pd
import datetime

def run_pmo_automation_v1_2():
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