# Relatório PMO - Formatação de Excel
#Learning Python with a fun project: Formatting an Excel report for PMO! 
# This script reads a CSV file, converts it to Excel, and applies some styling to make it look professional.
# The goal is to automate the generation of a visually appealing report that can be easily shared with stakeholders.
# included colors based on status, bold headers, and a clean layout to enhance readability.
#sent email with the formatted report as an attachment to ensure that the PMO team receives the latest insights without any manual effort.
# the email encludes only the new risks detected in the report, making it easier for the team to focus on what matters most.
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

def aplicar_cores_status(file_path):
    wb = load_workbook(file_path)
    ws = wb.active
    
    # Cores (HEX Codes)
    verde = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    vermelho = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

    # Assumindo que a coluna C (3) tem o Status
    for row in range(2, ws.max_row + 1):
        status = ws.cell(row=row, column=3).value
        if status == "Concluido":
            ws.cell(row=row, column=3).fill = verde
        elif status == "Atrasado":
            ws.cell(row=row, column=3).fill = vermelho

    wb.save("Report_Quinta.xlsx")
    print("🎨 Cores aplicadas com base no Status!")


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
aplicar_cores_status('Relatorio_Formatado_PMO.xlsx')
import openpyxl
import json
import os
import smtplib
from email.message import EmailMessage

# --- CONFIGURAÇÕES ---
ARQUIVO_EXCEL = "Report_Quinta.xlsx"
ARQUIVO_MEMORIA = "alertas_enviados.json"
COR_ALVO = "FFC7CE" # O seu vermelho claro

from dotenv import load_dotenv
# Configurações de E-mail 
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_ADDRESS")  # Defina a variável de ambiente EMAIL_USER com seu email
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Defina a variável de ambiente EMAIL_PASSWORD com sua senha

if EMAIL_USER is None or EMAIL_PASSWORD is None:
    print("❌ ERRO CRÍTICO: O Python não encontrou o arquivo .env ou as variáveis!")
    print(f"DEBUG: EMAIL_ADDRESS encontrado? {'Sim' if EMAIL_USER else 'Não'}")
    print(f"DEBUG: EMAIL_PASSWORD encontrado? {'Sim' if EMAIL_PASSWORD else 'Não'}")
    # Encerra o script para não dar erro de 'NoneType'
    exit()


# --- FUNÇÕES DE APOIO ---
def carregar_memoria():
    if os.path.exists(ARQUIVO_MEMORIA):
        with open(ARQUIVO_MEMORIA, 'r') as f: return json.load(f)
    return {}

def salvar_memoria(memoria):
    with open(ARQUIVO_MEMORIA, 'w') as f: json.dump(memoria, f, indent=4)

# --- LOGICA PRINCIPAL DO AGENTE ---
def rodar_agente():
    wb = openpyxl.load_workbook(ARQUIVO_EXCEL, data_only=True)
    ws = wb.active
    memoria = carregar_memoria()
    novos_alertas = []

    for row in range(2, ws.max_row + 1):
        nome = ws.cell(row=row, column=1).value
        cor = ws.cell(row=row, column=3).fill.start_color.rgb[2:] # Pega o RGB sem o prefixo 'FF'
        print (f"🔍 Verificando tarefa: {nome} - Cor: {cor}")
        if cor == COR_ALVO and nome not in memoria:
            print(f"🔎 Novo risco detectado: {nome}")
            novos_alertas.append({"tarefa": nome})
            memoria[nome] = "NOTIFICADO"

    if novos_alertas:
        salvar_memoria(memoria)
        print(f"📢 {len(novos_alertas)} novos riscos encontrados. A guardar... ")
        enviar_email(novos_alertas)
        
print("✅ Agente de Riscos PMO executado com sucesso!")
def enviar_email(alertas):
    msg = EmailMessage()
    msg['Subject'] = f"🚨 Relatório de Riscos - {len(alertas)} itens"
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER
    
    conteudo = "Resumo de Riscos\n\n"
    for a in alertas:
        conteudo += f"Tarefa: {a['tarefa']}\n"
    
    msg.set_content(conteudo)
    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(EMAIL_USER, EMAIL_PASSWORD)
        s.send_message(msg)
        print("📧 Email de alerta enviado com sucesso!")

carregar_memoria()
salvar_memoria({})
rodar_agente()
enviar_email([{"tarefa": "Exemplo de Tarefa com Risco"}])
