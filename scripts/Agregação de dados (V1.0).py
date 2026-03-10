# Agregação de dados de terça-feira - Versão 1.0
# Primeira versão do teste para agregar os dados de terça-feira.

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
