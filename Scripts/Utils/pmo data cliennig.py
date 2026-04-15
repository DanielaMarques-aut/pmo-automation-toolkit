
"""PMO Data Cleaning and Aggregation Pipeline

Processes PMO project time-tracking CSV files to:
1. Validate and clean raw time data (removing 'h' suffix, converting to numeric)
2. Aggregate time spent per project
3. Generate audit-ready reports

Includes health checks, logging, and error handling for data quality assurance.
Essential for preparing time-tracking data for PMO analysis and decision-making.
"""

import os
import pandas as pd
import sys
import warnings
import glob
import logging
from datetime import datetime
from typing import Optional, List

# File configuration
FILE_NAME: str = 'dados_pmo_segunda.csv'

# Configure logging to both file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=f"{FILE_NAME.replace('.csv', '.log')}",
    filemode='w'
)


def log_event(message: str) -> None:
    """
    Write timestamped event message to log file.

    Appends a timestamped message to the PMO data log file for audit trail purposes.
    Includes both file logging and console output for monitoring.

    Args:
        message: Event description to log (e.g., "ERROR: File not found").
                 Include context about what triggered the event.

    Returns:
        None: Writes to file with side effect.

    Note:
        - Uses UTC-style ISO format for timestamps: YYYY-MM-DD HH:MM:SS
        - Appends to existing log file (does not overwrite)
        - Ensures UTF-8 encoding for international characters
    """
    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FILE_NAME.replace('.csv', '.log'), "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")


def run_health_check() -> None:
    """
    Validate all PMO CSV files in current directory for integrity.

    Scans for all CSV files matching pattern 'pmo_*.csv' and checks:
    - File readability
    - DataFrame is not empty
    - Reports corrupted or problematic files

    Returns:
        None: Prints health status for each file found.

    Output:
        Console output showing:
        - ✅ OK: File is valid with row count
        - ⚠️ EMPTY: File exists but has no data rows
        - ❌ CORRUPT: File exists but cannot be read (logs error)

    Example:
        >>> run_health_check()
        File: pmo_second.csv | Status: ✅ OK | Rows: 145
        File: pmo_corrupt.csv | Status: ❌ CORRUPT: ParserError
    """
    files: List[str] = glob.glob("*pmo_*.csv")
    for f in files:
        try:
            df: pd.DataFrame = pd.read_csv(f)
            status: str = "✅ OK" if not df.empty else "⚠️ EMPTY"
            print(f"File: {f} | Status: {status} | Rows: {len(df)}")
        except Exception as e:
            print(f"File: {f} | ❌ CORRUPT: {e}")
            log_event(f"ERROR: Corrupted file: {f} - {str(e)}")


def processar_dados(file_name: str) -> Optional[pd.DataFrame]:
    """
    Complete pipeline: Load → Validate → Clean → Aggregate → Export.

    Main function processing PMO time-tracking data:
    1. Runs health checks on all PMO files
    2. Loads specified CSV file
    3. Cleans time data (removes 'h' suffix, converts to numeric)
    4. Drops rows with invalid time values
    5. Aggregates time by project
    6. Exports aggregated report

    Args:
        file_name: Name of CSV file to process. Should match pattern 'dados_pmo_*.csv'.
                   File must contain columns: 'projeto' and 'tempo_gasto'.

    Returns:
        Optional[pd.DataFrame]: Aggregated report if successful (project | total_tempo_gasto),
                               None if file missing, empty, or processing fails.

    Processing Steps:
        1. Health Check: Validates all PMO files in directory
        2. Load: Reads CSV with pandas
        3. Validate: Checks for empty file
        4. Clean: Removes 'h' suffix from time values, converts to numeric
        5. Aggregate: Groups by project, sums tempo_gasto, sorts ascending
        6. Export: Saves to 'relatorio_final.csv'

    Output Files:
        - relatorio_final.csv: Contains project name and total hours (ascending order)
        - dados_pmo_segunda.log: Contains execution log with timestamps

    Note:
        - Logs all events (success/error) to both console and log file
        - Handles missing files gracefully
        - Drops rows where tempo_gasto cannot be converted to numeric
        - Outputs summary table to console before export

    Example:
        >>> result = processar_dados('dados_pmo_segunda.csv')
        >>> if result is not None:
        ...     print(result)
    """
    run_health_check()
    print(f"Processando o arquivo: {file_name}")
    log_event("SYSTEM START: Commencing daily PMO data pull.")

    # Step 1: Validate file existence
    if not os.path.isfile(file_name):
        msg: str = f"Arquivo {file_name} não encontrado."
        print(f"❌ {msg}")
        log_event(f"ERROR: {msg}")
        return None

    # Step 2: Load CSV file
    try:
        df: pd.DataFrame = pd.read_csv(file_name)

        # Validate: Check if file is empty
        if df.empty:
            warning: str = "⚠️ AVISO: Ficheiro vazio detetado! O ficheiro contém cabeçalhos mas não tem dados."
            print(warning)
            log_event(warning)
            return None

        success: str = "Dados carregados com sucesso!"
        print(f"✅ {success}")
        log_event(success)

        # Step 3: Clean data - Remove 'h' suffix and convert to numeric
        df["tempo_gasto"] = pd.to_numeric(
            df["tempo_gasto"].astype(str).str.replace("h", "", case=False),
            errors='coerce'
        )

        # Step 4: Drop rows with invalid time values (NaN after conversion)
        df = df.dropna(subset=["tempo_gasto"])

        # Step 5: Aggregate time by project
        resumo: pd.DataFrame = df.groupby("projeto")["tempo_gasto"].sum().reset_index()
        resumo = resumo.sort_values(by="tempo_gasto", ascending=True)

        # Display report to console
        print("\n📊 RELATÓRIO DE HORAS POR PROJETO:")
        print(resumo)
        log_event("SUCCESS: Report generated successfully.")

        # Step 6: Export aggregated report
        resumo.to_csv('relatorio_final.csv', index=False)
        print("\n✅ Relatório exportado como 'relatorio_final.csv'")
        log_event("SUCCESS: Report exported as 'relatorio_final.csv'")

        return resumo

    except Exception as e:
        error_msg: str = f"Erro ao ler o arquivo: {e}"
        print(f"❌ {error_msg}")
        log_event(f"ERROR: {error_msg}")
        return None


if __name__ == "__main__":
    """Execute data processing when script is run directly."""
    processar_dados(file_name=FILE_NAME)
