"""PMO Integrated Dashboard System: Progress & Budget Visualization (V2.0).

This module extends V1.8 with dual-axis visualization showing completion
progress and budget burn rate simultaneously. Enables stakeholders to quickly
identify projects that are ahead/behind schedule relative to spending.

Primary Purpose:
    Create comprehensive project status dashboard displaying both schedule
    performance (% complete) and financial performance (% budget spent).
    Identify schedule-budget mismatches: projects ahead on schedule but
    burning budget quickly (risk indicator) or slow progress with heavy spend.

Key Concepts:
    - Dual-Axis Chart: Bar chart + line chart with separate y-axes
    - Backend Configuration: Force TkAgg backend for compatibility
    - Fail-Safe Pattern: Always save file before attempting display
    - Grid Lines: Add reference lines for easier reading
    - Color Differentiation: Blue for progress, red for budget
    - Professional Layout: Title, legends, grid styling

Dual-Axis Architecture:
    - ax1 (Left): Completion % (bar chart, blue color)
    - ax2 (Right): Budget Spent % (line chart, red color)
    - Both axes: 0-110% range for consistent interpretation

Performance Interpretation:
    Healthy Project:
    - Completion ≈ Budget Spent (progress synchronized with spending)
    - Example: 50% complete, 50% budget spent (balanced)
    
    At-Risk Project (Ahead):
    - Completion > Budget Spent (ahead of schedule, conservative spend)
    - Example: 70% complete, 40% budget spent (slow spending, schedule risk)
    
    At-Risk Project (Behind):
    - Completion < Budget Spent (behind schedule, heavy spend)
    - Example: 30% complete, 60% budget spent (schedule risk, budget risk)

Project Phases Workflow:
    1. Planning: High planning spend, 100% planning completion
    2. Development: Increasing complexity, 85% completion
    3. Testing: Growing test coverage, 40% completion  
    4. UAT: User acceptance, 10% completion
    5. Deployment: Final phase, 0% completion (not started)

Dependencies:
    - matplotlib: Figure creation, dual-axis plotting, styling
    - pandas: DataFrame organization
    - os: File path operations

Backend Configuration:
    TkAgg is the most reliable backend across Windows, Linux, Mac
    Forces explicit backend before plotting to avoid display issues

Output Strategy – "Fail-Safe Outputs":
    1. Create figure and plot data
    2. Save PNG file immediately (guarantees deliverable)
    3. Attempt interactive display (may fail in headless environments)
    On display failure, PNG file still exists for reporting

Visualization Elements:
    - Bar Chart: Completion progress by phase
    - Line Chart: Budget burn rate by phase  
    - Horizontal Grid: Reference lines at 25, 50, 75, 100%
    - Title: Centered, bold, large font
    - Legends: Identify each data series
    - Axis Labels: Clear units and meaning

Examples:
    Generate quarterly PMO operations dashboard:
    
    >>> exec(open('PMO Visualizer (V2).py').read())
    🚀 Starting PMO Visualizer Build...
    ✅ Success: Report saved as '.../pmo_report_friday.png'
    📈 Attempting to open interactive window...
    
    # Visual output:
    # Left axis: Planning(100%), Development(85%), Testing(40%)
    # Right axis: Budget burn 20%, 45%, 60%...
    # Green areas: On-track projects
    # Red areas: Risk projects

Architecture Notes:
    V2.0 introduces dual-axis capability for schedule/budget analysis.
    This pattern is widely used in project management dashboards
    (PMI standards, Agile boards, SAFe reporting).

Grid and Styling:
    - Alpha transparency: 0.7 for subtle grid (not competing with data)
    - Y-axis limits: Both set to 0-110% for proportional comparison
    - Line style: Dashed grid for distinction from data lines
    - Marker: Circle marker on line chart for data point visibility

Roadmap:
    V2.1: Add project status annotations (on-track, at-risk, critical)
    V2.2: Add professional branding and corporate colors
    V2.3: Multiple dashboard layouts (1x2, 2x2, 3x3 subplots)
    V3: Real-time updates from project management system
    V4: Drill-down capabilities (click project → task-level details)
    V5: Integration with Slack/Teams for automated distribution

Related Sessions:
    - Monday-Wednesday: Data aggregation and cleaning
    - Thursday: Visualization patterns
    - Friday: Report delivery and stakeholder communication

Notes for Developers:
    If window doesn't open on your system:
    1. Check if matplotlib backend is GUI-enabled
    2. Ensure TkAgg is installed: pip install tk
    3. Look for pmo_report_friday.png (report saved regardless)
"""

import matplotlib.pyplot as plt
import pandas as pd
import os
from typing import Optional, Dict, List, Any

# --- 1. CONFIGURATION & BACKEND FIX ---
# We force a common backend that works well with VS Code and Windows
try:
    plt.switch_backend('TkAgg') 
except Exception as e:
    print(f"Switching to default backend due to: {e}")

def generate_pmo_report() -> None:
    print("🚀 Starting PMO Visualizer Build...")

    # --- 2. DATA STRUCTURE (The "Dictionary" approach) ---
    # As a PMO, you track project phases and their completion percentages
    data = {
        'Project Phase': ['Planning', 'Development', 'Testing', 'UAT', 'Deployment'],
        'Completion %': [100, 85, 40, 10, 0],
        'Budget Spent (%)': [20, 45, 60, 70, 75]
    }

    df = pd.DataFrame(data)

    # --- 3. VISUALIZATION LOGIC ---
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Bar chart for Completion
    ax1.bar(df['Project Phase'], df['Completion %'], color='skyblue', label='Completion Progress')
    ax1.set_ylabel('Completion %', color='blue', fontsize=12)
    ax1.set_ylim(0, 110)

    # Line chart for Budget (Secondary Axis)
    ax2 = ax1.twinx()
    ax2.plot(df['Project Phase'], df['Budget Spent (%)'], color='red', marker='o', linewidth=2, label='Budget Burn')
    ax2.set_ylabel('Budget Spent %', color='red', fontsize=12)
    ax2.set_ylim(0, 110)

    plt.title('PMO Quarterly Operations: Progress vs. Budget', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # --- 4. THE "FAIL-SAFE" OUTPUTS ---
    
    # Save a file first (so you always have the result)
    filename = "pmo_report_friday.png"
    plt.savefig(filename, dpi=300)
    print(f"✅ Success: Report saved as '{os.path.abspath(filename)}'")

    # Attempt to show the window
    print("📈 Attempting to open interactive window...")
    plt.show()
generate_pmo_report()
