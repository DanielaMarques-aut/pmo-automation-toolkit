
#pmo data cliennig
# O objetivo deste script é ler um arquivo CSV contendo dados de tempo gasto em projetos, 
# limpar os dados (removendo o 'h' e convertendo para números), agregar o tempo por projeto e
#  exportar um relatório final em formato CSV. 
# Este processo é crucial para garantir que os dados estejam prontos para análise e apresentação ao PMO,
#  facilitando a tomada de decisões informadas.
import os
import pandas as pd

#Define the file name
File_name = 'dados_pmo_segunda.csv'

#criar função para ler o arquivo csv
def processar_dados(file_name):
    print(f"Processando o arquivo: {file_name}")

    #Verificar se o arquivo existe
    if not os.path.isfile(file_name):
        print(f"Arquivo {file_name} não encontrado.")
        return
    #Ler o arquivo csv usando pandas
    try:
        df = pd.read_csv(file_name)
        if df.empty:
            print("⚠️ AVISO: Ficheiro vazio detetado! O ficheiro contém cabeçalhos mas não tem dados.")
            return
        print("Dados carregados com sucesso!")
        
    #LIMPEZA DOS DADOS
     # Removemos o 'h', convertemos para número e lidamos com vazios (NaN)
        df["tempo_gasto"] =  pd.to_numeric(df["tempo_gasto"].astype(str).str.replace("h","",case=False), errors='coerce')
    # Removemos linhas onde o Tempo_Gasto não pôde ser convertido (NaN)
        df = df.dropna(subset=["tempo_gasto"])
    #AGREGAÇÃO
        resumo=df.groupby("projeto")["tempo_gasto"].sum().reset_index().sort_values(by="tempo_gasto", ascending=True)
    #OUTPUT FINAL
        print("\n📊 RELATÓRIO DE HORAS POR PROJETO:")
        print(resumo)
        
    # Guardar o resultado num novo Excel para o teu chefe
        resumo.to_csv('relatorio_final.csv', index=False)
        print("\n✅ Relatório exportado como 'relatorio_final   .csv'")
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None
processar_dados(file_name=File_name)