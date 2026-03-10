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
run_analysis()
