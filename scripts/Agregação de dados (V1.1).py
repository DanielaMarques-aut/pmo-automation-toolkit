#Agregação de dados de terça-feira - Versão 1.1
# Primeira versão do teste para agregar os dados de terça-feira.
# O objetivo é criar um resumo executivo que possa ser apresentado na reunião de equipa, 
# destacando os principais indicadores e alertas.

import pandas as pd
import numpy as np

def run_analysis():
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
    plt.savefig("gasto_departamento.png")
run_analysis()
