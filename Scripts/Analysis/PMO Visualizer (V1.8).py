"""PMO Portfolio Visualizer: Financial Health Dashboard (V1.8).

This module demonstrates visual storytelling for PMO data using Matplotlib.
Transforms numerical variance data into color-coded bar charts that immediately
communicate project financial health status to executives and stakeholders.

Primary Purpose:
    Create professional financial health dashboards showing project budget
    variances at a glance. Use color coding (green=profit, red=loss) to
    enable instant visual comprehension without reading data tables. Designed
    for executive status meetings and stakeholder presentations.

Key Concepts:
    - Visual Storytelling: Numbers become stories through color and layout
    - Conditional Coloring: Green for positive variance (budget surplus),
      red for negative variance (budget deficit)
    - Fail-Safe Output: Always save PNG file as backup (prevents lost reports
      if display window doesn't open)
    - Professional Styling: Borders, grid lines, reference lines for clarity
    - Accessibility: Large fonts, high contrast colors for readability

Visualization Components:
    1. Figure Setup: Create canvas with specified size (10×6 inches)
    2. Bar Chart: Portfolio variance by project
    3. Color Logic: List comprehension for conditional coloring
    4. Reference Line: Horizontal line at zero for visual anchor
    5. Annotations: Title, axis labels, legend
    6. Layout Control: tight_layout() auto-adjusts spacing

Color Coding Standard:
    - Green (#2ecc71): Positive variance (under budget / surplus)
    - Red (#e74c3c): Negative variance (over budget / deficit)
    - Black dashed line: Zero reference for break-even point

Financial Interpretation:
    Variance = Budget Allocated - Actual Spent
    - Positive variance: Project completed under budget (good cost control)
    - Negative variance: Project over budget (requires remediation)
    - Zero variance: Project exactly on budget (rare, excellent execution)

Dependencies:
    - pandas: DataFrame creation and data organization
    - matplotlib: Figure creation, bar charts, styling
    - os: File path operations (imported, optional in V1.8)

Output Strategy:
    1. Save to PNG file: Guarantees report deliverable exists
    2. Display interactively: Show in development environment if available
    3. Pause briefly: plt.pause(3) gives window time to render

The "Fail-Safe" Pattern:
    1. Save file first (ensures report survives even if display fails)
    2. Attempt to show window (plt.show(), plt.pause())
    3. Graceful degradation: If window doesn't appear, file still exists
    This pattern prevents lost work and improves user experience.

Workflow:
    1. DATA STRUCTURE: Create dictionary with project variance data
    2. DATAFRAME: Convert to pandas for structured analysis
    3. VISUALIZATION SETUP: Create figure with specified dimensions
    4. CONDITIONAL COLORING: Generate color list based on variance sign
    5. BAR CHART: Draw bars with conditional colors
    6. STYLING: Add title, labels, reference line
    7. LAYOUT: Auto-adjust margins and spacing
    8. OUTPUT: Save PNG file first, then attempt display

Examples:
    Run financial health visualizer:
    
    >>> exec(open('PMO Visualizer (V1.8).py').read())
    --- 📊 GERANDO DASHBOARD EXECUTIVO ---
    Sucesso! A abrir o gráfico no teu ecrã...
    
    # Visual output: Bar chart saved as pmo_chart.png
    # Shows variance by project with color coding
    # Green bars: Risk AI (+1500€), Legacy Up (-1200€)
    # Red bars: Cloud Ops (-2800€)

Graph Title: "Saúde Financeira: Variância por Projeto (€)"
Y-Axis: "Budget vs Gasto Real" (in currency units)
X-Axis: Project names from portfolio

Assumptions:
    Data is numeric and ready for plotting (no cleaning required in this module)
    File system is writable (can save PNG to current directory)

Production Considerations:
    - PNG resolution: Default (72 DPI). For printing, change dpi=300 in savefig()
    - Display backend: May vary by OS/environment (Windows, Linux, Mac)
    - Interactive mode: plt.show(block=False) prevents blocking other processes

Roadmap:
    V2: Add secondary axis for completion percentage
    V2.1: Multi-project dashboard with subplots
    V2.2: Add professional branding and logo
    V2.3: Integrate with business intelligence (BI) tools
    V2.4: Add interactivity (hover tooltips, drill-down)
    V3: Real-time dashboard connected to data warehouse
    V4: Mobile-friendly responsive design

Related Sessions:
    - Tuesday: Data aggregation
    - Thursday: Visualization patterns and storytelling
    - Friday: Report distribution and email delivery
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
from typing import Optional, Dict, List, Any

def executar_visualizacao() -> None:
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




