# Relatório PMO - Formatação de Excel
#Learning Python with a fun project: Formatting an Excel report for PMO! 
# This script reads a CSV file, converts it to Excel, and applies some styling to make it look professional.
# The goal is to automate the generation of a visually appealing report that can be easily shared with stakeholders.



import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill

def formatar_excel_pmo(file_path):
    print(f"🎨 A formatar visualmente: {file_path}")
    
    # 1. Primeiro criamos o Excel com Pandas
    df = pd.read_csv('relatorio_final.csv')
    excel_file = 'Relatorio_Formatado_PMO.xlsx'
    df.to_excel(excel_file, index=False)

    # 2. Abrimos com Openpyxl para dar o "toque de mestre"
    wb = load_workbook(excel_file)
    ws = wb.active

    # 3. Estilizar o cabeçalho (Linha 1)
    azul_escuro = PatternFill(start_color="000080", end_color="000080", fill_type="solid")
    fonte_branca = Font(color="FFFFFF", bold=True)

    for cell in ws[1]: # Para cada célula na primeira linha
        cell.fill = azul_escuro
        cell.font = fonte_branca

    wb.save(excel_file)
    print(f"✨ Report Profissional gerado: {excel_file}")
formatar_excel_pmo('relatorio_final.csv')