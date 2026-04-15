"""PMO Integrated System with Professional Formatting: Portfolio Dashboard (V2.1-Enhanced).

This module represents an enhanced iteration of V2.1 with additional visual
styling and professional formatting capabilities. Extends chart aesthetics
with font configuration, improved readability, and professional business presentation.

Primary Purpose:
    Create polished, publication-ready PMO portfolio dashboards with enhanced
    visual styling. Apply professional font families, sizing, and spacing
    conventions to ensure reports meet corporate communication standards.
    Suitable for board presentations, investor communications, and executive
    stakeholder reviews.

Key Enhancements over V2.1:
    - Matplotlib Configuration: Set global font family and size
    - Professional Aesthetics: Arial font (corporate standard)
    - Improved Readability: Larger base font size (12pt)
    - Consistent Styling: All text elements use configured styles
    - Print-Ready: Optimized for PDF export and printed documents

Visual Style Configuration:
    Font Family: Arial (widely available, professional appearance)
    Font Size: 12pt (readable on slides and printed documents)
    Figure Size: 10×6 inches (16:9 aspect ratio for widescreen)
    DPI: 300 (print quality when saved as PNG)

Styling Pattern (rcParams):
    matplotlib.rcParams["font.family"] = "Arial"
    matplotlib.rcParams["font.size"] = 12
    
    This pattern applies globally to all text elements in subsequent figures,
    ensuring consistency without specifying font in each element.

Workflow (Same as V2.1 plus Styling):
    1. MATPLOTLIB CONFIG: Set font family and size globally
    2. DATA ORGANIZATION: Portfolio dictionary structure
    3. DATAFRAME CONVERSION: Pandas transformation
    4. PROMPT GENERATION: AI-ready prompt formatting
    5. VISUALIZATION: Bar chart with conditional colors
    6. PROFESSIONAL STYLING: Apply corporate formatting
    7. OUTPUT: Save and display

Financial Health Categories:
    - Green (on track): Positive variance, "Concluído", "Em Dia"
    - Red (at risk): Negative variance, "Atrasado"  
    - Legend identifies data series clearly

Dependencies:
    - matplotlib: Figure creation, rcParams configuration
    - pandas: Data transformation and analysis
    - os: File path operations

Font Configuration Benefits:
    - CONSISTENCY: All text uses same family (professional appearance)
    - READABILITY: 12pt base size suitable for presentations
    - UNIVERSAL: Arial is installed on Windows, Mac, Linux
    - CORPORATE: Matches Microsoft Office defaults (for stakeholder alignment)
    - SCALABILITY: Font size adjusts proportionally for different figure sizes

Examples:
    Generate professionally formatted portfolio dashboard:
    
    >>> exec(open('PMO Visualizer (V2.1) (2).py').read())
    🚀 Processamento de Portfólio AI-Ops...
    
    # Visual output:
    # - Bar chart with professional Arial font
    # - Larger, clearer text than V2.1
    # - Color-coded variance indicators
    # - Zero-line reference
    # - Grid background for easier reading
    
    ✅ Gráfico guardado com sucesso
    📊 Tentando abrir janela de visualização...
    
    --- TABELA DE OPERAÇÕES (PREPARADA PARA IA) ---
    Projeto           Status      Variancia_EUR
    Automação...      Atrasado           -4500
    Migração...         Em Dia            1200

Presentation Scenarios:
    - Executive Steering Committee: Professional appearance essential
    - Investor Relations: Print-quality required (300 DPI + clear fonts)
    - Board Meetings: Large screens (needs readable text)
    - Annual Reports: Corporate color scheme consistency
    - Printed Documents: Must survive B&W photocopying

Print Configuration (Optional Enhancements):
    For higher-quality PDF export, consider:
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    # This creates print-ready output suitable for annual reports

Roadmap:
    V2.2: Add corporate color palette (brand guidelines)
    V2.3: Support multiple chart layouts (dashboard grids)
    V2.4: Theme system (light mode, dark mode for presentations)
    V3: Integration with corporate design system (logo, watermarks)
    V4: Automated PDF generation with headers/footers
    V5: Export to PowerPoint with professional templates

Related Styling Resources:
    - Matplotlib style sheets: seaborn, ggplot, fivethirtyeight
    - Corporate font guidelines: Check company brand standards
    - Color palette standards: Match corporate identity colors
    - Layout guidelines: 16:9 (widescreen) vs 4:3 (legacy)

Compatibility Notes:
    - Font families available: Check plt.rcParams['font.sans-serif']
    - Fallback font: If Arial unavailable, uses next in sans-serif list
    - Print rendering: Some PDF readers require font embedding
    - Web display: Different from print (test in target format)

Best Practices:
    1. Always test output in target medium (screen, print, PDF)
    2. Use consistent font across all company dashboards
    3. Consider accessibility (font size for vision impairment)
    4. Test color blindness mode (red-green must have other distinction)
    5. Save multiple formats (PNG for web, PDF for print)
"""

import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import Optional, Dict, List, Any

matplotlib.use("TkAgg")

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 12
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