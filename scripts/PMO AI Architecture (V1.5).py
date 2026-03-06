# PROJECT: PMO AI Architecture (V1.5)
# GOAL: Master Functions, Parameters and Prompt Engineering
# AUTHOR: Daniela Marques | DATE: Wednesday, March 4th, 2026

import pandas as pd
import datetime

# --- FUNDAMENTOS: O QUE É UMA FUNÇÃO? ---
# Imagina uma função como uma receita: tu dás os ingredientes (parâmetros)
# e ela devolve o prato pronto (return).

def criar_prompt_estrategico(nome_projeto, risco, variancia):
    """
    Esta função recebe dados do projeto e constrói uma pergunta 
    profissional para ser enviada a uma IA no futuro.
    """
    # Usamos f-strings (o f antes das aspas) para inserir variáveis no texto
    prompt = f"Como consultor sénior, analisa o projeto '{nome_projeto}'. " \
             f"O risco atual é '{risco}' e a variância orçamental é de {variancia}€. " \
             f"Gera um plano de mitigação de 3 passos."
    
    return prompt # O 'return' é o resultado final que sai da função

def simulador_resposta_ia(prompt_gerado):
    """
    Como não usamos API KEY, esta função simula o comportamento da IA.
    Em programação, isto chama-se 'MOCKING'.
    """
    # Simulamos um processamento baseado no conteúdo do prompt
    return "[SIMULAÇÃO IA] Recomendação: Rever alocação de recursos e ativar plano B."

def executar_sessao():
    
    
    # 1. DATA (O nosso dicionário - a base de tudo)
    data = {
        'Projeto': ['Risk Automation', 'Cloud Migration'],
        'Risco': ['Atraso na API', 'Base de dados lenta'],
        'Variancia': [1500, -2000] # Positivo é sobra, Negativo é défice
    }
    
    df = pd.DataFrame(data)

    # 2. APLICAÇÃO DA LÓGICA (Onde o Python brilha)
    # Criamos a coluna de Prompts usando a nossa função
    # O 'lambda' é como um estagiário que leva cada linha até à função
    df['Prompt_Gerado'] = df.apply(lambda x: criar_prompt_estrategico(x['Projeto'], x['Risco'], x['Variancia']), axis=1)

    # 3. SIMULAÇÃO DE RESPOSTA
    df['Recomendacao_IA'] = df['Prompt_Gerado'].apply(simulador_resposta_ia)

    # 4. OUTPUT PARA O TERMINAL
    print("\nEXEMPLO DE PROMPT CONSTRUÍDO:")
    print(df['Prompt_Gerado'].iloc[0])
    
    print("\nRELATÓRIO FINAL (PRONTO PARA ESCALAR):")
    print(df[['Projeto', 'Recomendacao_IA']])

    print("\n" + "="*60)
    print("LOG: Lógica de Prompting validada. Sistema pronto para conexão API.")
    
    