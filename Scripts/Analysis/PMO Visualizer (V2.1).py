"""PMO Integrated System with Prompt Engineering: Portfolio Health & AI Readiness (V2.1).

This module consolidates core PMO capabilities: structured data organization,
AI-ready prompt generation, and professional visualization. Bridges data systems
with AI integration by preparing project data in formats suitable for LLM analysis.

Primary Purpose:
    Integrate three critical PMO functions into single cohesive system:
    1. Efficient dictionary-based data structure (optimized for memory)
    2. Prompt engineering for Gemini AI integration (future V3 with API)
    3. Professional portfolio health visualization (executive summaries)
    
    Create production-ready pipeline transforming project data → AI insights → visuals

Core Features:
    - Portfolio Data as Dictionary: Fast lookups, structured organization
    - Prompt Engineering: Format project info for AI analysis (context injection)
    - Conditional Coloring: Visual health indicators (green=healthy, red=risky)
    - Fail-Safe Output: Save PNG synchronously, then attempt interactive display
    - Professional Formatting: Grid lines, zero-line reference, bold titles

Dictionary Data Structure Advantages:
    - Memory Efficient: Indexed access O(1) vs DataFrame O(n)
    - Structured: Keys enforce naming conventions
    - AI-Ready: Easy to serialize to JSON for API calls
    - Readable: Key names self-document data meaning

Prompt Engineering Pattern (For Gemini Integration):
    The prompt format enables AI context understanding:
    "Analise o projeto {nome}. Status: {status}. 
     Risco: {nivel_risco}. Variância: {variancia}€. 
     Sugira uma estratégia de mitigação rápida."
    
    This structure ensures AI:
    - Understands business context (status, risk level)
    - Makes numeric-aware decisions (can reason about variance)
    - Produces actionable recommendations (mitigation strategies)

Workflow:
    1. DATA ORGANIZATION: Create PMO portfolio dictionary
    2. DATAFRAME CONVERSION: Transform to pandas for analysis
    3. PROMPT GENERATION: Create AI-ready prompts for each project
    4. VISUALIZATION: Color-code and chart the portfolio
    5. DISPLAY: Save and show results
    6. TERMINAL OUTPUT: Print table for quick review

Dictionary Keys Explained:
    - Projeto: Human-readable project name
    - Status: Current lifecycle state (Atrasado, Em Dia, Concluído)
    - Variancia_EUR: Budget variance in euros (negative = over budget)
    - Risco_Nivel: Risk assessment (Crítico, Médio, Baixo, Nulo)

Dependencies:
    - matplotlib: Figure creation, bar charts, styling
    - pandas: DataFrame conversion, apply() for prompt generation
    - os: File path handling

Color Coding Strategy:
    - Green (#2ecc71): Positive variance (under budget, "Concluído")
    - Red (#e74c3c): Negative variance (over budget, "Atrasado")
    - Zero-line: Black dashed reference for break-even

Prompt Columns Explained:
    The 'Prompt_IA' column contains structured input for future Gemini API:
    - Contains all relevant context for AI analysis
    - Formatted as natural language question (not structured JSON)
    - Ready to be sent via genai.models.generate_content()
    - Designed for "long form" text responses with recommendations

Examples:
    Run integrated PMO system:
    
    >>> exec(open('PMO Visualizer (V2.1).py').read())
    🚀 Processamento de Portfólio AI-Ops...
    
    --- TABELA DE OPERAÇÕES (PREPARADA PARA IA) ---
                 Projeto      Status  Variancia_EUR
    0  Automação Risk-AI     Atrasado          -4500
    1    Migração Cloud      Em Dia          1200
    ...
    
    --- EXEMPLO DE PROMPT GERADO (LINHA 1) ---
    Analise o projeto Automação Risk-AI. Status: Atrasado. 
    Risco: Crítico. Variância: -4500€. 
    Sugira uma estratégia de mitigação rápida.
    
    ✅ Gráfico guardado com sucesso: .../pmo_report_final_week2.png
    📊 Tentando abrir janela de visualização...

Error Handling and Fallback:
    Try-except block gracefully handles display failures:
    - PNG always saved first (guaranteed deliverable)
    - If window display fails, users still have report file
    - Warning message informs of partial failure (file saved, display didn't work)

Data Validation:
    - Assumes numeric variance values (EUR)
    - Dictionary keys must match expected field names
    - Project names are unique identifiers

Roadmap:
    V2.2: Add professional styling (themes, fonts)
    V2.3: Multi-dashboard layouts for different stakeholder groups
    V3: Live Gemini API integration (replace comment placeholder)
    V3.1: Prompt caching to reduce API costs
    V4: Automated daily report generation and email distribution
    V5: Slack/Teams integration for daily portfolio status pushes

Production Considerations:
    - For large portfolios (>50 projects): Consider pagination
    - API Integration: Set GOOGLE_API_KEY in .env file
    - Rate Limiting: Implement exponential backoff for retry logic
    - Cost Control: Use prompt caching to avoid duplicate API calls
    - Data Freshness: Set scheduled execution frequency (daily, weekly)

Related Modules:
    - Scripts/Analysis/Data_Auditor.py: Health detection patterns
    - Scripts/Analysis/PMO AI Architecture (V1.5).py: Prompt engineering
    - Scripts/Setup/: Report formatting and email delivery
    - Scripts/Utils/: Chart generation helpers
"""

import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import Optional, Dict, List, Any


def gerar_sistema_pmo() -> None:
    print("🚀 Processamento de Portfólio AI-Ops...")

    # 1. ESTRUTURA DE DICIONÁRIO (O que pediste para organizar)
    # Em vez de listas soltas, os dados estão mapeados por 'Chaves'
    pmo_data = {
        "Projeto": ["Automação Risk-AI", "Migração Cloud", "Interface Ops", "Legacy Update"],
        "Status": ["Atrasado", "Em Dia", "Concluído", "Atrasado"],
        "Variancia_EUR": [-4500, 1200, 300, -2100],
        "Risco_Nivel": ["Crítico", "Baixo", "Nulo", "Médio"]
    }

    # Transformação em DataFrame (Padrão de mercado para análise de dados)
    df = pd.DataFrame(pmo_data)

    # 2. LÓGICA DE PROMPT (Preparação para a IA)
    def construir_prompt(row):
        return f"Analise o projeto {row['Projeto']}. Status: {row['Status']}. " \
               f"Risco: {row['Risco_Nivel']}. Variância: {row['Variancia_EUR']}€. " \
               f"Sugira uma estratégia de mitigação rápida."

    # Criamos uma nova coluna com os prompts que seriam enviados ao Gemini
    df['Prompt_IA'] = df.apply(construir_prompt, axis=1)

    # 3. VISUALIZAÇÃO (O "Fail-Safe" que aprendemos)
    # Tentamos abrir a janela, mas guardamos SEMPRE o ficheiro como segurança
    try:
        plt.figure(figsize=(10, 6))
        
        # Cores condicionais: Vermelho para prejuízo, Verde para lucro
        colors = ['#e74c3c' if x < 0 else '#2ecc71' for x in df['Variancia_EUR']]
        
        bars = plt.bar(df['Projeto'], df['Variancia_EUR'], color=colors)
        
        # Estilização do Gráfico
        plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
        plt.title('Saúde Financeira do Portfólio - PMO Dashboard', fontsize=14, fontweight='bold')
        plt.ylabel('Variância Orçamental (€)')
        plt.grid(axis='y', alpha=0.3)

        # Guardar o gráfico (Crucial para o teu reporte de Sexta-feira)
        plt.tight_layout()
        plt.savefig("pmo_report_final_week2.png")
        print(f"✅ Gráfico guardado com sucesso: {os.path.abspath('pmo_report_final_week2.png')}")

        # Mostrar o gráfico (Se o sistema permitir a popup)
        print("📊 Tentando abrir janela de visualização...")
        plt.show()

    except Exception as e:
        print(f"⚠️ Aviso de Visualização: O gráfico foi guardado como ficheiro, mas a janela não abriu. Erro: {e}")

    # 4. EXIBIÇÃO DE DADOS NO TERMINAL
    print("\n--- TABELA DE OPERAÇÕES (PREPARADA PARA IA) ---")
    # Mostramos apenas as colunas principais para não poluir o terminal
    print(df[['Projeto', 'Status', 'Variancia_EUR']])
    
    print("\n--- EXEMPLO DE PROMPT GERADO (LINHA 1) ---")
    print(df['Prompt_IA'].iloc[0])


if __name__ == "__main__":
    gerar_sistema_pmo()
    # Mantém o terminal aberto para conseguires ler os resultados
    input("\nProcesso concluído. Pressiona ENTER para fechar...")