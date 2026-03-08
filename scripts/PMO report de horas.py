# PMO report de horas
# Autor: Daniela Marques
# Data: 2024-08-03
import pandas as pd
import numpy as np
# Carregar o arquivo Excel de um caminho específico
path =r"C:\Users\daniq\carrer\Data/PMO_report_horas.xlsx" 
import os
df = pd.read_excel(path)
# Verificar se as colunas foram lidas corretamente
print("Colunas encontradas:")
print(df.columns)
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