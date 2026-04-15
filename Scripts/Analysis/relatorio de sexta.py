"""
Friday Weekly Close-out Report Generator Module.

This module automates the end-of-week reporting cycle: data aggregation,
summary report generation, and email distribution. It combines data cleaning
(Monday's logic), aggregation (Tuesday's logic), and email integration for
Friday stakeholder communication.

Primary Purpose:
    Generate weekly PMO reports summarizing departmental hours worked and
    export to Excel for email distribution. Automates routine Friday reporting
    to ensure consistent, timely stakeholder updates.

Key Concepts:
    - Pipeline Orchestration: Combine Monday→Tuesday→Friday logic
    - Data Flow: Load → Clean → Aggregate → Format → Email
    - Reusable Patterns: Hour cleaning (strip 'h' suffix, numeric coercion)
    - Email Integration: Automatic Excel attachment handling
    - Error Recovery: Graceful handling of missing credentials/files

Workflow:
    1. DATA SETUP: Create department hours DataFrame (simulated or real)
    2. CLEAN: Remove 'h' suffix, convert to numeric via pd.to_numeric()
    3. AGGREGATE: Group by Dept, sum hours across all entries
    4. SUMMARIZE: Calculate total hours and format report text
    5. EXPORT: Save summary to Excel (PMO_Report.xlsx)
    6. EMAIL: Send report with Excel attachment to stakeholders

Component Functions:
    - run_weekly_closeout(): Orchestrates entire data processing pipeline
    - enviar_alerta_pmo(): Email dispatch with Excel file attachment

Email Attachment Pattern:
    - Binary read mode ('rb') for Excel files
    - MIME type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
    - Adds attachment to EmailMessage object

Dependencies:
    - pandas: DataFrame operations, groupby, Excel export
    - smtplib: Gmail SMTP connection via SMTP_SSL
    - email.message: EmailMessage for structured email construction
    - os: File path operations

Author: PMO Reporting Team | Date: 2026-04-15
Schedule: Runs every Friday 17:00 for stakeholder distribution

"""

import pandas as pd
import smtplib
from email.message import EmailMessage
import os
from typing import Optional, Dict, Any, List

def run_weekly_closeout() -> Optional[str]:
        print("🎯 Starting Friday Close-out...")

    # 1. LOAD & CLEAN (Monday's Logic)
    # Replace with your actual file path
        data = {'Dept': ['TI', 'HR', 'Ops'], 'Hours': ['40h', '35', '50h']}
        df = pd.DataFrame(data)
        df['Hours_Clean'] = pd.to_numeric(df['Hours'].astype(str).str.replace('h', ''), errors='coerce')

    # 2. AGGREGATE (Tuesday's Logic)
        summary = df.groupby('Dept')['Hours_Clean'].sum().reset_index()
    
    # 3. GENERATE INSIGHT (Thursday's Logic)
        total_hours = summary['Hours_Clean'].sum()
        report_text = f"Weekly PMO Report:\n\n{summary.to_string()}\n\nTotal Hours: {total_hours}"
        print(report_text)
        df_summary = pd.DataFrame(summary)
        df_summary.to_excel(rf"C:\Users\daniq\carrer\Output\PMO_Report.xlsx", index=False)
        
        print("✅ Report Ready for Distribution!")
        return report_text
def enviar_alerta_pmo(assunto, corpo, nome_ficheiro): 
   
    # 4. AUTO-EMAIL
    EMAIL_ADDRESS = ""
    EMAIL_PASSWORD = ""
    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS # Envia para ti mesma como log
    msg.set_content(corpo)
    print("📧 Preparando para enviar alerta por email...")
    pathname = rf"C:\Users\daniq\carrer\Output\{nome_ficheiro}"
    try:
        with open(pathname, 'rb') as f:
            file_data = f.read()
            msg.add_attachment(
                file_data, 
                maintype='application', 
                subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                filename=nome_ficheiro
            )
    except FileNotFoundError:
        print(f"❌ Erro: O ficheiro {pathname} não foi encontrado!")
        return
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)   
                smtp.send_message(msg)
                print("🚀 Alerta enviado com sucesso!")
    except Exception as e:
        print(f"❌ Falha ao enviar alerta: {e}")
        print(f"❌ Falha no envio: {e}")
texto_do_relatorio = run_weekly_closeout()
    
    # 2. Pass that text into the email function
enviar_alerta_pmo("Relatório Diário de Operações - PMO", texto_do_relatorio, "PMO_Report.xlsx")
