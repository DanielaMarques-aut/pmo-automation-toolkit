"""Data Aggregation Engine - Tuesday Report Generator (V1.0).

This module provides foundational data aggregation functionality for Tuesday-based
project reporting. Demonstrates core pandas operations: DataFrame construction,
groupby aggregation, and risk-based filtering for executive summaries.

Primary Purpose:
    Automate the aggregation of project data (hours, status) into structured
    pivot tables using pandas GroupBy. Identify projects with errors for
    risk assessment and escalation to project managers.

Key Concepts:
    - DataFrame Construction: Create structured data from Python dictionaries
    - Pivot Table Equivalent: Use pandas groupby to calculate sum by project
    - Boolean Indexing: Filter rows based on status conditions
    - Data Transformation: Extract all hours allocated to projects with errors
    - Risk Analysis: Isolate error-status tasks for impact assessment

Workflow:
    1. DATA CREATION: Define project dictionary (Projeto, Horas, Status)
    2. DF CREATION: Convert dictionary to pandas DataFrame
    3. AGGREGATION: Group by project, sum hours (equivalent to Excel pivot table)
    4. VISUALIZATION: Print original table, summary, and error-impact analysis
    5. RISK FILTERING: Extract only projects with 'Erro' status for further review

Dependencies:
    - pandas: DataFrame operations, groupby aggregation, arithmetic operations
    - numpy: numeric operations (imported for compatibility, not actively used in V1)

Examples:
    Run the script for Tuesday data summary:
    
    >>> exec(open('Agregação de dados (V1.0).py').read())
    --- TABELA ORIGINAL ---
    Projeto Status Horas
    0   Alpha     Ok    10
    1    Beta  Erro    20
    ...
    --- PIVOT TABLE EM PYTHON (SOMA DE HORAS) ---
    Projeto  Horas
    0   Alpha     30
    1    Beta     30
    ...
    --- ANÁLISE DE RISCO (PROJETOS COM ERRO) ---
    Projeto  Horas
    0    Beta     20
    1  Gamma      0

Architecture Notes:
    V1.0 is a teaching module demonstrating pandas fundamentals. Not optimized
    for large datasets but serves as foundation for automated reporting. V1.1
    extends this with better formatting and risk notifications.

Roadmap:
    V2: Add data validation and error handling
    V3: Connect to real data sources (CSV/Excel)
    V4: Add visualization (matplotlib/plotly charts)
"""

import pandas as pd
import numpy as np

# 1. CRIAR DADOS (O teu Excel de trabalho)
data = {
    'Projeto': ['Alpha', 'Beta', 'Alpha', 'Gamma', 'Beta', 'Alpha'],
    'Horas': [10, 20, 15, 30, 10, 5],
    'Status': ['Ok', 'Erro', 'Ok', 'Ok', 'Ok', 'Erro']
}
df = pd.DataFrame(data)

print("--- TABELA ORIGINAL ---")
print(df)

# 2. O EQUIVALENTE À PIVOT TABLE (GROUPBY)
# No Excel: Arrastas 'Projeto' para Linhas e 'Horas' para Valores (Soma)
pivot_python = df.groupby('Projeto')['Horas'].sum().reset_index()

print("\n--- PIVOT TABLE EM PYTHON (SOMA DE HORAS) ---")
print(pivot_python)

# 3. FILTRAGEM AVANÇADA (O que a IA faz melhor)
# Isolar apenas projetos com 'Erro' e calcular o impacto
erros_impacto = df[df['Status'] == 'Erro'].groupby('Projeto')['Horas'].sum().reset_index()

print("\n--- ANÁLISE DE RISCO (PROJETOS COM ERRO) ---")
print(erros_impacto)
