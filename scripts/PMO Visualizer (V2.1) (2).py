"""
PMO INTEGRATED SYSTEM (V2.0)
----------------------------
Este código consolida:
1. Estrutura de Dados em Dicionário (Eficiência)
2. Lógica de Prompt Engineering (IA Ready)
3. Visualização de Saúde de Portfólio (Storytelling)
"""

import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import os
matplotlib.use("TkAgg")

plt.rcParams["font.family"] = "Arial"      # fontfamily mais legível
plt.rcParams["font.size"] = 12             # tamanho de fonte mais confortável
def gerar_sistema_pmo():
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