"""Data Loading, Validation, and Processing Utilities

Provides functions for loading, validating, and processing PMO data from CSV files
and JSON memory stores. Includes memory persistence to avoid duplicate notifications
and data quality checks.
"""

import json
import logging
from typing import Optional, Dict
import pandas as pd
from pathlib import Path
from config import ARQUIVO_MEMORIA

def carregar_memoria() -> Dict[str, any]:
    """
    Load the memory dictionary from JSON file with previously notified alerts.

    Reads the alerts memory file to retrieve previously notified risks and avoid
    duplicate notifications. Returns an empty dictionary if the file doesn't exist.

    Returns:
        Dict[str, any]: Dictionary containing previously notified tasks as keys and 
                        their notification status as values. Empty dict if file missing.

    Raises:
        json.JSONDecodeError: If the JSON file is corrupted or invalid.
        IOError: If there's an issue reading the file.
    """
    if ARQUIVO_MEMORIA.exists():
        with open(ARQUIVO_MEMORIA, 'r') as f:
            return json.load(f)
    return {}

def salvar_memoria(memoria: Dict[str, any]) -> None:
    """
    Save the memory dictionary to JSON file for persistence.

    Persists the current state of notified risks to avoid duplicate notifications
    in future runs.

    Args:
        memoria: Dictionary containing task names as keys and their notification 
                 status as values.

    Returns:
        None: Writes data to disk with side effects.

    Raises:
        IOError: If there's an issue writing to the file.
        TypeError: If the memoria object is not JSON serializable.
    """
    with open(ARQUIVO_MEMORIA, 'w') as f:
        json.dump(memoria, f, indent=4)

def carregar_e_validar_dados(caminho: str) -> Optional[pd.DataFrame]:
    """
    Load and validate CSV data with automatic delimiter detection.

    Reads a CSV file, sanitizes column names (strips whitespace), and validates
    that required columns are present. Uses pandas with automatic delimiter detection.

    Args:
        caminho: Absolute or relative path to the CSV file to load.

    Returns:
        Optional[pd.DataFrame]: DataFrame with validated data if successful, 
                                None if loading or validation fails.

    Raises:
        FileNotFoundError: If the specified CSV file does not exist.
        pd.errors.EmptyDataError: If the CSV file is empty.
        UnicodeDecodeError: If there's an encoding issue with the file.
    """
    try:
        logging.info(f"🔍 A ler ficheiro: {caminho}")
        df: pd.DataFrame = pd.read_csv(caminho, sep=None, engine='python', encoding='utf-8-sig')
        # Sanitize column names
        df.columns = df.columns.str.strip()
        # Validate required columns
        colunas_obrigatorias: list[str] = ["Status", "Tarefa"]
        if not all(col in df.columns for col in colunas_obrigatorias):
            logging.error(f"❌ Erro de Schema: Colunas {colunas_obrigatorias} não encontradas.")
            return None
        return df
    except Exception as e:
        logging.error(f"💥 Falha ao carregar CSV: {e}")
        return None

def normalizar_status(df: pd.DataFrame) -> None:
    """
    Normalize status column and perform data quality checks on DataFrame.

    Standardizes status values by stripping whitespace and capitalizing, then checks
    for data inconsistencies and outliers that might indicate data quality issues.

    Args:
        df: DataFrame containing PMO data with 'Status' and 'Horas' columns.

    Returns:
        None: Modifies the input DataFrame in-place.

    Note:
        - Modifies df in-place without returning anything
        - Logs warnings/errors for detected issues
        - Checks for completed tasks with 0 or negative hours
        - Detects outliers (tasks with > 100 hours)
    """
    # Normalize status
    df['Status'] = df['Status'].str.strip().str.capitalize()
    # Check for inconsistencies
    inconsistentes: pd.DataFrame = df[(df['Status'] == 'Concluído') & (df['Horas'] <= 0)]
    if not inconsistentes.empty:
        logging.warning(f"⚠️ Alerta de QA: {len(inconsistentes)} tarefas concluídas com 0 horas.")
    
    # Detect outliers
    outliers = df[df['Horas'] > 100]
    if not outliers.empty:
        logging.error(f"🚨 Crítico: Detetadas horas excessivas (>100h) em {len(outliers)} linhas.")