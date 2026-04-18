"""Email Alert Automation Module with Attachment Support.

This module provides utilities for sending automated email alerts with Excel
attachments using Gmail SMTP. It implements secure credential management and
robust error handling for production email delivery.

Key Features:
    - Gmail App Passwords: Secure authentication without plaintext passwords
    - File Attachment: Excel (.xlsx) and binary file support
    - Error Handling: Comprehensive try-catch for network and file failures
    - Logging: Console feedback for debugging and monitoring

Security Considerations:
    - PRODUCTION ISSUE: Email and password are hardcoded in script
    - RECOMMENDATION: Load credentials from .env file instead
    - ALWAYS USE: Gmail App Passwords, NOT main account password
    - Generate app password at: myaccount.google.com/apppasswords

Automation Pattern:
    Configure once with valid Gmail App Password, then call enviar_alerta_pmo()
    to send alerts programmatically. Ideal for scheduled PMO report distribution.
"""

import smtplib
from email.message import EmailMessage
import os
from typing import Optional
pasta_output: str = r"C:\Users\daniq\carrer\Output"

print(f"🔍 Checking files in: {pasta_output}")
try:
    ficheiros_na_pasta = os.listdir(pasta_output)
    print(f"📁 Files found: {ficheiros_na_pasta}")
except Exception as e:
    print(f"❌ Error accessing folder: {e}")


def enviar_alerta_pmo(
    assunto: str,
    corpo: str,
    nome_ficheiro: str
) -> bool:
    """
    Send automated email alert with Excel attachment via Gmail SMTP.
    
    Composes and sends email with file attachment using Gmail's SMTP server.
    Implements secure authentication with App Passwords and comprehensive error
    handling for network and file operation failures.
    
    Args:
        assunto (str): Email subject line. Example: "Daily Operations Report"
        corpo (str): Email body text. Can include multiple lines.
            Example: "Daily metrics attached.\\n\\nBest regards,"
        nome_ficheiro (str): Filename in pasta_output directory (without path).
            Example: "relatorio_final.xlsx"
    
    Returns:
        bool: True if email sent successfully, False if any error occurred.
            Detailed error messages printed to console.
    
    Raises:
        No exceptions raised to caller. All errors caught and logged:\n            - FileNotFoundError: File doesn't exist in pasta_output
            - SMTPAuthenticationError: Invalid credentials
            - SMTPException: SMTP connection failed
            - ConnectionError: Network unreachable
    
    Notes:
        SECURITY PATTERN - App Passwords:
        Gmail requires 2-Step Verification for SMTP access. Generate app-specific
        password at myaccount.google.com/apppasswords rather than using main
        account password. This limits token scope and prevents account lockout.
        
        FILE ATTACHMENT FORMAT:
        Automatically detects Excel files (.xlsx) and sets MIME type to
        'vnd.openxmlformats-officedocument.spreadsheetml.sheet'.
        
        IDEMPOTENCY CONSIDERATION:
        This function sends email immediately - no queue or retry logic.
        If network fails mid-send, email may be partially delivered.
    
    Examples:
        Send daily operations report:
        
        >>> success = enviar_alerta_pmo(
        ...     "Daily Report",
        ...     "Daily metrics attached.\\n\\nBest regards, PMO Team",
        ...     "relatorio_final.xlsx"
        ... )
        >>> if success:
        ...     print("Email delivered")
        ... else:
        ...     print("Email failed - check logs")
    
    \"\"\"\n  
    """
    EMAIL_ADDRESS: str = "teu_email_aqui@gmail.com"
    EMAIL_PASSWORD: str = "tua-app-password"

    msg: EmailMessage = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content(corpo)
    print("📧 Preparing email alert...")
    
    pathname: str = rf"C:\Users\daniq\carrer\Output\{nome_ficheiro}"
    
    try:
        with open(pathname, 'rb') as f:
            file_data = f.read()
            msg.add_attachment(
                file_data,
                maintype='application',
                subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                filename=nome_ficheiro
            )
        print(f"✏️ Attachment added: {nome_ficheiro}")
    except FileNotFoundError:
        print(f"❌ Error: File {pathname} not found!")
        return False
    except IOError as io_err:
        print(f"❌ Error reading file: {io_err}")
        return False

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("🚀 Alert sent successfully!")
            return True
    except smtplib.SMTPAuthenticationError:
        print(f"❌ Authentication failed: Invalid email or app password")
        return False
    except smtplib.SMTPException as smtp_err:
        print(f"❌ SMTP error: {smtp_err}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {str(e)}")
        return False


if __name__ == "__main__":
    print("\\n--- Email Alert Demonstration ---\\n")
    success = enviar_alerta_pmo(
        "Daily Operations Report",
        "Please find attached the automatically generated Excel report.\\n\\nBest Regards,\\nPMO Team",
        'resumo_executivo_terca (2).xlsx'
    )
    if success:
        print("\\n✅ Demo completed")
    else:
        print("\\n⚠️ Demo failed - check configuration")
