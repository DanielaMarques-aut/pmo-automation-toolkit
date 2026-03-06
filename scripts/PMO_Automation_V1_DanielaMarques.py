
# Project: Automated PMO Risk Tracker
# Goal: Automate the formatting of project risks for stakeholder reporting.
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