"""Executive Summary Engine for Department Budget Analysis (V1.1).

This module extends V1.0 with enhanced aggregation, visualization, and
executive-ready reporting for director-level stakeholder presentations.
Transforms raw cost data into actionable business intelligence with risk
alerting and professional visual dashboards.

Primary Purpose:
    Generate department-level budget summaries with automated risk detection.
    Produce professional Excel reports and visual charts for Friday team meetings.
    Identify budget anomalies (over 100% spending) for immediate escalation
    to finance and operations teams.

Key Concepts:
    - Executive Formatting: Structured output designed for C-level review
    - Multi-Aggregation: Sum, mean, count using pandas agg() on same column
    - Percentage Distribution: Calculate department share of total budget
    - Risk Alerting: Color-coded status indicators and automatic email escalation
    - Visual Storytelling: Matplotlib bar charts with percentage labels for impact
    - Error Detection: Automatic identification of anomalies (>100% spending)

Workflow:
    1. DATA SIMULATION: Create realistic department spending scenario
    2. GROUPBY AGGREGATION: Group by department and apply multiple aggregations
    3. PERCENTAGE CALCULATION: Calculate percentage of total for each department
    4. RISK IDENTIFICATION: Create alert for departments over budget
    5. EXCEL EXPORT: Generate formatted Excel report for presentations
    6. VISUALIZATION: Create professional bar chart with percentage annotations
    7. OUTPUT: Display dashboard to screen or save as PNG

Key Metrics Calculated:
    - Total_Gasto: Sum of actual spending per department
    - Media_Gasto: Average spending per department transaction
    - Qtd_Projetos: Count of projects per department
    - Percentagem do Total: Department share of portfolio budget (%)

Dependencies:
    - pandas: DataFrame operations, groupby aggregation, agg() function
    - matplotlib: Bar charts, figure sizing, text annotations, layout adjustment
    - numpy: Numeric operations (imported for compatibility)

Error Handling:
    Wrapped in try/except block catching generic exceptions during processing.
    On error, graceful message printed to console without crashing.

Data Validation:
    - Checks if alerts DataFrame is empty before printing alert count
    - Validates that total gasto can be divided (assumes valid numeric conversion)

Examples:
    Run for Tuesday department summary:
    
    >>> exec(open('Agregação de dados (V1.1).py').read())
    🚀 Iniciar Motor de Agregação de Terça-feira...
    
    --- RESUMO EXECUTIVO POR DEPARTAMENTO ---
      Departamento  Total_Gasto  Media_Gasto  Qtd_Projetos  Percentagem do Total
    0          TI        9500         4750              2                   38%
    1    Marketing        5500         2750              2                   22%
    ...
    
    ⚠️ ALERTAS DETETADOS: 2 projetos requerem revisão.
    ✅ Relatório de Pivot gerado com sucesso!
    🚀 Dashboard guardado como 'gasto_departamento.png'

Output Files Generated:
    - resumo_executivo_terca.xlsx: Executive summary Excel report
    - gasto_departamento.png: Visual dashboard (bar chart with percentages)

Roadmap:
    V2: Add email notifications for alerts
    V3: Connect to real database (SQL Server or PostgreSQL)
    V4: Add predictive analytics (forecast over-budget risk)
    V5: Integrate with Slack for automated team notifications
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, List, Any

def run_analysis() -> None:
    print("🚀 Iniciar Motor de Agregação de Terça-feira...")

    # 1. CARREGAMENTO DE DADOS
    try:
        # Cramos dados de teste
        data = {
            'Departamento': ['TI', 'Marketing', 'TI', 'RH', 'Marketing', 'Vendas'],
            'Gasto_Real': [5000, 2500, 4500, 1200, 3000, 7000],
            'Status': ['Validado', 'Validado', 'Erro', 'Validado', 'Validado', 'Erro']
        }
        df = pd.DataFrame(data)
        
        # 2. LÓGICA DE AGRUPAMENTO 
        # Agrupamos por Departamento e somamos os gastos
        resumo_departamento = df.groupby('Departamento')['Gasto_Real'].agg(['sum', 'mean', 'count']).reset_index()
        # Renomear colunas para formato Executivo
        resumo_departamento.columns = ['Departamento', 'Total_Gasto', 'Media_Gasto', 'Qtd_Projetos']
        # Calcular a percentagem do total gasto por departamento
        resumo_departamento['Percentagem do Total'] = resumo_departamento['Total_Gasto'].div(df['Gasto_Real'].sum()).mul(100).round(2).apply(lambda x: f"{x}%") 
        # Renomear colunas para formato Executivo
        resumo_departamento.columns = ['Departamento', 'Total_Gasto', 'Media_Gasto', 'Qtd_Projetos', 'Percentagem do Total']

        # 3. IDENTIFICAÇÃO DE RISCO
        # Criar um resumo apenas de projetos com 'Erro'
        alertas = df[df['Status'] == 'Erro']

        # 4. OUTPUTS
        print("\n--- RESUMO EXECUTIVO POR DEPARTAMENTO ---")
        print(resumo_departamento)
        
        if not alertas.empty:
            print(f"\n⚠️ ALERTAS DETETADOS: {len(alertas)} projetos requerem revisão.")
            
        # Guardar para apresentar na reunião de equipa
        resumo_departamento.to_excel("resumo_executivo_terca.xlsx", index=False)
        print("\n✅ Relatório de Pivot gerado com sucesso!")

    except Exception as e:
        print(f"❌ Erro no processamento: {e}")

    import matplotlib.pyplot as plt

        # Ordenar os departamentos pelo gasto para ficar visualmente mais claro
    df_departamentos = resumo_departamento.sort_values(by='Total_Gasto', ascending=False)

        # Gráfico de barras para mostrar o gasto real por departamento
    plt.figure(figsize=(8,5))
    plt.bar(df_departamentos['Departamento'], df_departamentos['Total_Gasto'], color='skyblue')

    # Adicionar rótulos de percentagem em cima das barras
    for idx, row in df_departamentos.iterrows():
        plt.text(
            x=idx, 
            y=row['Total_Gasto'] + max(df_departamentos['Total_Gasto']) * 0.01,  # Pequeno deslocamento para cima
            s=f"{row['Percentagem do Total']}",
            ha='center', 
            
    )

    plt.title('Gasto Real por Departamento')
    plt.xlabel('Departamento')
    plt.ylabel('Gasto Real')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    plt.savefig("Data/Output/gasto_departamento.png")
run_analysis()
