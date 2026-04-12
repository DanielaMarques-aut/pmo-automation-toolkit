import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from typing import Dict, List, Any

def audit_project_health(file_path: Path):
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
