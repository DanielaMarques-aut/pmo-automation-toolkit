"""
Programming Base: 'Vectorization' - Instead of looping through rows, 
Pandas applies operations to entire columns at once (C-speed efficiency).
Title: Consolidated PMO Auditor & Budget Aggregator
Description: Combines Overdue detection with Budget aggregation by Manager.
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
from datetime import datetime

def run_consolidated_audit(csv_file):
     # CLEAN CODE: 'Input Validation'
    # We check if the file exists to prevent a 'Traceback' error for the user.
    try:
        # FAIL-FAST: Validate file existence
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"❌ Error: {csv_file} not found. Create a dummy CSV first!")
        return
    except Exception as e:
        print(f"❌ Error during processing: {e}")
    # SEMANTIC TYPE HINTING (Implicit)
        
    # PROGRAMMING BASE: 'Data Types'
    # In Excel, dates are often strings. In Python, we cast them to 'datetime' 
    # objects to perform math (e.g., Today - Deadline).
    df['Deadline'] = pd.to_datetime(df['Deadline'])
        
        # 1. OVERDUE ANALYSIS (Vectorization)
        
    # CLEAN CODE: 'Meaningful Names'
    # Instead of 'mask', we use 'overdue_df' so any dev understands the intent immediately. we also filter the DataFrame to only include rows where 'Task_ID' is not the header string, ensuring we analyze only real data.
    today = datetime.now()
    overdue_df = df[(df['Deadline'] < today) & (df['Status'] != 'Completed')]
        
        # 2. BUDGET AGGREGATION (New Concept: GroupBy)
        # Programming Base: Data Reduction. 
        # We transform raw data into high-level business insights.
    budget_by_manager = df.groupby('Manager')['Budget'].sum().reset_index()
        
        # 3. REPORTING
    print("="*40)
    print(f"📊 PMO EXECUTIVE REPORT - {today.strftime('%d/%m/%Y')}")
    print("="*40)
    print(f"Total Projects: {len(df)}")    
    print(f"\n⚠️ CRITICAL OVERDUE PROJECTS: {len(overdue_df)}")
    if not overdue_df.empty:
        print(overdue_df[['ProjectName', 'Deadline', 'Budget']])
            
        print("\n💰 BUDGET ALLOCATION BY MANAGER:")
        print(budget_by_manager.to_string(index=False))
        
        print("="*40)
        print("✅ Audit completed.")


if __name__ == "__main__":
    # Usando Pathlib para localizar o ficheiro de dados
    data_file = Path.cwd() / "data" / "projects.csv"
    # Rodar a função de auditoria
    run_consolidated_audit(data_file)