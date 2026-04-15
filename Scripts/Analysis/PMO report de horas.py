"""PMO Hours Reporting System with Data Quality Validation.

This module automates the analysis of employee hours reporting, detecting
discrepancies, validating data quality, and generating escalation reports
for underreporting or over-reporting cases. Designed for compliance tracking
and resource utilization analysis in PMO environments.

Primary Purpose:
    Validate time tracking data from spreadsheets. Identify employees who
    have not reported sufficient hours, flagging under-utilization risk.
    Detect anomalies where reported hours exceed expected capacity (>100%).
    Generate Excel reports for HR/Operations review with automated status
    categorization (OK, Pendente, Atenção, Verificar).

Key Concepts:
    - Data Cleaning: Remove 'h' suffix and convert strings to numeric values
    - Percentage Calculation: Normalize reports against expected hours
    - Anomaly Detection: Identify outliers (NA values, >100%, <100%)
    - Conditional Logic: np.select() for multi-condition status assignment
    - Data Segregation: Split clean data from errors into separate exports
    - Quality Thresholds: Define business rules (e.g., >100% is error)

Workflow:
    1. FILE LOADING: Read hours spreadsheet from specified file path
    2. COLUMN NORMALIZATION: Strip whitespace from column names
    3. DATA CLEANING: Remove 'h' suffix, convert to numeric values
    4. PERCENTAGE CALCULATION: Calculate % of expected hours reported
    5. ANOMALY DETECTION: Identify missing data and over-reporting cases
    6. STATUS CLASSIFICATION: Assign status using multi-condition logic
    7. REPORT GENERATION: Export error cases for Operations review
    8. ALERT GENERATION: Highlight employees with pending hours

Data Quality Categories:
    - OK: 100% hours reported as expected
    - Verificar: Pessoa não encontrada (missing employee record)
    - Atenção (Reporte > 100%): Employee reported more hours than capacity
    - Pendente (Reporte < 100%): Employee has unreported hours remaining

Error Detection Logic:
    - Condition 1: pd.isna(H reportadas) → "Verificar: Pessoa não encontrada"
    - Condition 2: %report > 100 → "Atenção: Reporte > 100%"
    - Condition 3: %report < 100 → "Pendente: Horas em falta"
    - Default: 'OK' (100% hours reported)

Dependencies:
    - pandas: DataFrame operations, type conversion, Excel I/O
    - numpy: Conditional logic with np.select() for multi-option status
    - openpyxl: Implied via to_excel() for Excel export (loaded by pandas)

Expected Input Format:
    Columns: id, Nome, H reportadas, H a reportar, ...
    H reportadas: Float or string with 'h' suffix (e.g., "10h" or "10")
    H a reportar: Expected hours (capacity) for reporting period

Percentage Calculation Formula:
    %report = (H reportadas / H a reportar) * 100

Examples:
    Run hours validation and generate reports:
    
    >>> # Script runs automatically on import
    >>> # Output:
    Colunas encontradas:
    ['id', 'Nome', 'H reportadas', 'H a reportar']
    
    ⚠️ Colaboradores não identificados ou sem dados:
    id                      Nome
    1001  NaN (pessoa não encontrada)
    
    Casos com reporte acima de 100%:
         Nome  %report
    0   João     105.5%
    2   Maria   110.0%
    
    ⚠️ Alerta: Colaboradores com horas em falta:
         Nome  %report
    1  Carlos     85.0%
    3   Paulo     70.0%
    
    Ficheiro de erros gerado com sucesso! 🚀
    Ficheiro de faltas gerado com sucesso! 🚀

Output Files Generated:
    - revisao_pmo.xlsx: All errors (missing data, over-reporting, under-reporting)
    - H em falta.xlsx: Employees with pending hours to complete

Data Validation Assumptions:
    - Hours are properly formatted (numeric or with 'h' suffix)
    - Employee names are unique identifiers
    - Expected hours (H a reportar) is always positive
    - Reporting period matches Excel load date

Roadmap:
    V1.1: Add day-of-week breakdown (detect which days are under-reported)
    V2: Email notifications to managers for team under-reporting
    V3: Dashboard visualization with trend analysis
    V4: Integration with time tracking system (Jira, Azure DevOps)
    V5: Predictive analysis (forecast under-reporting before month-end)
    V6: Multi-period comparison (week-over-week, month-over-month trends)

Related Modules:
    - Scripts/Setup/: Email delivery for compliance reports
    - Scripts/Utils/: Excel formatting and styling
    - Data/Raw/: Source hour tracking spreadsheets
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, List, Any
# Carregar o arquivo Excel de um caminho específico
path =r"C:\Users\daniq\carrer\Data/PMO_report_horas.xlsx" 
import os
df = pd.read_excel(path)
df.columns = df.columns.str.strip()
# Verificar se as colunas foram lidas corretamente
print("Colunas encontradas:")
print(df.columns)
df[df.columns] = df[df.columns].apply(lambda x: x.str.strip())
# Verificar os tipos de dados de cada coluna
print(df.dtypes)
# Limpeza e conversão das colunas de horas
df['H reportadas'] = pd.to_numeric(df['H reportadas'].astype(str).str.replace('h', ''), errors='coerce')
df['H a reportar'] = pd.to_numeric(df['H a reportar'].astype(str).str.replace('h', ''), errors='coerce')

# Verificar se a conversão funcionou
print(df[['H reportadas', 'H a reportar']].dtypes)
# 3. Criar a nova coluna de % (O que não existia no Excel!)
df['%report'] = (df['H reportadas'] / df['H a reportar']) * 100

# Ver o resultado com a nova coluna
print(df[['Nome', 'H reportadas', 'H a reportar', '%report']].head())
# Isolar quem não tem dados válidos de horas (os "Não Encontrados")
nao_encontrados = df[df['H reportadas'].isna()]

print("⚠️ Colaboradores não identificados ou sem dados:")
print(nao_encontrados[['id', 'Nome']])

# Mostra quantas células vazias existem em cada coluna
print(df.isnull().sum())

# Filtrar apenas as linhas com erro de lógica
erros_percentagem = df[df['%report'] > 100].fillna(False)


print("Casos com reporte acima de 100%:")
print(erros_percentagem[['Nome', '%report']])

# 1. Definir as condições de erro (estas geram listas de True/False)
condicao_na = df['H reportadas'].isna()
condicao_excesso = df['%report'] > 100

# 2. Criar o DataFrame de erros unindo as duas condições
# Usamos o símbolo | para dizer "se uma ou outra for verdadeira"
df_erros = df[condicao_na | condicao_excesso].copy()


# Definir as condições
condicoes = [
    df['H reportadas'].isna(),
    df['%report'] > 100,
    df['%report'] < 100
]

# Definir as mensagens para cada condição
mensagens = [
    'Verificar: Pessoa não encontrada',
    'Atenção: Reporte > 100%',
    'Pendente: Horas em falta'
]

# Criar a coluna Status (se nenhuma condição for metida, fica 'OK')
df['Status'] = np.select(condicoes, mensagens, default='OK')

# Exportar apenas os erros para um novo ficheiro
df[df['Status'] != 'OK'].to_excel('revisao_pmo.xlsx', index=False)
print("Ficheiro de erros gerado com sucesso! 🚀")

# Filtrar quem reportou menos de 100%
alertas = df[df['%report'] < 100]

# Mostrar o resultado
print("⚠️ Alerta: Colaboradores com horas em falta:")
print(alertas[['Nome', '%report']])
# Exportar % <100 para um novo ficheiro
alertas.to_excel('H em falta.xlsx', index=False)
print("Ficheiro de faltas gerado com sucesso! 🚀")