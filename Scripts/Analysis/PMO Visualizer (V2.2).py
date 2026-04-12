"""
PMO INTEGRATED SYSTEM (V2.2)
----------------------------
Este código consolida:
1. Estrutura de Dados em Dicionário (Eficiência)
3. Visualização de Saúde de Portfólio (Storytelling)
O objetivo é criar um dashboard executivo que destaca a saúde financeira e o progresso dos projetos,
 usando dados simulados para refletir um cenário real de PMO.O objetivo é criar um dashboard com mais do que um gráfico e
 recber os dados do utilizador para criar um dashboard mais personalizado e interativo.
"""
from csv import excel
import json
import matplotlib.pyplot as plt
import pandas as pd

def graph_lab():
    # 1. THE DATA (Advanced Dictionary Structure)
    # This mimics a real  database
    pmo_portfolio = {
        'Project_ID': ['PRJ-001', 'PRJ-002', 'PRJ-003', 'PRJ-004'],
        'Name': ['AI Integration', 'Cloud Migration', 'Security Audit', 'Legacy Sync'],
        'Budget_Status': [-1500, 2500, -800, 4200],  # Negative is over-budget
        'Completion_Pct': [90, 45, 15, 60]
    }

    add_more = input("Deseja adicionar mais projetos? Y/N: ")
    while add_more.upper() == 'Y':
        project_id = input("Enter Project ID: ")
        name = input(" What's the Project Name: ")
        budget_status = int(input("Budget Status (€): "))
        completion_pct = int(input("Completion Percentage (%): "))
        
        pmo_portfolio['Project_ID'].append(project_id)
        pmo_portfolio['Name'].append(name)
        pmo_portfolio['Budget_Status'].append(budget_status)
        pmo_portfolio['Completion_Pct'].append(completion_pct)
        
        add_more = input("Deseja adicionar mais projetos? Y/N: ")
    df = pd.DataFrame(pmo_portfolio)
    df.to_excel("pmo_portfolio.xlsx", index=False)
   
    # 2. CREATE A MULTI-PLOT DASHBOARD 
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Graph 1: Financial Health (Bars)
    colors = ['red' if x < 0 else 'green' for x in df['Budget_Status']]
    ax1.bar(df['Name'], df['Budget_Status'], color=colors)
    ax1.set_title('Budget Variance (€)')
    ax1.axhline(0, color='black', linewidth=1)

    # Graph 2: Progress vs Target (Horizontal Bars)
    ax2.barh(df['Name'], df['Completion_Pct'], color='skyblue')
    ax2.set_title('Completion Percentage (%)')
    ax2.set_xlim(0, 100)

    plt.suptitle('PMO EXECUTIVE DASHBOARD - WEEK 2 REVIEW', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save & Show
    plt.savefig("Dashboard.png")
    print("🚀 Dashboard saved as 'Dashboard.png'")
    plt.show()
graph_lab()
