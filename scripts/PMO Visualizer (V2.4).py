#PMO Vizualizer - Pipeline de Engenharia de Dados para Qualidade de Dados
# Este script simula um pipeline de engenharia de dados para validar e limpar dados de tarefas reportadas, 
# atribuindo status de qualidade e destacando casos que requerem intervenção da equipa de operações (Ops).
# O objetivo é garantir que os dados sejam consistentes, confiáveis e prontos para análise, 
# enquanto automatizamos a triagem de casos problemáticos.
import pandas as pd
import numpy as np

def run_data_engineering_pipeline():
    print("🚀 Iniciar Pipeline de Engenharia de Dados...")

    # 1. SIMULAÇÃO DO DESAFIO TÉCNICO
    # Dados reais costumam vir com 'h', 'hrs' ou vazios (NaN)
    data = {
        'ID_Tarefa': [101, 102, 103, 104, 105],
        'Horas_Reportadas': ['8h', '10', 'vazio', '12h', np.nan],
        'Progresso_Estimado': [100, 110, 50, '90%', 0]
    }
    
    df = pd.DataFrame(data)
    print("\n--- Dados Originais (Com Inconsistências) ---")
    print(df)

    # 2. SOLUÇÃO DE ENGENHARIA: Normalização com to_numeric
    # Removemos caracteres não numéricos (como 'h' ou '%') antes da conversão
    df['Horas_Limpas'] = df['Horas_Reportadas'].astype(str).str.replace(r'[^0-9.]', '', regex=True)
    
    # errors='coerce' transforma o que não for número em NaN (Single Source of Truth)
    df['Horas_Limpas'] = pd.to_numeric(df['Horas_Limpas'], errors='coerce')
    
    # Repetimos para o Progresso
    df['Progresso_Limpo'] = pd.to_numeric(df['Progresso_Estimado'].astype(str).str.replace('%', ''), errors='coerce')

    # 3. LÓGICA DE NEGÓCIO: Sistema de Etiquetas (Status)
    def atribuir_status(row):
        if pd.isna(row['Horas_Limpas']) or pd.isna(row['Progresso_Limpo']):
            return '🔴 Erro de Input (NaN)'
        if row['Progresso_Limpo'] > 100:
            return '🟡 Discrepância (Prod > 100%)'
        if row['Horas_Limpas'] == 0:
            return '⚪ Sem Atividade'
        return '🟢 Validado'

    df['Status_QA'] = df.apply(atribuir_status, axis=1)

    # 4. EXPORTAÇÃO E TRIAGEM AUTOMÁTICA
    print("\n--- Relatório Final com Triagem Automática ---")
    print(df[['ID_Tarefa', 'Horas_Limpas', 'Progresso_Limpo', 'Status_QA']])
    
    # Isolamento para a equipa de Ops (quem precisa de intervir)
    intervencao_urgente = df[df['Status_QA'].str.contains('🔴|🟡')]
    
    if not intervencao_urgente.empty:
        print(f"\n⚠️ Alerta de Ops: {len(intervencao_urgente)} casos requerem a tua atenção imediata.")
        print(intervencao_urgente[['ID_Tarefa', 'Status_QA']])
run_data_engineering_pipeline()
