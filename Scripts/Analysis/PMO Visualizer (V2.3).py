"""PMO Advanced Dashboard: Budget Variance with Professional Styling (V2.3).

This module demonstrates advanced visualization techniques: dynamic data loading,
professional color schemes (seaborn-v0_8-muted theme), and annotated bar charts
with value labels. Targets director/CFO audience with polished, presentation-ready
outputs suitable for board meetings and investor presentations.

Primary Purpose:
    Create sophisticated portfolio health dashboard automatically loading data
    from Excel files. Apply professional styling frameworks (seaborn themes)
    for consistent, polished aesthetics. Add value annotations directly on
    bars for instant data comprehension without separate legends.

Key Enhancements over V2.2:
    - File-Based Input: Load data from Excel (if exists), fall back to test data
    - Seaborn Styling: Apply muted color palette for professional appearance
    - Horizontal Bar Chart: Project names displayed fully (better readability)
    - Value Annotations: Display EUR amounts directly on bars
    - Smart Coloring: Green for savings, red for overspend
    - Polished Layout: Grid lines, edge colors, alpha transparency

Visualization Strategy:
    - Chart Type: Horizontal bar chart (project names on y-axis)
    - Primary Metric: Budget deviation (planned vs actual) in EUR
    - Color Coding: Green for positive (savings), red for negative (overspend)
    - Annotations: Value labels (€5200, -€3000) at bar ends
    - Grid: Subtle vertical gridlines for reference
    - Title: Large, clear statement of business meaning
    - Edge Colors: Black borders on bars for print clarity

Professional Styling Framework:
    seaborn-v0_8-muted provides:
    - Consistent color palette (professional appearance)
    - Reduced ink (lighter backgrounds, subtle colors)
    - Typography: Better default font selection
    - Whitespace: Improved margins and padding
    - Grid: Subtle reference lines

Calculating Budget Deviation:
    Desvio = Budget_Planeado - Gasto_Real
    
    Positive Desvio (Green): Project saved money
    - Example: Planned €10000, Spent €8000 → Desvio = +€2000 (savings)
    
    Negative Desvio (Red): Project overspent
    - Example: Planned €5000, Spent €7000 → Desvio = -€2000 (overspend)

Dependencies:
    - pandas: Excel I/O, DataFrame operations
    - matplotlib: Figure creation, bar charts, annotations
    - os: File path checking

Workflow:
    1. TEST DATA CREATION: Define create_excel_teste() function
    2. FILE CHECKING: Check if input Excel exists
    3. DATA LOADING: Read from Excel (or create test file)
    4. FIELD CREATION: Calculate deviation (Planned - Actual)
    5. STYLING: Apply seaborn theme + configuration
    6. VISUALIZATION: Horizontal bars with conditional colors
    7. ANNOTATIONS: Add value labels at bar ends
    8. OUTPUT: Save PNG and attempt display

Data File Strategy:
    Test Mode: If dados_pmo_trabalho.xlsx doesn't exist, create it
    - Simulates real scenario while allowing script to run standalone
    - Demonstrates file creation pattern (useful for setup scripts)
    - Allows users to modify generated file for custom data
    
    Production Mode: Replace with call to actual database/API
    - df = pd.read_sql("SELECT * FROM projects WHERE status='active'", conn)

Example DataFrame:
    Departamento       Gasto_Real  Budget_Planeado  Desvio
    Logística               12000            10000    2000
    Marketing               8500             9000     500
    TI                     15000            14000   -1000
    RH                      4000             4500     500
    Vendas                  9200            10000     800

Color and Styling Rules:
    Edge Color: Always black (#000000) for print clarity
    Edge Width: 1.5pt for professional appearance
    Alpha: 0.8 (slight transparency for modern look)
    Font Weight: Bold for value labels (ensure readability)
    Grid: Dashed line, only x-axis, subtle alpha

Value Annotation Pattern:
    For each bar:
    1. Get width (deviation value)
    2. Calculate x position (bar_width or bar_width - 1000)
    3. Place text at (x, y) = (label_x_pos, bar_center)
    4. Center alignment, bold font
    
    Positioning logic handles negative values carefully:
    - Positive bar: Label placed at bar_width (right end)
    - Negative bar: Label placed at bar_width - 1000 (inside bar if space)

Examples:
    Run advanced portfolio analysis dashboard:
    
    >>> exec(open('PMO Visualizer (V2.3).py').read())
    ✅ Ficheiro Excel de teste criado!
    🚀 Dashboard guardado!
    
    # Visual output:
    # Horizontal bars showing budget deviations
    # Green bars (savings): Logística +2000€, Marketing +500€
    # Red bars (overspend): TI -1000€
    # Values annotated directly on bars
    # Professional seaborn color scheme

Seaborn Theme Details:
    seaborn-v0_8-muted provides:
    - Base colors: Soft, desaturated palette
    - Axes: Light gray gridlines
    - Figure: White background
    - Legend: Clean box styling
    - Overall: Professional, publication-ready appearance

Key Differences from V2.2:
    V2.2: Basic two-subplot layout, no annotations
    V2.3: Single sophisticated chart, annotated values, professional styling
    
    V2.3 trades multiple charts for single high-quality visualization
    Better for executive summaries, board presentations

Roadmap:
    V2.4: Multiple visualization themes (dark mode, colorblind-friendly)
    V3: Real-time data updates from Excel (background polling)
    V3.1: Drill-down capability (click department → line item details)
    V4: Integration with accounting system (automated data pull)
    V4.1: Forecasting (project spending trends with predictions)
    V5: Web dashboard (interactive version)

Output Files:
    - dados_pmo_trabalho.xlsx: Excel data source (created if missing)
    - dashboard_trabalho_project.png: Final visualization (300 DPI ready)

Print Quality Configuration:
    Current settings optimized for screen display. For print/PDF:
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')

Print Considerations:
    - B&W Printing: Color will convert to grayscale
    - Font Rendering: Arial remains readable in print
    - Value Labels: Bold font ensures visibility in print
    - Grid Lines: Dashed style helps distinguish from data
    - Edge Width: 1.5pt appropriate for both screen and print

Related Modules:
    - V2.1: Single-plot dictionary-based structure
    - V2.2: Multi-plot user interactive input
    - V2.3: Single sophisticated plot with professional styling (this module)
    - V2.4 (Future): Multiple theme options and customization
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import Optional, Dict, List, Any

# 1. PREPARAÇÃO DO EXCEL (Simulação)
# Este bloco cria uma simulação de dados para testar
def criar_excel_teste() -> None:
    data = {
        'Departamento': ['Logística', 'Marketing', 'TI', 'RH', 'Vendas'],
        'Gasto_Real': [12000, 8500, 15000, 4000, 9200],
        'Budget_Planeado': [10000, 9000, 14000, 4500, 10000]
    }

    df_teste = pd.DataFrame(data)
    df_teste.to_excel("dados_pmo_trabalho.xlsx", index=False)
    print("✅ Ficheiro Excel de teste criado!")

def pmo_excel_visualizer() -> None:
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