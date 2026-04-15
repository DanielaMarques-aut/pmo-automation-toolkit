"""Email Notification Utilities for PMO Alerts

Provides functions for sending email notifications containing risk summaries and
formatted Excel reports. Integrates with Gmail SMTP server via credentials stored
in environment variables.
"""

import smtplib
import logging
from typing import List, Dict
from email.message import EmailMessage
from config import EMAIL_USER, EMAIL_PASSWORD, ARQUIVO_EXCEL_FORMATADO

def enviar_email(alertas: List[Dict[str, str]]) -> None:
    """
    Send email notification with detected risks and formatted Excel report.

    Creates and sends an email message containing a summary of detected risks from
    the PMO report. Automatically attaches the formatted Excel file for reference.
    
    Email Details:
        - Subject: "Relatório de Riscos - {count} itens"
        - Body: Greeting + Summary of each risk task + Professional closing
        - Attachment: Formatted Excel report (ARQUIVO_EXCEL_FORMATADO)
        - Recipient: EMAIL_USER (environment variable)

    Args:
        alertas: List of alert dictionaries, each containing at minimum a 'tarefa' key
                with the task/alert name. Example format:
                [{'tarefa': 'Task 1', 'severity': 'High'}, {'tarefa': 'Task 2'}]

    Returns:
        None: Sends email as side effect. Logs success or failure.

    Raises:
        smtplib.SMTPException: If unable to connect or authenticate with SMTP server.
        FileNotFoundError: If the formatted Excel file (ARQUIVO_EXCEL_FORMATADO) 
                          does not exist.
        KeyError: If alert dictionary is missing required 'tarefa' key.
        TypeError: If alertas is not a list or not iterable.

    Note:
        - Requires EMAIL_USER and EMAIL_PASSWORD set in environment variables
        - Uses Gmail SMTP server (smtp.gmail.com:587)
        - Enables TLS encryption for the connection
        - Logs error if email send fails but does not raise exception

    Example:
        >>> alerts = [
        ...     {'tarefa': 'Fix Database Connection'},
        ...     {'tarefa': 'Update Security Patches'}
        ... ]
        >>> enviar_email(alerts)
        # Sends email to EMAIL_USER with 2 items and Excel attachment
    """
    msg = EmailMessage()
    msg['Subject'] = f"Relatório de Riscos - {len(alertas)} itens"
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER
    conteudo: str = "Olá,\n\nSegue o resumo dos riscos detectados no relatório PMO.\n\n Atenciosamente,\n Agente de Riscos PMO,\n\nResumo de Riscos\n\n"
    for a in alertas:
        conteudo += f"Tarefa: {a['tarefa']}\n"
    msg.set_content(conteudo)

    with open(ARQUIVO_EXCEL_FORMATADO, 'rb') as f:
        file_data: bytes = f.read()
        msg.add_attachment(
            file_data,
            maintype='application',
            subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            filename=ARQUIVO_EXCEL_FORMATADO
        )

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        try:
            s.starttls()
            s.login(EMAIL_USER, EMAIL_PASSWORD)
            s.send_message(msg)
            logging.info("📧 Email de alerta enviado com sucesso!")
        except Exception as e:
            logging.error(f"FALHA AO ENVIAR EMAIL: {str(e)}")