# PROJECT: PMO Visualizer (V1.8).py
# GOAL: Transform Numbers into Decisions (Visual storytelling)
# AUTHOR: Daniela Marques | DATE: Thursday, March 5th, 2026

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

def executar_visualizacao():
    print("--- 📊 GERANDO DASHBOARD EXECUTIVO ---")
    
    # 1. Dados (Recuperados da nossa lógica de V1.5)
    data = {
        'Projeto': ['Risk AI', 'Cloud Ops', 'Digital Ops', 'Legacy Up'],
        'Variancia': [1500, -2800, 500, -1200]
    }
    df = pd.DataFrame(data)

    # 2. CRIAR O GRÁFICO
    # Criamos a área do gráfico
    plt.figure(figsize=(10, 6))
    
    # Lógica de Cores: Verde para positivo, Vermelho para negativo
    # Isto é Python básico: "Cria uma lista de cores baseada na Variancia"
    cores = ['#2ecc71' if x > 0 else '#e74c3c' for x in df['Variancia']]
    
    # Desenhar as barras
    plt.bar(df['Projeto'], df['Variancia'], color=cores)

    # Personalização (Storytelling)
    plt.title('Saúde Financeira: Variância por Projeto (€)', fontsize=14, fontweight='bold')
    plt.xlabel('Projetos do Portfólio', fontsize=12)
    plt.ylabel('Budget vs Gasto Real', fontsize=12)
    
    # Linha de referência no zero
    plt.axhline(0, color='black', linewidth=1, linestyle='--')

    # 3. OUTPUT
    print("Sucesso! A abrir o gráfico no teu ecrã...")
    plt.tight_layout() # Ajusta as margens automaticamente
    plt.show(block = False)
    plt.pause(3)  # O comando que faz a janela aparecer
output_path = "pmo_chart.png"
plt.savefig(output_path)


executar_visualizacao()




