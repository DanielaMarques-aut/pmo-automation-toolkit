import matplotlib.pyplot as plt
import pandas as pd
import os

# --- 1. CONFIGURATION & BACKEND FIX ---
# We force a common backend that works well with VS Code and Windows
try:
    plt.switch_backend('TkAgg') 
except Exception as e:
    print(f"Switching to default backend due to: {e}")

def generate_pmo_report():
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
