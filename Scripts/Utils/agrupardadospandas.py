"""PMO Data Aggregation and Analysis Module

This module provides functions for loading, validating, and analyzing Project Management
Office (PMO) data from CSV files. It calculates portfolio health metrics, generates
formatted reports, and integrates AI-based risk analysis.

Key Functions:
    - carregar_dados: Load and validate CSV data
    - validar_colunas: Check for required columns
    - sanitizar_dados: Clean and type-convert data
    - calcular_metrica_saude: Calculate portfolio health KPIs
    - formatar_relatorio_kpis: Format metrics as readable report
    - calcular_saude_projeto: Main pipeline function

Each function includes comprehensive logging for audit trails and error tracking.
"""

import os

import pandas as pd
import logging
from pathlib import Path
from typing import Optional, Dict, List, Union, Any
from importlib.metadata import metadata
import inspect
import notificaçao
from notificaçao import gerar_report_pmo
from testaiproject import analisar_risco_com_ia
from testaiproject import consultar_mitigação_ia

# Configuração de Logs persistentes (conforme o teu sucesso de ontem!)
logging.basicConfig(level=logging.INFO, format='%(asctime)s -- %(levelname)s - %(message)s')


def carregar_dados(caminho_csv: str) -> Optional[pd.DataFrame]:
    """
    Load CSV file and validate its existence.
    
    Attempts to load a CSV file from the specified path. Returns None and logs
    an error if the file doesn't exist or cannot be read.

    Args:
        caminho_csv: Absolute or relative path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: Loaded DataFrame if successful, None on error.
                               Log message indicates number of rows loaded.

    Raises:
        No exceptions raised. All errors are logged and None is returned.

    Example:
        >>> df = carregar_dados('dados_pmo_segunda.csv')
        >>> if df is not None:
        ...     print(f"Loaded {len(df)} rows")
    """
    if not Path(caminho_csv).exists():
        logging.error(f"❌ Ficheiro crítico em falta: {caminho_csv}")
        return None

    try:
        df: pd.DataFrame = pd.read_csv(caminho_csv)
        logging.info(f"✅ CSV carregado: {caminho_csv} ({len(df)} linhas)")
        return df
    except Exception as e:
        logging.error(f"💥 Erro ao carregar CSV '{caminho_csv}': {e}")
        return None


def validar_colunas(df: pd.DataFrame, colunas_esperadas: List[str]) -> bool:
    """
    Validate that DataFrame contains all required columns.

    Checks if the DataFrame has all columns specified in the expected columns list.
    Logs error with missing column names if validation fails.

    Args:
        df: DataFrame to validate for required columns.
        colunas_esperadas: List of required column names.

    Returns:
        bool: True if all columns present, False if any are missing.

    Note:
        Missing columns are logged with error level for troubleshooting.

    Example:
        >>> df = pd.DataFrame({'Status': [1], 'Projeto': ['P1']})
        >>> validar_colunas(df, ['Status', 'Projeto'])
        True
        >>> validar_colunas(df, ['Status', 'Tempo_Gasto'])
        False  # Logs error about missing 'Tempo_Gasto'
    """
    faltam: list[str] = [c for c in colunas_esperadas if c not in df.columns]
    if faltam:
        logging.error(f"💥 Colunas em falta: {faltam}")
        return False
    return True


def sanitizar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean data by removing nulls and converting column types.

    Removes rows with null Status values and converts Tempo_Gasto column to numeric.
    Handles edge cases like values with time unit suffixes (e.g., "5h").

    Args:
        df: DataFrame to sanitize. Required columns: Status, Tempo_Gasto.

    Returns:
        pd.DataFrame: Cleaned DataFrame with nullable rows removed and types converted.

    Note:
        - Modifies the DataFrame in-place
        - Logs warnings when null values are encountered
        - Handles 'h' suffix removal for time values (e.g., "5h" -> 5)
        - Missing Tempo_Gasto values filled with 0

    Example:
        >>> df = pd.DataFrame({
        ...     'Status': ['Concluído', None, 'Atrasado'],
        ...     'Tempo_Gasto': ['5h', '10', None]
        ... })
        >>> cleaned = sanitizar_dados(df)
        # Returns df with null Status row removed and Tempo_Gasto as floats
    """
    if df['Status'].isnull().any():
        logging.warning("⚠️ Encontrados valores nulos no Status. A limpar...")
        df = df.dropna(subset=['Status'])

    df['Tempo_Gasto'] = pd.to_numeric(df.get('Tempo_Gasto', pd.Series(dtype='float64')), errors='coerce').fillna(0)
    if 'Tempo_Gasto' in df.columns:
        df['Tempo_Gasto'] = df['Tempo_Gasto'].astype(str).str.replace('h', '', case=False)
        df['Tempo_Gasto'] = pd.to_numeric(df['Tempo_Gasto'], errors='coerce')

    return df


def preparar_dados(caminho_csv: str) -> Optional[pd.DataFrame]:
    """
    Complete pipeline for loading, validating, and cleaning CSV data.

    Orchestrates the full data preparation workflow: load → validate → clean.
    Returns None if any step fails, with detailed error logging.

    Args:
        caminho_csv: Path to the CSV file to process.

    Returns:
        Optional[pd.DataFrame]: Prepared DataFrame if successful, None on any failure.

    Note:
        - Expects columns: Status, Projeto, Tempo_Gasto
        - Each step logs detailed information about validation results
        - Returns None immediately if validation fails (fail-fast pattern)

    Example:
        >>> df = preparar_dados('dados_pmo.csv')
        >>> if df is not None:
        ...     metrics = calcular_metrica_saude(df)
    """
    df: Optional[pd.DataFrame] = carregar_dados(caminho_csv)
    if df is None:
        return None

    colunas_esperadas: list[str] = ['Status', 'Projeto', 'Tempo_Gasto']
    if not validar_colunas(df, colunas_esperadas):
        return None

    return sanitizar_dados(df)


def calcular_metrica_saude(df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """
    Calculate portfolio health metrics from project data.

    Computes key performance indicators (KPIs) for portfolio health assessment:
    - Total task count
    - Risk percentage (delayed tasks)
    - Completion rate
    - Unreported tasks percentage
    - AI-based risk analysis for delayed projects

    Args:
        df: DataFrame with columns: Status, Tempo_Gasto, Projeto.
           Requires at least one row of data.

    Returns:
        Optional[Dict[str, Any]]: Dictionary with calculated KPIs:
            - total_tarefas: Count of all tasks
            - percentual_risco: % of delayed tasks
            - taxa_conclusao: % of completed tasks
            - taxa_nao_reportados: % of tasks without reported time
            - respostaai: AI risk analysis response
            Returns None if DataFrame is empty.

    Logs Warnings:
        - Risk > 50%: High risk detection warning
        - Completion < 50%: Low completion rate warning
        - Unreported > 20%: High unreported task percentage

    Note:
        - Sets status to 'Erro de Reporte' for tasks with unreported time
        - Base calculation excludes unreported tasks for percentages
        - Integrates with AI module for risk analysis of delayed projects

    Example:
        >>> metrics = calcular_metrica_saude(df)
        >>> if metrics:
        ...     print(f"Risk: {metrics['percentual_risco']:.1f}%")
    """
    total_tarefas: int = len(df)
    if total_tarefas == 0:
        logging.warning("⚠️ O ficheiro CSV está vazio. Não há tarefas para calcular.")
        return None

    atrasados: int = len(df[df['Status'] == 'Atrasado'])
    concluidos: int = len(df[df['Status'] == 'Concluído'])
    nao_reportados: int = int(df['Tempo_Gasto'].isna().sum())

    df.loc[df['Tempo_Gasto'].isna(), 'Status'] = 'Erro de Reporte'

    base: int = total_tarefas - nao_reportados
    percentual_risco: float = (atrasados / base) * 100 if base > 0 else 0
    taxa_conclusao: float = (concluidos / base) * 100 if base > 0 else 0
    taxa_nao_reportados: float = (nao_reportados / total_tarefas) * 100

    if percentual_risco > 50:
        logging.warning(f"⚠️ Alta taxa de risco detectada: {percentual_risco:.1f}% dos projetos estão atrasados.")
    if taxa_conclusao < 50:
        logging.warning(f"⚠️ Baixa taxa de conclusão detectada: Apenas {taxa_conclusao:.1f}% dos projetos estão concluídos.")
    if taxa_nao_reportados > 20:
        logging.warning(f"⚠️ Alta taxa de não reportados: {taxa_nao_reportados:.1f}% das tarefas não têm tempo gasto reportado.")
    
    test: Optional[str] = None
    if [df['Status'] == 'Atrasado']:
        test = analisar_risco_com_ia([df['Projeto']], 5)

    return {
        'total_tarefas': total_tarefas,
        'percentual_risco': percentual_risco,
        'taxa_conclusao': taxa_conclusao,
        'taxa_nao_reportados': taxa_nao_reportados,
        'respostaai': test,
    }


def formatar_relatorio_kpis(kpis: Optional[Dict[str, Union[int, float]]]) -> Union[str, Dict[str, Any]]:
    """
    Format calculated metrics into a readable report.

    Converts KPI dictionary into formatted text report or returns raw metrics
    if no data is available.

    Args:
        kpis: Dictionary of KPIs from calcular_metrica_saude() or None.

    Returns:
        Union[str, Dict]: If kpis is None, returns descriptive message string.
                         Otherwise returns the kpis dictionary for further processing.

    Note:
        - Original implementation has all formatting lines commented out
        - Currently returns raw dict for flexibility in downstream processing
        - Can be extended with custom formatting as needed

    Example:
        >>> kpis = {'total_tarefas': 10, 'percentual_risco': 30.0}
        >>> report = formatar_relatorio_kpis(kpis)
        >>> print(report)  # Returns the kpis dict
    """
    if kpis is None:
        return "Nenhuma tarefa encontrada no relatório."
    return kpis


def calcular_saude_projeto(caminho_csv: str) -> Optional[Union[str, Dict[str, Any]]]:
    """
    Main function to calculate project health from CSV file.

    Orchestrates complete workflow: data preparation → metric calculation → report formatting.
    Full error handling with logging at each step.

    Args:
        caminho_csv: Path to the CSV file containing project data.

    Returns:
        Optional[Union[str, Dict]]: Formatted report or metrics dict if successful,
                                     None if preparation or calculation fails.

    Raises:
        No exceptions raised. All errors are logged and None is returned.

    Note:
        - Implements complete fail-fast pattern with early returns
        - Logs errors at each major step for audit trail
        - Integrates all sub-functions in proper sequence

    Example:
        >>> report = calcular_saude_projeto('dados_pmo_segunda.csv')
        >>> if report:
        ...     print(f"Health Report: {report}")
    """
    df: Optional[pd.DataFrame] = preparar_dados(caminho_csv)
    if df is None:
        logging.error("💥 Falha na preparação dos dados.")
        return None

    kpis = calcular_metrica_saude(df)
    if [df['Status'] == 'Atrasado']:
        test=analisar_risco_com_ia([df['Projeto']],5)
        analise= consultar_mitigação_ia([df['Projeto']],5,kpis)
    if kpis is not None:
        return formatar_relatorio_kpis(kpis), analise
    else:
        return "Relatório não gerado: Projeto não está atrasado.", analise


def enviar_notificacoes(resultado, arquivo, analise_ia=None, canal=notificaçao.obter_configuracoes_slack().get("canal_id")):
                                      #envia notificações  com o resultado do cálculo.
    """
Args: 
       Resultado (str or None): Relatório a ser enviado ou None em caso de falha.
        arquivo (str): Caminho do arquivo para anexar.
        canal (str): ID do canal do Slack (padrão: notificaçao.CANAL_ID).
""" 

    if not resultado:
        payload = notificaçao.construir_payload_visual(
            "💥 Falha ao calcular a saúde do projeto. Verifique os logs para detalhes.",
            "https://www.exemplo.com/relatorio-pmo.xlsx",
        )
        notificaçao.enviar_alerta_slack(payload)
        return

    notificaçao.test_api_configuration()
    payload = notificaçao.construir_payload_visual(resultado, "https://www.exemplo.com/relatorio-pmo.xlsx")
    layout_final= notificaçao.gerar_report_pmo("diario", resultado)
    if analise_ia:
        bloco_ia = {
            "type": "section",
            "text": {
                "type": "mrkdwn", 
                "text": f"*🤖 Análise da IA (Mitigação):*\n>{analise_ia}"
            }
        }
        # Adicionamos o bloco ao final da lista de blocos do payload
        payload["blocks"].append(bloco_ia)
    notificaçao.enviar_alerta_slack(payload, layout_final)
    notificaçao.enviar_ficheiro_slack(arquivo, canal)


if __name__ == "__main__":
    # Get the name of the file that initiated the execution
    stack = inspect.stack()
    # The last element in the stack is usually the entry point script
    entry_point_file = os.path.basename(stack[-1].filename)
    if entry_point_file == "main.py":
        
        caminho = 'dados_pmo_segunda2.csv'
    # 1. Recebe os dois valores separadamente (Unpacking)
        relatorio_kpis, analise_ia = calcular_saude_projeto(caminho)
        enviar_notificacoes(relatorio_kpis, caminho, analise_ia=analise_ia)

        if  relatorio_kpis:
            print( relatorio_kpis, analise_ia)
        else:
            logging.error("💥 Falha ao calcular a saúde do projeto. Verifique os logs para detalhes.")
           #enviar_notificacoes(resultado, caminho) 
        