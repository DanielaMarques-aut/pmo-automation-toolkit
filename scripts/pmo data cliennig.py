
#pmo data cleaning
# O objetivo deste script é ler um arquivo CSV contendo dados de tempo gasto em projetos, 
# limpar os dados (removendo o 'h' e convertendo para números), agregar o tempo por projeto e
#  exportar um relatório final em formato CSV. 
# Este processo é crucial para garantir que os dados estejam prontos para análise e apresentação ao PMO,
#  facilitando a tomada de decisões informadas.
import os
import pandas as pd
import sys
import warnings
import glob
import logging
import datetime

def run_health_check():
    files = glob.glob("*pmo_*.csv")
    for f in files:
        try:
            df = pd.read_csv(f)
            status = "✅ OK" if not df.empty else "⚠️ EMPTY"
            print(f"File: {f} | Status: {status} | Rows: {len(df)}")
        except Exception as e:
            print(f"File: {f} | ❌ CORRUPT: {e}")
            log_event(f"ERROR: Corrupted file: {f}")
#Define the file name
File_name = 'dados_pmo_segunda.csv'
# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',filename=f"{File_name.replace('.csv', '.log')}", filemode='w')
def log_event(message):
    #Writes a timestamped message to the log file.
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(File_name.replace('.csv', '.log'), "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")



#criar função para ler o arquivo csv
def processar_dados(file_name):
    run_health_check()
    print(f"Processando o arquivo: {file_name}")
    log_event("SYSTEM START: Commencing daily PMO data pull.")

    #Verificar se o arquivo existe
    #Se o arquivo não for encontrado, exibe uma mensagem de erro e encerra a função.
    if not os.path.isfile(file_name):
        msg=f"Arquivo {file_name} não encontrado."
        print(f"❌ {msg}")
        log_event(f"ERROR: {msg}")
        return
    #Ler o arquivo csv usando pandas
    #O arquivo é lido em um DataFrame do pandas. Se houver um erro na leitura, ele é capturado e exibido.
    #Args: file_name (str): O nome do arquivo CSV a ser processado.
    #Returns: pd.DataFrame: O DataFrame contendo os dados lidos do arquivo.
    # Se o arquivo for lido com sucesso, os dados são carregados em um DataFrame para processamento adicional.
    # Se o dataframe estiver vazio (ou seja, contém apenas cabeçalhos sem dados), uma mensagem de aviso é exibida e a função é encerrada para evitar erros posteriores no processamento.
    try:
        df = pd.read_csv(file_name)
        if df.empty:
            warning=("⚠️ AVISO: Ficheiro vazio detetado! O ficheiro contém cabeçalhos mas não tem dados.")
            print(warning)
            log_event(warning)
            return
        sucess=("Dados carregados com sucesso!")
        print(f"✅ {sucess}")
        log_event(sucess)

        
    #LIMPEZA DOS DADOS
    # Removemos o 'h', convertemos para número e lidamos com vazios (NaN)
    #Limpa os dados de tempo gasto removendo o sufixo 'h' e tratando nulos.
    #Args:df (pd.DataFrame): DataFrame original com a coluna 'tempo_gasto'.
    #Returns: pd.DataFrame: DataFrame limpo com 'tempo_gasto' como tipo numérico e sem linhas nulas.
        df["tempo_gasto"] =  pd.to_numeric(df["tempo_gasto"].astype(str).str.replace("h","",case=False), errors='coerce')
    # Removemos linhas onde o Tempo_Gasto não pôde ser convertido (NaN)
        df = df.dropna(subset=["tempo_gasto"])

    #AGREGAÇÃO
    #Agrega o tempo gasto por projeto, somando os valores e ordenando do menor para o maior.
    #Args:df (pd.DataFrame): DataFrame limpo com a coluna 'tempo_gasto' como numérica.
    #Returns: pd.DataFrame: DataFrame agregado com o total de tempo gasto por projeto, ordenado do menor para o maior.
        resumo=df.groupby("projeto")["tempo_gasto"].sum().reset_index().sort_values(by="tempo_gasto", ascending=True)
    #OUTPUT FINAL
        print("\n📊 RELATÓRIO DE HORAS POR PROJETO:")
        print(resumo)
        log_event("SUCCESS: Report generated successfully.")
    # Guardar o resultado num novo Excel para o teu chefe
    # O relatório é exportado como 'relatorio_final.csv' na mesma pasta do script.
    #Args:resumo (pd.DataFrame): DataFrame agregado com o total de tempo gasto por projeto.
    #Returns: o arquivo em caso de sucesso, ou uma mensagem de erro caso haja falha na exportação.
        resumo.to_csv('relatorio_final.csv', index=False)
        print("\n✅ Relatório exportado como 'relatorio_final   .csv'")
        log_event("SUCCESS: Report exported as 'relatorio_final.csv'")
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        log_event(f"ERROR: Erro ao ler o arquivo: {e}")
        return None
processar_dados(file_name=File_name)
