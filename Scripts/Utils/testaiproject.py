import os
from google import genai
from google.api_core import exceptions
from dotenv import load_dotenv
import time
import pandas as pd
from pathlib import Path
from datetime import datetime

# CLEAN CODE: Carregamento centralizado de configurações
# 1. Setup: Carregar a chave do cofre (.env)
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
        raise ValueError("Erro: A GEMINI_API_KEY não foi encontrada no ficheiro .env")

# 2. Configurar o Motor (Kernel)
# Clean Code Principle: Encapsulate the connection in a client object
client = genai.Client(api_key=api_key)

def analisar_risco_com_ia(projeto, atraso_dias):
    """
    PROGRAMMING BASE: Integração de API Externa.
    Envia o contexto do projeto para o Gemini e recebe uma sugestão de mitigação.
    """
    prompt = f"Atua como um PMO Sénior. O projeto '{projeto}' está atrasado {atraso_dias} dias. Sugere uma ação de mitigação curta (1 frase)."
    
    # Implementação de Retries (Resiliência)
    for delay in [1, 2, 4]:
        try:
            response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=(prompt)
)
            return response.text.strip()
        except exceptions.ResourceExhausted:
            wait_time =  10  # Espera 10s, depois 20s...
            print(f"⚠️ Limite atingido. A esperar {wait_time}s antes de tentar novamente...")
            time.sleep(wait_time)
        except Exception as e:
            time.sleep(delay)
    
    return "Sugestão indisponível de momento."
def gerar_sugestao_pmo(projeto, dias_atraso):
    """
    Recebe dados do projeto e usa IA para sugerir uma solução.
    Princípio: Input Limpo -> Output Útil.
    """
    prompt = (
        f"Atua como um Gestor de Projetos Sénior. O projeto '{projeto}' "
        f"está {dias_atraso} dias atrasado. Dá uma sugestão de 1 frase "
        "para recuperar o prazo."
    )

    try:
        # Chamada à API (Pode demorar alguns segundos)
     response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=(prompt)
)
     
     return response.text.strip()
    except exceptions.ResourceExhausted:
            wait_time =  10  # Espera 10s, depois 20s...
            print(f"⚠️ Limite atingido. A esperar {wait_time}s antes de tentar novamente...")
            time.sleep(wait_time)
    except Exception as e:
        # Fail-Safe: Se a IA falhar, não crashamos o sistema
        return "Análise manual recomendada devido a erro técnico."
def consultar_mitigação_ia(nome_projeto, dias_atraso, kpi_risco):
    """
    PROGRAMMING BASE: Prompt Engineering.
    Injeta contexto de negócio no modelo para obter respostas acionáveis.
    """
    # System Instruction implícita no Prompt
    prompt = (
        f"Contexto: PMO de Operações em Portugal.\n"
        f"Projeto: {nome_projeto}\n"
        f"Atraso: {dias_atraso} dias\n"
        f"KPI de Risco: {kpi_risco}%\n"
        f"Pergunta: Com base nestes dados, qual a melhor estratégia de mitigação? "
        f"Atuarás como um Consultor Sénior Especialista em Lean Six Sigma e PMO (Project Management Office), com foco rigoroso na eliminação de desperdícios e otimização de fluxos de trabalho. A tua missão é analisar dados de projetos — especificamente nomes de projetos, dias de atraso e KPIs de risco — para fornecer diagnósticos precisos e recomendações estratégicas. Deves adotar um tom profissional, analítico e orientado a resultados, tratando a eficiência operacional como a métrica principal de sucesso em cada interação.Nas tuas recomendações, é obrigatório priorizar soluções de 'custo zero' ou 'baixo impacto orçamental'. Deves focar-te na reafectação de recursos existentes, revisão de processos internos e melhoria da comunicação entre stakeholders, ignorando qualquer solução que exija investimento financeiro adicional ou contratação externa. A abordagem deve ser puramente baseada na metodologia Lean, procurando simplificar o complexo e maximizar o valor entregue com as ferramentas que a organização já possui.Todas as sugestões devem ser adaptadas à realidade e cultura do mercado de trabalho em Portugal, considerando a predominância de PMEs e as dinâmicas específicas de gestão de equipas locais. Deves utilizar terminologia técnica adequada ao contexto português (como 'prazos', 'partes interessadas' e 'objetivos') e propor soluções que respeitem o equilíbrio organizacional típico das empresas nacionais. O objetivo final é transformar os dados de atraso e risco em planos de ação práticos, imediatos e executáveis dentro da estrutura atual do projeto."
    )
    
    try:
        # Chamada à API (Pode demorar alguns segundos)
     response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=(prompt)
)
     
     return response.text.strip()
    except exceptions.ResourceExhausted:
            wait_time = 10  # Espera 10s, depois 20s...
            print(f"⚠️ Limite atingido. A esperar {wait_time}s antes de tentar novamente...")
            time.sleep(wait_time)
    except Exception as e:
        # Fail-Safe: Se a IA falhar, não crashamos o sistema
        return "Análise manual recomendada devido a erro técnico."


if __name__ == "__main__":
    print("🤖 Gemini a analisar solução...")
    # Teste rápido de integração
    sugestao = analisar_risco_com_ia("Migração de Servidores", 5)
    
    print(f"🤖 Sugestão da IA: {sugestao}")
       # Teste de Laboratório
    print("🤖 Gemini a analisar solução...")
    sugestao = gerar_sugestao_pmo("Implementação de CRM", 5)
    
    print(f"🤖 Sugestão da IA: {sugestao}")

    # Simulação de dados vindo do teu CSV/Pandas
    projeto_exemplo = "Migração de Cloud"
    atraso = 12
    risco = 35.5 # KPI
    print("🤖 Gemini a analisar solução...")
    sugestao = consultar_mitigação_ia(projeto_exemplo, atraso, risco)
    
# Pathlib: Guardar a sugestão num log diário
    log_path = Path.home() / "carrer" / "logs"
    
    if not log_path.exists():
        print("A pasta não existe")
   # 3. Gerar nome do ficheiro com timestamp para não sobrepor
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_ficheiro = f"sugestao_{timestamp}.txt"
    caminho_final = Path(log_path/nome_ficheiro)
        
    with open(caminho_final,"a", encoding="utf-8") as f:
        f.write(f"Data: {datetime.now()}\n")
        f.write("-" * 20 + "\n")
        f.write(f"Projeto: {projeto_exemplo} | IA: {sugestao}\n")
        
    print(f"🤖 IA sugere para {projeto_exemplo}: {sugestao}")
