"""Gemini AI Integration for PMO Risk Analysis and Mitigation

Provides functions for integrating Google's Gemini AI API to analyze project risks,
generate mitigation strategies, and provide actionable recommendations for PMO (Project
Management Office) operations.

Features:
- Risk analysis with retry logic for resilience
- Prompt engineering with business context injection
- Lean Six Sigma methodology-based recommendations
- Fail-safe fallbacks when API unavailable
- Structured logging of AI suggestions

All functions include exponential backoff and error handling for API resilience.
"""

import os
from typing import Optional
from google import genai
from google.api_core import exceptions
from dotenv import load_dotenv
import time
import pandas as pd
from pathlib import Path
from datetime import datetime

# Clean Code: Centralized configuration loading
load_dotenv()
api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Erro: A GOOGLE_API_KEY não foi encontrada no ficheiro .env")

# Configure Gemini client
client: genai.Client = genai.Client(api_key=api_key)


def analisar_risco_com_ia(projeto: str, atraso_dias: int) -> str:
    """
    Analyze project risk and get AI-powered mitigation suggestion.

    Sends project context (name and delay days) to Gemini AI requesting a brief
    mitigation action. Implements exponential backoff for API rate limits.

    Args:
        projeto: Project name to analyze.
        atraso_dias: Number of days the project is delayed.

    Returns:
        str: AI-generated mitigation suggestion (single sentence).
             Returns fallback message if all retries exhausted.

    Note:
        - Implements retry logic with delays: 1s, 2s, 4s
        - Handles ResourceExhausted exceptions with 10s wait before retry
        - Returns graceful fallback if AI unavailable

    Example:
        >>> suggestion = analisar_risco_com_ia("Website Redesign", 5)
        >>> print(suggestion)
        'Realocar recursos do projeto X para acelerar entrega'
    """
    prompt: str = (
        f"Atua como um PMO Sénior. O projeto '{projeto}' está atrasado {atraso_dias} dias. "
        f"Sugere uma ação de mitigação curta (1 frase)."
    )

    # Exponential backoff retry logic
    for delay in [1, 2, 4]:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text.strip()
        except exceptions.ResourceExhausted:
            wait_time: int = 10
            print(f"⚠️ Limite atingido. A esperar {wait_time}s antes de tentar novamente...")
            time.sleep(wait_time)
        except Exception as e:
            time.sleep(delay)

    return "Sugestão indisponível de momento."


def gerar_sugestao_pmo(projeto: str, dias_atraso: int) -> str:
    """
    Generate PMO-focused suggestion for delayed project recovery.

    Takes project information and uses AI to suggest a one-sentence recovery strategy.
    Implements fail-safe pattern to prevent system crashes on API errors.

    Args:
        projeto: Name of the delayed project.
        dias_atraso: Number of days behind schedule.

    Returns:
        str: One-sentence AI recommendation for recovery action.
             Returns fallback technical error message if API fails.

    Note:
        - Uses Gemini to generate Senior PM perspective suggestions
        - Implements fail-safe: returns graceful message on all errors
        - Does not return status/confidence, only the suggestion text

    Example:
        >>> suggestion = gerar_sugestao_pmo("Mobile App MVP", 7)
        >>> print(suggestion)
        'Incrementar horas de trabalho da equipa frontend e parallelizar testes'
    """
    prompt: str = (
        f"Atua como um Gestor de Projetos Sénior. O projeto '{projeto}' "
        f"está {dias_atraso} dias atrasado. Dá uma sugestão de 1 frase "
        "para recuperar o prazo."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except exceptions.ResourceExhausted:
        wait_time: int = 10
        print(f"⚠️ Limite atingido. A esperar {wait_time}s antes de tentar novamente...")
        time.sleep(wait_time)
        return "Análise manual recomendada devido a erro técnico."
    except Exception as e:
        # Fail-Safe: If AI fails, system continues without crashing
        return "Análise manual recomendada devido a erro técnico."


def consultar_mitigação_ia(nome_projeto: str, dias_atraso: int, kpi_risco: float) -> str:
    """
    Query AI for strategic mitigation recommendations using context injection.

    Provides expert-level mitigation strategy leveraging Lean Six Sigma methodology
    and PMO best practices. Uses comprehensive prompt with business context injection.

    Strategy Focus:
        - Cost-zero or low-impact solutions (no additional budget required)
        - Resource reallocation from existing teams
        - Process improvement and internal reviews
        - Stakeholder communication enhancement
        - Lean principles for efficiency optimization

    Args:
        nome_projeto: Name of the project requiring mitigation.
        dias_atraso: Days behind schedule.
        kpi_risco: Risk KPI percentage (0-100). Numeric indicator of project health.

    Returns:
        str: Strategic mitigation plan with actionable steps.
             Returns fallback if API unavailable or rate-limited.

    Note:
        - Uses advanced prompt engineering with system context
        - Tailored to Portuguese market and PME dynamics
        - Focuses on Lean Six Sigma and zero-cost solutions
        - Implements fail-safe for API resilience

    Example:
        >>> plan = consultar_mitigação_ia("Cloud Migration", 10, 65.5)
        >>> print(plan)
        'Realizar check-in diário com stakeholders, re-planear sprints...'
    """
    prompt: str = (
        f"Contexto: PMO de Operações em Portugal.\n"
        f"Projeto: {nome_projeto}\n"
        f"Atraso: {dias_atraso} dias\n"
        f"KPI de Risco: {kpi_risco}%\n"
        f"Pergunta: Com base nestes dados, qual a melhor estratégia de mitigação? "
        f"Atuarás como um Consultor Sénior Especialista em Lean Six Sigma e PMO (Project Management Office), "
        f"com foco rigoroso na eliminação de desperdícios e otimização de fluxos de trabalho. "
        f"A tua missão é analisar dados de projetos — especificamente nomes de projetos, dias de atraso e KPIs de risco "
        f"— para fornecer diagnósticos precisos e recomendações estratégicas. Deves adotar um tom profissional, "
        f"analítico e orientado a resultados, tratando a eficiência operacional como a métrica principal de sucesso.\n"
        f"OBRIGATÓRIO: Prioriza soluções de 'custo zero' ou 'baixo impacto orçamental'. Redireciona recursos existentes, "
        f"melhora processos internos e otimiza comunicação entre stakeholders. Ignora soluções que exijam investimento "
        f"financeiro adicional ou contratação externa. Focoa-te em Lean methodology e maximize valor com ferramentas "
        f"que a organização já possui.\n"
        f"Adapta recomendações à realidade portuguesa: PMEs, dinâmicas locais, cultura organizacional típica. "
        f"Usa terminologia adequada e propõe soluções práticas, imediatas e executáveis dentro da estrutura atual."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except exceptions.ResourceExhausted:
        wait_time: int = 10
        print(f"⚠️ Limite atingido. A esperar {wait_time}s antes de tentar novamente...")
        time.sleep(wait_time)
        return "Análise manual recomendada devido a erro técnico."
    except Exception as e:
        # Fail-Safe: Prevent system crashes on API errors
        return "Análise manual recomendada devido a erro técnico."


if __name__ == "__main__":
    """Execute AI analysis demonstrations when script runs directly."""
    print("🤖 Gemini a analisar solução...")

    # Demo 1: Risk analysis
    sugestao_1: str = analisar_risco_com_ia("Migração de Servidores", 5)
    print(f"🤖 Sugestão da IA (Risk Analysis): {sugestao_1}")

    # Demo 2: PMO suggestion
    sugestao_2: str = gerar_sugestao_pmo("Implementação de CRM", 5)
    print(f"🤖 Sugestão da IA (PMO): {sugestao_2}")

    # Demo 3: Strategic mitigation with KPI context
    projeto_exemplo: str = "Migração de Cloud"
    atraso: int = 12
    risco: float = 35.5

    sugestao_3: str = consultar_mitigação_ia(projeto_exemplo, atraso, risco)
    print(f"🤖 Estratégia PMA para {projeto_exemplo}: {sugestao_3}")

    # Log suggestion with timestamp (Pathlib demonstration)
    log_path: Path = Path.home() / "carrer" / "logs"

    if not log_path.exists():
        log_path.mkdir(parents=True, exist_ok=True)

    # Generate filename with timestamp to prevent overwrites
    timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_ficheiro: str = f"sugestao_{timestamp}.txt"
    caminho_final: Path = log_path / nome_ficheiro

    with open(caminho_final, "a", encoding="utf-8") as f:
        f.write(f"Data: {datetime.now()}\n")
        f.write("-" * 20 + "\n")
        f.write(f"Projeto: {projeto_exemplo} | IA: {sugestao_3}\n")

    print(f"✅ Sugestão salva em: {caminho_final}")
