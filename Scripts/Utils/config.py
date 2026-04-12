# config.py
# Configuration constants for the PMO report script

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Colors (HEX Codes)
verde = "C6EFCE"
vermelho = "FFC7CE"
amarelo = "FFEB9C"
azul_escuro = "000080"

# Color fills
from openpyxl.styles import Font, PatternFill
VERDE_FILL = PatternFill(start_color=verde, end_color=verde, fill_type="solid")
VERMELHO_FILL = PatternFill(start_color=vermelho, end_color=vermelho, fill_type="solid")
AMARELO_FILL = PatternFill(start_color=amarelo, end_color=amarelo, fill_type="solid")
AZUL_ESCURO_FILL = PatternFill(start_color=azul_escuro, end_color=azul_escuro, fill_type="solid")

# Fonts
FONTE_BRANCA = Font(color="FFFFFF", bold=True)

# File paths
ARQUIVO_EXCEL_ENTRADA = "Report_Quinta.xlsx"
ARQUIVO_MEMORIA = Path("alertas_enviados.json")
ARQUIVO_CSV = "dados_pmo_segunda.csv"
ARQUIVO_EXCEL_FORMATADO = 'Relatorio_Formatado_PMO.xlsx'

# Email settings
EMAIL_USER = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Risk color target (red without FF prefix)
COR_ALVO = vermelho