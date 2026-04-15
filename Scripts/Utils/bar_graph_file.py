from typing import Dict
import matplotlib.pyplot as plt
import os

def generate_budget_chart(data: Dict[str, float], output_path: str) -> str:
    """
    Generate a professional bar chart for PMO budget reporting.
    
    Saves a chart to disk and displays it with value labels on top of each bar.
    The function handles figure cleanup to prevent matplotlib conflicts in 
    interactive environments.
    
    Args:
        data: Dictionary mapping department names to budget values in euros.
              Example: {'IT': 66500.0, 'Data': 18000.0}
        output_path: Absolute or relative path where the PNG chart will be saved.
                     Parent directories are created if they don't exist.
    
    Returns:
        str: The output_path parameter (useful for chaining operations).
    
    Raises:
        OSError: If parent directories cannot be created.
        Exception: If matplotlib cannot save the figure.
    
    Example:
        >>> budget_data = {'IT': 66500, 'Data': 18000, 'Product': 45000}
        >>> path = generate_budget_chart(budget_data, 'outputs/budget.png')
        >>> print(path)
        'outputs/budget.png'
    """
    # Programming Bases: Limpar figuras anteriores para evitar sobreposição
    if plt.get_fignums():
         plt.clf() # Limpa a figura atual para evitar sobreposição de gráficos anteriores
    
    departments = list(data.keys())
    budgets = list(data.values())

    # Estilização Corporativa
    plt.figure(figsize=(10, 6))
    bars = plt.bar(departments, budgets, color='#2E86C1')
    
    plt.title('Distribuição de Orçamento por Departamento', fontsize=14)
    plt.xlabel('Departamento', fontsize=12)
    plt.ylabel('Valor (€)', fontsize=12)
    
    # Adicionar labels no topo de cada barra (Visual Clarity)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 500, f'{yval:,.0f}€', ha='center', va='bottom')

    # Fail-Fast: Garantir que a pasta de destino existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.savefig(output_path)  # Guardar o gráfico
    plt.show()  # Mostrar uma única vez
    plt.close()  # Fechar a figura para liberar memória
    return output_path