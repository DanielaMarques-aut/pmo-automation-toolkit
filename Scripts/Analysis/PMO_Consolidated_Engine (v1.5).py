"""
Title: PMO Consolidated Engine (v1.5)
Author: Daniela Marques
Description: Automated risk auditor integrating Pandas and Gemini AI.
Clean Code: 'Separation of Concerns' - Logic (Pandas) is separate from AI (Gemini).
Programming Base: 'Context Injection' - Sending structured summaries instead of raw data.
Modularization. If your code grows to include multiple systems (e.g., a "Risk_Module" and a "Data_Ingestion_Module"), 
having named loggers helps you identify exactly which part of the engine generated a specific message.
Benefit: Instead of messy prints, we have a history of what the AI did.
"""
import logging
from datetime import datetime
from pathlib import Path
import os
import time
import pandas as pd
import google.genai as genai
from dotenv import load_dotenv
from google.api_core import exceptions
from typing import Dict, Any, Optional ,List

log_dir = "logs"
# Cria pasta de logs se não existir
if not os.path.exists(log_dir):
        os.makedirs(log_dir)
logging.basicConfig(level= logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
        # Add encoding='utf-8' here to handle the emojis
        logging.FileHandler(os.path.join(log_dir, "pmo_audit.log"), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
log=logging.getLogger("PMO_Engine")
start_time: float = time.time()
# --- PROGRAMMING BASES: ENVIRONMENT ISOLATION ---
# Carregamos as chaves do .env para garantir 0% de exposição no GitHub.
load_dotenv()
api_key: str = os.getenv("GOOGLE_API_KEY")

if not api_key:
    log.error("❌ Error: GOOGLE_API_KEY not found in .env file.")
    exit(1)

# Configuração do Cliente Gemini
client: genai.Client = genai.Client(api_key=api_key)
model: str = "gemini-flash-latest"

def get_ai_insight(summary_text: str, retries: int = 3):
    """
    CLEAN CODE PRINCIPLE: Resilience Pattern (Retry Logic)
    Esta função lida com o erro 503 (Server Busy) que encontrámos.
    """
    prompt = f"""
    Act as operations Director. Analyse this project summary and 
    provide a strategic recommendation in two sentences focused on budget risk and resource allocation:
    {summary_text}
    """
    
    for i in range(retries):
        try:
            response: genai.types.GenerateContentResponse = client.models.generate_content(model=model, contents=prompt)

            return response.text
        except exceptions.InternalServerError:
            wait = (i + 1) * 2
            log.warning(f"⚠️ Busy server (503). Re-trying in {wait}s...")
            time.sleep(wait)
        except Exception as e:
            log.error(f"Error in IA analysis: {e}")
    return "IA unavailable at the moment."

def main():
    # --- CLEAN CODE: FAIL-FAST INGESTION ---
    file_path: str = "Data/Raw/projects.csv"
    report_dir: str = "output"

    if not Path(file_path).exists() or not Path(file_path).is_file():
        log.error(f"❌ Error: The file {file_path} does not exist.")
        return
    if not Path(report_dir).exists():
        log.warning(f"⚠️ Warning: The directory {report_dir} does not exist.")
        Path(report_dir).mkdir(parents=True, exist_ok=True) 

    try:
        # --- PROGRAMMING BASES: VECTORIZATION (Pandas) ---
        # Processamos milhares de linhas sem usar loops 'for'.
        # A IA adora dados limpos e estruturados, então fazemos isso antes de enviar.
        df: pd.DataFrame = pd.read_csv(file_path)
        df['Deadline'] = pd.to_datetime(df['Deadline'])
        df['Budget']= pd.to_numeric(df['Budget'], errors='coerce').fillna(0)
        df['Department'] = df['Department'].str.strip() # Limpa espaços em branco
        
        # Agregação por Departamento (Lição de Quinta-feira)
        # O GroupBy reduz a complexidade para a IA ler melhor.
        dept_summary: Dict[str, float] = df.groupby('Department')['Budget'].sum().to_dict()
        
        # Auditoria de Atrasos
        today: pd.Timestamp = pd.to_datetime('today')
        overdue_count: int = df[(df['Deadline'] < today) & (df['Status'] != 'Completed')].shape[0]

        # --- AI INTEGRATION ---
        log.info("🤖 Generating AI insights...")
        summary_for_ai: str = f"Dept Summary: {dept_summary}. Overdue Projects: {overdue_count}."
        insight: str = get_ai_insight(summary_for_ai)
        timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M")
        report_filename: str = f"{report_dir}/audit_report_{timestamp}.txt"
        # --- OUTPUT DE ELITE (Business Ops Language) ---
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write("📊 Executive Report\n")
            f.write("="*50 + "\n")
            f.write(f"Insights from AI: {insight}\n")
            f.write("-" * 50 + "\n")
            f.write("Budget Distribution by Department:\n")
            for dept, budget in dept_summary.items():
                f.write(f"• {dept}: {budget}€\n")
            f.write("="*50 + "\n")
        log.info(f"✅ Report saved to {report_filename}")
        log.info("\n" + "="*50)
        log.info("📊 Executive Report")
        log.info("="*50)
        log.info(f"Insights from AI: {insight}")
        log.info("-" * 50)
        log.info("Budget Distribution by Department:")
        for dept, budget in dept_summary.items():
            log.info(f"• {dept}: {budget}€")
        log.info("="*50)
        log.info(f"✅ Audit completed in {time.time() - start_time:.1f}s.")


    except Exception as e:
        log.error(f"❌ Critical failure in processing: {e}")

if __name__ == "__main__":
    main()