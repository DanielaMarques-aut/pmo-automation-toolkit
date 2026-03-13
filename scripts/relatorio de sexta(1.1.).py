import pandas as pd
import smtplib
import logging
import os
from pathlib import Path
from email.message import EmailMessage
from dotenv import load_dotenv

# 1. SETUP & CONFIGURATION
load_dotenv() # Loads your email/password from the .env file
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "Output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True) # Automatically creates the folder

# Configure Logging to save errors to a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        # Adding 'encoding="utf-8"' here fixes the UnicodeEncodeError
        logging.FileHandler(BASE_DIR / "pmo_pipeline.log", encoding="utf-8"),
        logging.StreamHandler() 
    ]
)
def validate_data(df):
    """Checks if the data is fit for processing."""
    required_cols = ['Dept', 'Hours']
    if df.empty:
        raise ValueError("The source data is empty.")
    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"Missing required column: {col}")

def run_weekly_closeout():
    try:
        logging.info("🎯 Starting Friday Close-out...")

        # 1. LOAD & CLEAN
        # (In a real scenario, you'd use pd.read_excel or pd.read_csv)
        data = {'Dept': ['TI', 'HR', 'Ops'], 'Hours': ['40h', '35', '50h']}
        df = pd.DataFrame(data)
        
        validate_data(df) # Stop early if data is bad

        df['Hours_Clean'] = pd.to_numeric(
            df['Hours'].astype(str).str.replace('h', '', case=False), 
            errors='coerce'
        ).fillna(0)

        # 2. AGGREGATE
        summary = df.groupby('Dept')['Hours_Clean'].sum().reset_index()
        total_hours = summary['Hours_Clean'].sum()
        
        # 3. GENERATE REPORT
        report_text = (
            f"Weekly PMO Report\n"
            f"{'='*20}\n"
            f"{summary.to_string(index=False)}\n"
            f"{'='*20}\n"
            f"Total Hours: {total_hours}"
        )

        file_path = OUTPUT_DIR / "PMO_Report.xlsx"
        summary.to_excel(file_path, index=False)
        
        logging.info(f"✅ Report saved to {file_path}")
        return report_text, file_path.name

    except Exception as e:
        logging.error(f"❌ Failed during data processing: {e}")
        raise # Re-raise to stop the script from sending a broken email

def send_pmo_email(subject, body, filename):
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        logging.error("❌ Email credentials not found in .env file!")
        return

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content(body)

    file_path = OUTPUT_DIR / filename

    # Attach file with robust check
    if not file_path.exists():
        logging.error(f"❌ Attachment not found: {file_path}")
        return

    try:
        with open(file_path, 'rb') as f:
            msg.add_attachment(
                f.read(),
                maintype='application',
                subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                filename=filename
            )

        logging.info("📧 Connecting to mail server...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            logging.info("🚀 Email sent successfully!")

    except Exception as e:
        logging.error(f"❌ Critical failure in email dispatch: {e}")

# --- EXECUTION ---
if __name__ == "__main__":
    try:
        report_content, file_name = run_weekly_closeout()
        send_pmo_email(
            subject="Relatório Diário de Operações - PMO", 
            body=report_content, 
            filename=file_name
        )
    except Exception as main_err:
        logging.critical(f"Pipeline crashed: {main_err}")