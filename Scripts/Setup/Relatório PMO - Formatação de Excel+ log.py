import pandas as pd
import os
import datetime
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill
import logging
# 1. GOVERNANÇA (LOGGING)
def log(msg):
    with open("pmo_production.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")

def run_master_pipeline():
    file_in = 'dados_pmo_segunda.csv'
    file_out = 'Relatorio_Final_Sexta.xlsx'
    
    log("🚀 Iniciando log")
    print("🚀 Iniciando pipeline...")
    # 2. VALIDAÇÃO (BASIC CHECKS)
    if not os.path.exists(file_in):
        log("❌ ERRO: Ficheiro de entrada não encontrado.")
        print("❌ ERRO: Ficheiro de entrada não encontrado.")
        print(os.path.abspath(file_in))
        return

    try:
        # 3. LIMPEZA (PANDAS)
        df = pd.read_csv(file_in)
        df['Tempo_Gasto'] = pd.to_numeric(df['Tempo_Gasto'].astype(str).str.replace('h', ''), errors='coerce')
        resumo = df.groupby('Projeto')['Tempo_Gasto'].sum().reset_index()
        resumo.to_excel(file_out, index=False)
        log(f"Dados limpos e agregados. Projetos processados: {len(resumo)}")
        print("log: Dados limpos e agregados. Projetos processados: ", len(resumo))

        # 4. FORMATAÇÃO (OPENPYXL)
        wb = load_workbook(file_out)
        ws = wb.active
        azul_header = PatternFill(start_color="000080", end_color="000080", fill_type="solid")
        for cell in ws[1]:
            cell.fill = azul_header
            cell.font = Font(color="FFFFFF", bold=True)
        
        wb.save(file_out)
        log("✨ Formatação visual concluída com sucesso.")
        print("🎉 Pipeline executado! Relatório pronto.")

    except Exception as e:
        log(f"💥 FALHA NO SISTEMA: {str(e)}")
run_master_pipeline()