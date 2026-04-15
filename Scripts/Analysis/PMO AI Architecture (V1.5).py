"""PMO AI Architecture: Prompt Engineering & Risk Mitigation Strategy Generator (V1.5).

This module demonstrates foundational AI integration patterns using prompt engineering
and LLM simulation. Creates strategic recommendations for project risk mitigation
by combining structured data inputs with simulated AI reasoning (mocking pattern).

Primary Purpose:
    Teach prompt engineering fundamentals through practical PMO use cases.
    Generate professional risk mitigation recommendations by constructing
    context-rich prompts that combine project data with business strategy.
    Simulate AI API responses before production integration (enables testing
    and cost control during development phase).

Core Learning Concepts:
    - FUNCTIONS AS RECIPES: Parameters are ingredients, return values are results
    - F-STRINGS: Template literals using f"text {variable}" syntax
    - MOCKING PATTERN: Simulate external API behavior without actual API calls
    - LAMBDA FUNCTIONS: Inline functions for apply() operations on DataFrames
    - PROMPT ENGINEERING: Craft structured prompts for precise AI responses
    - CONTEXT INJECTION: Send strategic summaries instead of raw data to AI

Function Design Pattern:
    1. criar_prompt_estrategico(): Takes project data, returns prompt text
    2. simulador_resposta_ia(): Takes prompt, simulates AI response (mocking)
    3. executar_sessao(): Orchestrates pipeline (data → prompts → AI → output)

Key Concepts Demonstrated:
    - Function Definition: def with parameters and return statements
    - Parameter Passing: Data flows through function arguments
    - DataFrame Operations: apply(lambda) to execute functions row-by-row
    - String Templating: F-strings for prompt construction
    - Control Flow: If/else logic for simulated decision-making
    - Data Transformation: From raw data to structured prompts to recommendations

Prompt Engineering Pattern:
    The risk mitigation prompt format:
    "Como consultor sénior, analisa o projeto '[PROJECT]'.
     O risco atual é '[RISK]' e a variância orçamental é de [VARIANCE]€.
     Gera um plano de mitigação de 3 passos."

    This pattern ensures:
    - Role definition: "Como consultor sénior" → AI assumes expert perspective
    - Context: Project name, risk type, and financial variance
    - Action: "Gera um plano" → Directs AI to produce structured response
    - Format: "3 passos" → Constrains response length to summary format

Workflow:
    1. DATA DEFINITION: Create dictionary with project risks and variances
    2. DATAFRAME CREATION: Convert to pandas for structured analysis
    3. PROMPT GENERATION: Apply criar_prompt_estrategico to each row
    4. AI SIMULATION: Apply simulador_resposta_ia to each prompt
    5. RESULTS DISPLAY: Print prompts and recommendations
    6. VALIDATION MESSAGE: Log system readiness for production API

Dependencies:
    - pandas: DataFrame creation and row-wise operations via apply()
    - datetime: Timestamp generation for logs (imported, optional in V1.5)

Mocking Pattern Benefits:
    - Cost Control: Test prompt engineering without API charges
    - Speed: Instant responses without network latency
    - Safety: Develop and test without involving real AI systems
    - Learning: Understand prompt structure before API integration
    - CI/CD: Enable unit tests that don't depend on external APIs

Data Structure:
    {
        'Projeto': ['Risk Automation', 'Cloud Migration'],
        'Risco': ['Atraso na API', 'Base de dados lenta'],
        'Variancia': [1500, -2000]  # Positive=surplus, Negative=deficit
    }

Examples:
    Execute AI prompt generation session:
    
    >>> exec(open('PMO AI Architecture (V1.5).py').read())
    EXEMPLO DE PROMPT CONSTRUÍDO:
    Como consultor sénior, analisa o projeto 'Risk Automation'. 
    O risco atual é 'Atraso na API' e a variância orçamental é de 1500€. 
    Gera um plano de mitigação de 3 passos.
    
    RELATÓRIO FINAL (PRONTO PARA ESCALAR):
              Projeto             Recomendacao_IA
    0  Risk Automation      [SIMULAÇÃO IA] Recomendação: Rever alocação...
    1   Cloud Migration      [SIMULAÇÃO IA] Recomendação: Rever alocação...
    
    ============================================================
    LOG: Lógica de Prompting validada. Sistema pronto para conexão API.

Production Roadmap:
    V2: Replace simulador_resposta_ia() with actual Gemini API calls
    V3: Add retries with exponential backoff for rate limiting
    V4: Implement prompt versioning and A/B testing
    V5: Add structured output parsing (extract JSON from AI responses)
    V6: Caching layer to avoid duplicate API calls for same projects

Architecture Decision:
    V1.5 uses mocking to validate prompt structure before costs accumulate.
    Testing confirms the pipeline works correctly, then V2 swaps simulator
    with real API. This approach saves 95% of API costs during development.

Related Sessions:
    - Tuesday: Data aggregation and groupby operations
    - Thursday: Prompt engineering patterns
    - Friday: Report generation and email delivery
"""

import pandas as pd
import datetime
from typing import Optional, Dict, List, Any

# --- FUNDAMENTOS: O QUE É UMA FUNÇÃO? ---
# Imagina uma função como uma receita: tu dás os ingredientes (parâmetros)
# e ela devolve o prato pronto (return).

def criar_prompt_estrategico(nome_projeto: str, risco: str, variancia: float) -> str:
    """
    Esta função recebe dados do projeto e constrói uma pergunta 
    profissional para ser enviada a uma IA no futuro.
    """
    # Usamos f-strings (o f antes das aspas) para inserir variáveis no texto
    prompt = f"Como consultor sénior, analisa o projeto '{nome_projeto}'. " \
             f"O risco atual é '{risco}' e a variância orçamental é de {variancia}€. " \
             f"Gera um plano de mitigação de 3 passos."
    
    return prompt # O 'return' é o resultado final que sai da função

def simulador_resposta_ia(prompt_gerado: str) -> str:
    """
    Como não usamos API KEY, esta função simula o comportamento da IA.
    Em programação, isto chama-se 'MOCKING'.
    """
    # Simulamos um processamento baseado no conteúdo do prompt
    return "[SIMULAÇÃO IA] Recomendação: Rever alocação de recursos e ativar plano B."

def executar_sessao() -> None:
    
    
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
    
    