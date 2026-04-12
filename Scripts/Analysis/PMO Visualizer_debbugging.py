import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import os

def run_debug():
    print("--- PMO Visualizer Debug Mode ---")
    
    # 1. Check which 'backend' Matplotlib is using
    # On Windows, it should usually be 'TkAgg' or 'Qt5Agg'
    current_backend = matplotlib.get_backend()
    print(f"Current Graphics Backend: {current_backend}")

    # 2. Create sample PMO data
    data = {
        'Project': ['Project A', 'Project B', 'Project C'],
        'Efficiency': [85, 92, 78]
    }
    df = pd.DataFrame(data)

    try:
        # 3. Force a standard interactive backend if yours is broken
        # If this fails, the script will catch the error below
        plt.figure(figsize=(8, 5))
        plt.bar(df['Project'], df['Efficiency'], color='skyblue')
        plt.title('PMO Debug Test - Efficiency')
        plt.ylabel('Score (%)')

        print("Attempting to open chart window...")
        
        # This is the line that usually triggers the window
        plt.show(block=False) 
        plt.pause(3) # Give it 3 seconds to appear
        
        # 4. FALLBACK: Save to file
        # If the window isn't showing, we will save it so you can see the result
        output_path = "pmo_chart_test2.png"
        plt.savefig(output_path)
        print(f"SUCCESS: Chart saved as '{output_path}' in your folder.")
        print("Check your folder for the image file!")

    except Exception as e:
        print(f"ERROR encountered: {e}")
    
    print("\n--- Diagnostic Complete ---")
    input("Press Enter to close this terminal...")
run_debug ()