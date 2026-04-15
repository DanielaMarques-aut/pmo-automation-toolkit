"""Project Health Auditor with Budget Variance Detection (Data_Auditor).

This module performs multi-dimensional project auditing combining task status
analysis with budget variance tracking. Provides early warning system for
pending, delayed, and over-budget tasks requiring immediate management action.

Primary Purpose:
    Automated health audit of project portfolios through data validation,
    status filtering, and budget analysis. Generates visual reports and
    alert summaries for Ops teams. Enables proactive risk management
    before cost overruns and schedule slippages become critical.

Key Concepts:
    - Clean Code Principles: Type hinting for parameter clarity
    - Data Abstraction: CSV to DataFrame transformation
    - Boolean Indexing: Efficient filtering of task statuses
    - Numeric Coercion: Safe conversion of budget strings to floats
    - Variance Calculation: Budget allocated vs actual spend analysis
    - Visual Analysis: Matplotlib charts for stakeholder communication
    - Multi-Level Alerts: Escalation based on severity (pending/delayed/over-budget)

Workflow:
    1. FILE LOADING: Read CSV project file with optional header cleanup
    2. DATA VALIDATION: Remove duplicate headers and validate column existence
    3. TASK FILTERING: Identify pending, delayed, and over-budget tasks
    4. STATUS REPORTING: Print alerts for each anomaly type
    5. BUDGET ANALYSIS: Calculate variance and visualize by status
    6. VARIANCE DETECTION: Flag projects over budget for escalation

Task Status Categories:
    - In Progress: Pending with planned completion
    - Delayed: Past deadline with ongoing work
    - Completed: Finished projects
    - Over Budget: Actual spend exceeds allocated budget

Budget Variance Logic:
    - Budget_Diff = Budget_Allocated - Actual_Spent
    - Positive variance: Under budget (good cost control)
    - Negative variance: Over budget (requires action)

Dependencies:
    - pandas: DataFrame operations, data type conversion, groupby analysis
    - pathlib: Cross-platform file path handling
    - matplotlib.pyplot: Visual dashboard generation

Error Handling:
    - FileNotFoundError: Graceful error message if CSV not found
    - Generic Exception: Catch-all for unexpected errors during analysis

Data Validation:
    - Header row filtering: Removes duplicate headers in data stream
    - Type coercion: Uses 'coerce' mode to handle invalid budget entries
    - Empty DataFrame check: Validates before printing detailed analysis

Examples:
    Audit project portfolio from CSV:
    
    >>> from pathlib import Path
    >>> audit_project_health(Path("data/project_status.csv"))
    🔍 Analisando saúde do projeto...
    
    ⚠️ Alerta: Existem 3 tarefas pendentes.
    ❌ Alerta: Existem 2 tarefas atrasadas.
    ⚠️ Alerta: Existem 5 tarefas acima do orçamento.
    
    Variance by Status (displayed as bar chart):
    Budget_Diff
    In Progress:   5000€  (positive variance)
    Delayed:      -3000€  (negative variance)

Key Outputs:
    - Console alerts for pending and delayed tasks
    - Matplotlib bar chart: Variance distribution by status
    - List of over-budget tasks with budget/actual/variance columns

Assumptions:
    - CSV has columns: Task_ID, Task_Name, Status, Budget_Allocated, Actual_Spent
    - File exists in data/ subfolder relative to script location
    - Data is reasonably clean (handles some missing values gracefully)

Roadmap:
    V2: Add email notifications for critical alerts
    V3: Integrate with project management APIs (Jira, Azure DevOps)
    V4: Add predictive variance forecasting (ML-based cost estimation)
    V5: Connect to real-time data warehouse for continuous monitoring
"""

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Optional

def audit_project_health(file_path: Path) -> None:
    """
    CLEAN CODE PRINCIPLE: Type Hinting
    Usamos ': Path' para dizer ao Python que esperamos um objeto de caminho.
    BASES: Data Abstraction - Transformamos uma tabela num DataFrame.
    """
    try:
        # Carregar os dados
        df: pd.DataFrame = pd.read_csv(file_path) # Ou pd.read_excel para ficheiros .xlsx
        
        print("🔍 Analisando saúde do projeto...")
    # 2. Filter out rows where the Task_ID is actually the header string
    # This keeps only "Real" data
        df_clean: pd.DataFrame = df[df['Task_ID'] != 'Task_ID']
        
        # Lógica de Negócio: Filtrar tarefas com 'Status' == 'In Progress'
        # BASES: Boolean Indexing (Filtragem eficiente)
        pending_tasks: pd.DataFrame = df_clean[df_clean['Status'] == 'In Progress']
        delayed_tasks: pd.DataFrame = df_clean[df_clean['Status'] == 'Delayed']
        if not pending_tasks.empty:
            print(f"⚠️ Alerta: Existem {len(pending_tasks)} tarefas pendentes.")
            print(pending_tasks[['Task_Name', 'Status']])
        if not delayed_tasks.empty:
            print(f"❌ Alerta: Existem {len(delayed_tasks)} tarefas atrasadas.")
            print(delayed_tasks[['Task_Name', 'Status']])
        else:
            print("✅ Tudo em dia! Excelente gestão de PMO.")
        df_clean['Budget_Allocated'] = pd.to_numeric(df_clean['Budget_Allocated'], errors='coerce')
        df_clean['Actual_Spent'] = pd.to_numeric(df_clean['Actual_Spent'], errors='coerce')
        df_clean['Budget_Diff'] = df_clean['Budget_Allocated'] - df_clean['Actual_Spent']
        # Visualização: Diferença média de orçamento por status
        df_clean.groupby('Status')['Budget_Diff'].mean().plot(kind='bar', title='Diferença Média de Orçamento por Status')
        plt.xlabel('Status')
        plt.ylabel('Diferença de Orçamento')
        plt.show()
        over_budget_tasks: pd.DataFrame = df_clean[df_clean['Budget_Diff'] < 0]
        if not over_budget_tasks.empty:
            print(f"⚠️ Alerta: Existem {len(over_budget_tasks)} tarefas acima do orçamento.")
            print(over_budget_tasks[['Task_Name', 'Budget_Allocated', 'Actual_Spent', 'Budget_Diff']])

    except FileNotFoundError:
        print(f"❌ Erro: O ficheiro {file_path.name} não foi encontrado.")
    except Exception as e:
        print(f"⚠️ Erro inesperado: {e}")

if __name__ == "__main__":
    # Usando Pathlib para localizar o ficheiro de dados
    data_file = Path.cwd() / "data" / "project_status.csv"
    # Rodar a função de auditoria
    audit_project_health(data_file)
