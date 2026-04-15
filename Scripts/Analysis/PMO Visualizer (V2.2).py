"""PMO Multi-Plot Dashboard with Interactive User Input (V2.2).

This module introduces user interactivity to the PMO reporting system. Enables
dynamic portfolio configuration through console prompts, allowing stakeholders
to customize dashboard inputs without code modification. Demonstrates dual-plot
layouts (side-by-side comparisons) suitable for comparative analysis.

Primary Purpose:
    Create customizable PMO portfolio dashboard allowing real-time project
    addition via console input. Generate professional multi-plot layouts
    comparing financial health (budget variance) with schedule performance
    (completion percentage). Enable ad-hoc reporting without template changes.

Key Enhancements:
    - Interactive Input: User can add projects dynamically
    - Multi-Plot Layout: Side-by-side bar charts for comparison
    - Excel Export: Save portfolio data for further analysis
    - Flexible Dashboard: Same visualization code, different data inputs
    - Professional Styling: Color-coded health status, clear legends

User Interaction Pattern:
    Prompt: "Deseja adicionar mais projetos? Y/N: "
    User Input: Y → Request project details (ID, Name, Budget, Completion)
    Data Capture: Append to portfolio dictionary
    Loop: Repeat until user enters N
    Export: Save all projects to Excel

Two Subplot Layout:
    - Left Plot: Budget Status (bars, negative=red, positive=green)
    - Right Plot: Completion Percentage (bars, blue color)
    - Both: Show same projects for easy comparison

Graph 1 - Budget Variance:
    Type: Vertical bar chart
    Y-Axis: Budget Status in EUR (negative=overspend, positive=savings)
    Color: Red for negative (risk), green for positive (safe)
    Reference: Zero-line (axhline) shows break-even point
    Purpose: Quick identification of over-budget projects

Graph 2 - Completion Progress:
    Type: Horizontal bar chart (shows project name clearly)
    X-Axis: Completion percentage (0-100%)
    Color: All bars blue (progress state)
    Reference: 100% marked on x-axis for clear target
    Purpose: Visual comparison of schedule progress

Dependencies:
    - matplotlib: Figure creation, subplot management, bar charts
    - pandas: DataFrame creation and Excel export
    - os: File path operations

Typical Use Case:
    Friday status meeting where PM updates portfolio:
    1. Script starts, shows initial 4 projects
    2. PM says "Y" to add more
    3. Script prompts for new project details
    4. PM enters: PRJ-005, "Risk Mitigation", €8000, 75%
    5. Dashboard regenerates with new project included
    6. Chart saved to Dashboard.png for presentation

Initial Portfolio (Predefined):
    - PRJ-001: AI Integration (-€1500 over budget, 90% complete)
    - PRJ-002: Cloud Migration (+€2500 savings, 45% complete)
    - PRJ-003: Security Audit (-€800 over budget, 15% complete)
    - PRJ-004: Legacy Sync (+€4200 savings, 60% complete)

Examples:
    Run interactive dashboard builder:
    
    >>> exec(open('PMO Visualizer (V2.2).py').read())
    # Initial 4 projects displayed
    # Prompts: "Deseja adicionar mais projetos? Y/N: "
    # User enters Y
    # Prompts: "Enter Project ID: "
    # ... (collect all project details)
    # Prompts: "Deseja adicionar mais projetos? Y/N: "
    # User enters N
    # Dashboard created with all projects
    🚀 Dashboard saved as 'Dashboard.png'

Excel Export Format:
    File: pmo_portfolio.xlsx
    Columns: Project_ID, Name, Budget_Status, Completion_Pct
    Use For: Further analysis, historical tracking, audit trails

Input Validation Strategy:
    - Project ID: Free text (no validation, accept any string)
    - Name: Free text (project description)
    - Budget: Integer input, expects currency (EUR assumed)
    - Completion: Integer input, 0-100% range (no validation enforced)

Note on Input Validation:
    V2.2 has minimal validation for teaching purposes. In production,
    add validation for: numeric fields, percentage ranges, duplicate IDs.

Workflow:
    1. INITIAL DATA: Create 4-project baseline portfolio
    2. USER INTERACTION: Prompt for additional projects
    3. DATA APPEND: Add new projects to dictionary lists
    4. LOOP CONTROL: Repeat prompts until user opts out
    5. DATAFRAME: Convert final portfolio to pandas
    6. EXCEL EXPORT: Save portfolio for record-keeping
    7. VISUALIZATION: Generate dual-plot dashboard
    8. OUTPUT: Save PNG and display

Roadmap:
    V2.3: Input validation (numeric ranges, ID uniqueness)
    V2.4: Data persistence (read existing portfolio from file)
    V3: Database backend (allow historical comparison)
    V3.1: Drag-drop chart interaction (click project to edit)
    V4: Web dashboard (Flask/Django for browser access)
    V4.1: Real-time updates from project management system

Limitations:
    - Console input only (no GUI dialogs)
    - Portfolio discarded on script exit (use Excel export for persistence)
    - No error recovery (invalid input causes script failure)
    - Simple layout only (advanced features in V3+)

Production Considerations:
    - For enterprise use: Add database persistence layer
    - For remote teams: Convert to web application
    - For daily automation: Schedule script runs with pre-loaded data
    - For compliance: Add audit logging of all portfolio changes
"""

from csv import excel
import json
import matplotlib.pyplot as plt
import pandas as pd
from typing import Optional, Dict, List, Any

def graph_lab() -> None:
    # 1. THE DATA (Advanced Dictionary Structure)
    # This mimics a real  database
    pmo_portfolio = {
        'Project_ID': ['PRJ-001', 'PRJ-002', 'PRJ-003', 'PRJ-004'],
        'Name': ['AI Integration', 'Cloud Migration', 'Security Audit', 'Legacy Sync'],
        'Budget_Status': [-1500, 2500, -800, 4200],  # Negative is over-budget
        'Completion_Pct': [90, 45, 15, 60]
    }

    add_more = input("Deseja adicionar mais projetos? Y/N: ")
    while add_more.upper() == 'Y':
        project_id = input("Enter Project ID: ")
        name = input(" What's the Project Name: ")
        budget_status = int(input("Budget Status (€): "))
        completion_pct = int(input("Completion Percentage (%): "))
        
        pmo_portfolio['Project_ID'].append(project_id)
        pmo_portfolio['Name'].append(name)
        pmo_portfolio['Budget_Status'].append(budget_status)
        pmo_portfolio['Completion_Pct'].append(completion_pct)
        
        add_more = input("Deseja adicionar mais projetos? Y/N: ")
    df = pd.DataFrame(pmo_portfolio)
    df.to_excel("pmo_portfolio.xlsx", index=False)
   
    # 2. CREATE A MULTI-PLOT DASHBOARD 
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Graph 1: Financial Health (Bars)
    colors = ['red' if x < 0 else 'green' for x in df['Budget_Status']]
    ax1.bar(df['Name'], df['Budget_Status'], color=colors)
    ax1.set_title('Budget Variance (€)')
    ax1.axhline(0, color='black', linewidth=1)

    # Graph 2: Progress vs Target (Horizontal Bars)
    ax2.barh(df['Name'], df['Completion_Pct'], color='skyblue')
    ax2.set_title('Completion Percentage (%)')
    ax2.set_xlim(0, 100)

    plt.suptitle('PMO EXECUTIVE DASHBOARD - WEEK 2 REVIEW', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save & Show
    plt.savefig("Dashboard.png")
    print("🚀 Dashboard saved as 'Dashboard.png'")
    plt.show()
graph_lab()
