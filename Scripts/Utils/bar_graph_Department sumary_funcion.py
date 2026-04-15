
from matplotlib import pyplot as plt
from typing import Dict


def create_department_summary_chart(dept_summary: Dict[str, float], output_file: str = 'dept_summary_chart.png') -> None:
    """
    Generate a horizontal bar chart showing operational load distribution by department.
    
    Creates a professional bar chart with departments sorted by load/budget in ascending
    order. Horizontal orientation facilitates reading long department names. Chart is
    saved to disk without displaying in interactive environments to prevent workflow
    interruption.
    
    Args:
        dept_summary: Dictionary mapping department names to their load/budget values.
                      Example: {'IT': 66500.0, 'Data': 18000.0, 'Product': 45000.0}
        output_file: Filename for the PNG chart (without path). Chart is saved to
                     Data/output/ directory. Default is 'dept_summary_chart.png'.
    
    Returns:
        None: Side effect is creating and saving a PNG file to disk.
    
    Raises:
        FileNotFoundError: If Data/output/ directory does not exist.
        ValueError: If dept_summary is empty (fails silently with empty chart).
        Exception: If matplotlib cannot write to the specified path.
    
    Note:
        - Uses barh (horizontal bars) for better readability of department names
        - Automatically sorts departments by value for consistent visualization
        - Data labels are added on each bar for precise value reading
        - tight_layout() prevents label truncation
    
    Example:
        >>> summary = {'IT': 66500, 'Data': 18000, 'Product': 45000}
        >>> create_department_summary_chart(summary, 'budget_dist.png')
        ✅ Gráfico salvo como Data/output/budget_dist.png
    """
    
    # Ordenação dos dados: Essencial para uma leitura rápida de Ops/PMO
    # Transformamos o dicionário numa lista de tuplos ordenada pelo valor (item[1])
    sorted_items: list[tuple[str, float]] = sorted(dept_summary.items(), key=lambda item: item[1])
    departments: list[str] = [item[0] for item in sorted_items]
    values: list[float] = [item[1] for item in sorted_items]

    # Substituição do .figure() por subplots para maior controlo (Standard Profissional)
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Gráfico de barras horizontais (barh) facilita a leitura de nomes de departamentos longos
    bars = ax.barh(departments, values, color='#2c3e50')
    
    # Customização técnica para Business Ops
    ax.set_title('Distribuição de Carga Operacional por Departamento', fontsize=14, fontweight='bold')
    ax.set_xlabel('Volume de Tarefas / Budget', fontsize=12)
    ax.set_ylabel('Departamento', fontsize=12)
    
    # Adiciona etiquetas de dados para evitar ambiguidade
    ax.bar_label(bars, padding=3)
    
    # Previne o corte de labels (labels truncation)
    plt.tight_layout()
    
    # Guardar o ficheiro (Sem usar plt.show() para evitar interrupções no workflow)
    plt.savefig(f"Data/output/{output_file}")
    print(f"✅ Gráfico salvo como Data/output/{output_file}")
    plt.close()  # Fechar a figura para liberar memória