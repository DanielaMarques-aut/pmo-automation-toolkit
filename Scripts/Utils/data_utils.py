# data_utils.py
# Data loading, validation, and processing utilities

import json
import logging
import pandas as pd
from pathlib import Path
from config import ARQUIVO_MEMORIA

def carregar_memoria():
    """
    Load the memory dictionary from the JSON file.

    This function reads the alerts memory file to retrieve previously notified risks.
    If the file doesn't exist, it returns an empty dictionary.

    Returns:
        dict: A dictionary containing previously notified tasks as keys and their status as values.
              Returns an empty dict if the file doesn't exist.

    Raises:
        json.JSONDecodeError: If the JSON file is corrupted or invalid.
        IOError: If there's an issue reading the file.
    """
    if ARQUIVO_MEMORIA.exists():
        with open(ARQUIVO_MEMORIA, 'r') as f:
            return json.load(f)
    return {}

def salvar_memoria(memoria):
    """
    Save the memory dictionary to the JSON file.

    This function persists the current state of notified risks to avoid duplicate notifications.

    Args:
        memoria (dict): A dictionary containing task names as keys and their notification status as values.

    Raises:
        IOError: If there's an issue writing to the file.
        TypeError: If the memoria object is not JSON serializable.
    """
    with open(ARQUIVO_MEMORIA, 'w') as f:
        json.dump(memoria, f, indent=4)

def carregar_e_validar_dados(caminho):
    """
    Load and validate CSV data from the specified file path.

    This function reads a CSV file, sanitizes column names, and validates that required
    columns are present. It uses pandas with automatic delimiter detection.

    Args:
        caminho (str): The file path to the CSV file to be loaded.

    Returns:
        pandas.DataFrame or None: The loaded and validated DataFrame if successful,
        None if loading or validation fails.

    Raises:
        FileNotFoundError: If the specified CSV file does not exist.
        pandas.errors.EmptyDataError: If the CSV file is empty.
        UnicodeDecodeError: If there's an encoding issue with the file.
    """
    try:
        logging.info(f"🔍 A ler ficheiro: {caminho}")
        df = pd.read_csv(caminho, sep=None, engine='python', encoding='utf-8-sig')
        # Sanitize column names
        df.columns = df.columns.str.strip()
        # Validate required columns
        colunas_obrigatorias = ["Status", "Tarefa"]
        if not all(col in df.columns for col in colunas_obrigatorias):
            logging.error(f"❌ Erro de Schema: Colunas {colunas_obrigatorias} não encontradas.")
            return None
        return df
    except Exception as e:
        logging.error(f"💥 Falha ao carregar CSV: {e}")
        return None

def normalizar_status(df):
    """
    Normalize the 'Status' column and perform data quality checks on the DataFrame.

    This function standardizes status values by stripping whitespace and capitalizing,
    then checks for data inconsistencies and outliers that might indicate data quality issues.

    Args:
        df (pandas.DataFrame): The DataFrame containing PMO data with 'Status' and 'Horas' columns.

    Note:
        This function modifies the input DataFrame in-place and logs warnings/errors
        for detected issues. It does not return anything.

    Warnings logged:
        - Tasks marked as 'Concluído' with 0 or negative hours
        - Tasks with more than 100 hours (potential outliers)
    """
    # Normalize status
    df['Status'] = df['Status'].str.strip().str.capitalize()
    # Check for inconsistencies
    inconsistentes = df[(df['Status'] == 'Concluído') & (df['Horas'] <= 0)]
    if not inconsistentes.empty:
        logging.warning(f"⚠️ Alerta de QA: {len(inconsistentes)} tarefas concluídas com 0 horas.")
    
    # Detect outliers
    outliers = df[df['Horas'] > 100]
    if not outliers.empty:
        logging.error(f"🚨 Crítico: Detetadas horas excessivas (>100h) em {len(outliers)} linhas.")