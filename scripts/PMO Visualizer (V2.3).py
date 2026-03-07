"""
PMO INTEGRATED SYSTEM (V2.3)
----------------------------
Este código consolida:
1. Estrutura de Dados em Dicionário (Eficiência)
3. Visualização de Saúde de Portfólio (Storytelling)
O objetivo é criar um dashboard executivo que possa ser facilmente atualizado com novos dados, 
mantendo uma estética profissional e clara.(temas e estilos)
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. PREPARAÇÃO DO EXCEL (Simulação)
# Este bloco cria uma simulação de dados para testar
def criar_excel_teste():
    data = {
        'Departamento': ['Logística', 'Marketing', 'TI', 'RH', 'Vendas'],
        'Gasto_Real': [12000, 8500, 15000, 4000, 9200],
        'Budget_Planeado': [10000, 9000, 14000, 4500, 10000]
    }

    df_teste = pd.DataFrame(data)
    df_teste.to_excel("dados_pmo_trabalho.xlsx", index=False)
    print("✅ Ficheiro Excel de teste criado!")

def pmo_excel_visualizer():
    # Garantir que o ficheiro existe
    if not os.path.exists("dados_pmo_trabalho.xlsx"):
        criar_excel_teste()

    # --- 2. LEITURA DO EXCEL ---
    # Aqui é onde o Python le os dados do teu trabalho
    df = pd.read_excel("dados_pmo_trabalho.xlsx")
    
    # Criar uma coluna calculada (Lógica de PMO)
    df['Desvio'] = df['Budget_Planeado'] - df['Gasto_Real']

    # --- 3. ESTÉTICA E TEMAS 
    # Vamos usar o estilo 'seaborn-v0_8' para um look de consultoria
    plt.style.use('seaborn-v0_8-muted') 
    
    fig, ax = plt.subplots(figsize=(12, 7))

    # Gráfico de Barras Horizontal
    cores = ['#2ecc71' if x >= 0 else '#e74c3c' for x in df['Desvio']]
    bars = ax.barh(df['Departamento'], df['Desvio'], color=cores, edgecolor='black', alpha=0.8)

    # Detalhes de Expert
    ax.set_title('Análise de Performance Orçamental por Departamento', fontsize=16, pad=20)
    ax.set_xlabel('Desvio (€) - Positivo é Poupança | Negativo é Excesso', fontsize=12)
    ax.axvline(0, color='black', linewidth=1.5)
    ax.grid(axis='x', linestyle='--', alpha=0.4)

    # Adicionar os valores nas barras (Final Touch)
    for bar in bars:
        width = bar.get_width()
        label_x_pos = width if width > 0 else width - 1000
        ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{int(width)}€', 
                va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig("dashboard_trabalho_project.png")
    print("🚀 Dashboard guardado!")
    plt.show()

pmo_excel_visualizer()