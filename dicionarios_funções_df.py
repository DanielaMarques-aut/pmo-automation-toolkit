import pandas as pd
import datetime

# 1. DEFINIÇÃO DE FUNÇÕES (A nossa 'máquina' de decisão)
def definir_saude(financeiro):
    # Uma função é uma regra: "Se entrar X, sai Y"
    if financeiro < 0:
        return '🔴 OVER BUDGET'
    return '🟢 ON TRACK'

def executar_toolkit():
    print(f"--- 🚀 PMO TOOLKIT V1.5: FUNDAMENTOS ---")
    
    # 2. DICIONÁRIO (A nossa base de dados bruta)
    data = {
        'Projeto': ['Risk AI', 'Cloud Ops'],
        'Budget': [1000, 5000],
        'Gasto': [1200, 4000]
    }
    
    # 3. DATAFRAME (Organização em tabela)
    df = pd.DataFrame(data)
    
    # 4. CÁLCULOS (Transformação)
    df['Variancia'] = df['Budget'] - df['Gasto']
    
    # Aqui usamos a nossa função 'definir_saude' em cada linha
    df['Status'] = df['Variancia'].apply(definir_saude)
    
    print(df)
    print("\n[Conceitos dominados: Dicionários, Funções e DataFrames]")