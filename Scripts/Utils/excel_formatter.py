# excel_formatter.py
# Excel formatting utilities

import logging
from pandas import DataFrame
from openpyxl import load_workbook
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from config import (
    VERDE_FILL, VERMELHO_FILL, AMARELO_FILL, AZUL_ESCURO_FILL, FONTE_BRANCA,
    ARQUIVO_EXCEL_FORMATADO
)

def aplicar_cores_status(arquivo_excel_entrada: str, df: DataFrame) -> None:
    """
    Apply conditional formatting to an Excel file based on task status.

    This function loads an existing Excel file, applies color coding to the status column
    based on the values in the DataFrame, formats the header row with dark blue background
    and white text, and saves the formatted file.

    Color coding:
    - Red: Tasks with status "Atrasado" (Delayed)
    - Green: Tasks with status "Concluído" (Completed)
    - Yellow: All other statuses

    Args:
        arquivo_excel_entrada (str): Path to the input Excel file to be formatted.
        df (pandas.DataFrame): DataFrame containing the data with a 'Status' column
            that determines the color coding.

    Raises:
        FileNotFoundError: If the input Excel file does not exist.
        openpyxl.utils.exceptions.InvalidFileException: If the Excel file is corrupted.
        PermissionError: If there's no write permission for the output file.

    Note:
        The function assumes the Excel file has data starting from row 2 (row 1 is header).
        The status column is assumed to be column 3 (C).
        The formatted file is saved with the name defined in ARQUIVO_EXCEL_FORMATADO.
    """
    logging.info(f"Aplicar cores com base no status: {arquivo_excel_entrada}")
    wb: Workbook = load_workbook(arquivo_excel_entrada)
    ws: Worksheet = wb.active

    # Apply red for "Atrasado"
    df_riscos = df[df["Status"] == "Atrasado"]
    for index in df_riscos.index:
        ws.cell(row=index + 2, column=3).fill = VERMELHO_FILL

    # Apply green for "Concluído"
    df_concluidos = df[df["Status"] == "Concluído"]
    for index in df_concluidos.index:
        ws.cell(row=index + 2, column=3).fill = VERDE_FILL

    # Apply yellow for others
    df_outros = df[~df["Status"].isin(["Atrasado", "Concluído"])]
    for index in df_outros.index:
        ws.cell(row=index + 2, column=3).fill = AMARELO_FILL

    # Format header
    logging.info(f"A formatar visualmente o cabeçalho do relatório: {arquivo_excel_entrada}, aplicando cor azul escuro e fonte branca.")
    for i, cell in enumerate(ws[1]):
        logging.debug(f"A formatar célula do cabeçalho: {i} of {len(ws[1])} celulas.")
        cell.fill = AZUL_ESCURO_FILL
        cell.font = FONTE_BRANCA

    logging.info(f"Cores aplicadas com base no status. Relatório atualizado: {arquivo_excel_entrada}")
    logging.info(f"✨ Report Profissional gerado: {ARQUIVO_EXCEL_FORMATADO}")
    wb.save(ARQUIVO_EXCEL_FORMATADO)
