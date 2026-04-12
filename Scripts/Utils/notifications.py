# notifications.py
# Notification utilities for email and alerts

import smtplib
import logging
from email.message import EmailMessage
from config import EMAIL_USER, EMAIL_PASSWORD, ARQUIVO_EXCEL_FORMATADO

def enviar_email(alertas):
    """
    Send an email notification with the list of new risks detected in the PMO report.

    This function creates an email message containing a summary of the detected risks,
    attaches the formatted Excel report, and sends it to the configured email address.

    Args:
        alertas (list[dict]): A list of dictionaries, each containing information about
            a detected risk. Each dictionary should have at least a 'tarefa' key with
            the task name.

    Raises:
        smtplib.SMTPException: If there's an error connecting to or sending via the SMTP server.
        FileNotFoundError: If the formatted Excel file cannot be found.
        Exception: For other unexpected errors during email sending.

    Example:
        >>> alertas = [{"tarefa": "Task 1"}, {"tarefa": "Task 2"}]
        >>> enviar_email(alertas)
        # Sends email with summary of Task 1 and Task 2
    """
    msg = EmailMessage()
    msg['Subject'] = f"Relatório de Riscos - {len(alertas)} itens"
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER
    conteudo = "Olá,\n\nSegue o resumo dos riscos detectados no relatório PMO.\n\n Atenciosamente,\n Agente de Riscos PMO,\n\nResumo de Riscos\n\n"
    for a in alertas:
        conteudo += f"Tarefa: {a['tarefa']}\n"
    msg.set_content(conteudo)

    with open(ARQUIVO_EXCEL_FORMATADO, 'rb') as f:
        file_data = f.read()
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
    msg = EmailMessage()
    msg['Subject'] = f"Relatório de Riscos - {len(alertas)} itens"
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER
    conteudo = "Olá,\n\nSegue o resumo dos riscos detectados no relatório PMO.\n\n Atenciosamente,\n Agente de Riscos PMO,\n\nResumo de Riscos\n\n"
    for a in alertas:
        conteudo += f"Tarefa: {a['tarefa']}\n"
    msg.set_content(conteudo)

    with open(ARQUIVO_EXCEL_FORMATADO, 'rb') as f:
        file_data = f.read()
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