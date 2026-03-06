# PROJECT: Automated PMO Risk & Budget Tracker (V1)
# GOAL: Automate Financial Variance and Project Health Monitoring
# AUTHOR: Daniela Marques | DATE: Monday, March 2nd, 2026

import pandas as pd
import datetime

def run_pmo_automation_v1():
    print(f"--- 🚀 PMO AUTOMATION V1: EXECUTION {datetime.datetime.now().strftime('%H:%M')} ---")
    
    # 1. DATA INGESTION (Simulando a base de dados )
    data = {
        'Project_Name': ['Risk Automation', 'Cloud Migration', 'AI Integration', 'Digital Ops'],
        'Budget_Allocated': [12000, 45000, 25000, 8000],
        'Current_Spend': [10500, 48000, 12000, 8500],
        'Risk_Level': ['Low', 'High', 'Medium', 'Medium'],
        'Risk_Description': [
            'Atraso na documentação da API',
            'Latência na base de dados (atraso de 2 dias)',
            'Aguarda chaves de API do stakeholder',
            'Excesso de orçamento devido a custos de hardware'
        ]
    }
    
    # Criamos o DataFrame (A "tabela inteligente" do Python)
    df = pd.DataFrame(data)

    # 2. TRANSFORMATION (A Automação BizOps)
    df['Variance'] = df['Budget_Allocated'] - df['Current_Spend']
    df['Health_Status'] = df['Variance'].apply(lambda x: '🔴 OVER BUDGET' if x < 0 else '🟢 ON TRACK')

    # 3. INSIGHTS GENERATION
    print("\n📊 PORTFOLIO STATUS REPORT:")
    print("-" * 65)
    report = df[['Project_Name', 'Health_Status', 'Variance']]
    print(report.to_string(index=False))
    
    # 4. CRITICAL ALERTS
    critical_projects = df[df['Variance'] < 0]
    if not critical_projects.empty:
        print("\n⚠️ ACTION REQUIRED:")
        for _, row in critical_projects.iterrows():
            print(f" -> {row['Project_Name']} precisa de revisão orçamental (Deficit: {row['Variance']}€)")
    else:
        print("\n✅ Financeiramente saudável: Todos os projetos dentro do budget.")

    # -------------------------------------------------------------------------
    # 5. AI_INTEGRATION_PLAN (Roadmap para V2 - Agente de Inteligência Artificial)
    # -------------------------------------------------------------------------
    # Este bloco define a arquitetura para a integração de Generative AI (LLMs).
    # Objetivo V2: Utilizar Gemini API para analisar a 'Risk_Description' e 
    # gerar planos de mitigação baseados no 'Health_Status'.
    
    print("\n" + "🤖 AI INTEGRATION PLAN (Roadmap para V2):")
    print("-" * 65)
    for _, row in df.iterrows():
        # Exemplo da tarefa que a IA irá executar na V2:
        print(f"Project: {row['Project_Name']}")
        print(f"   > Contexto IA: Status {row['Health_Status']} | Risco: {row['Risk_Description']}")
        print(f"   > Próximo Passo: Conectar API para gerar recomendações de mitigação.\n")

    print("="*65)
    print("V1 DEPLOYED: Processamento de dados concluído. Pronto para escalar com IA.")
