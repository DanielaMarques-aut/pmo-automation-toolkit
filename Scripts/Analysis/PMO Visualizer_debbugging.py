"""PMO Visualizer Debug Mode: Backend Configuration & Fallback Testing.

This module provides diagnostic capabilities for Matplotlib backend configuration
and display troubleshooting. Identifies incompatibilities between Matplotlib
and your system environment (Windows, Linux, Mac). Tests visualization pipeline
with automatic fallback to file-saving if interactive display unavailable.

Primary Purpose:
    Debug display issues when Matplotlib windows don't open in VS Code or
    other integrated development environments. Identify active graphics backend
    and test compatibility. Ensure reports are always saved to disk even if
    interactive visualization fails (fail-safe pattern).

Common Problems Addressed:
    - Matplotlib Window Won't Open:
      Cause: Wrong backend for environment (TkAgg vs Qt5Agg vs Agg)
      Solution: Test current backend, suggest alternatives
    
    - "RuntimeError: No module named 'tkinter'":
      Cause: TkAgg backend requires tk library (not installed)
      Solution: Install python-tk or conda tk package
    
    - Frozen VS Code on plt.show():
      Cause: Interactive mode conflicts with IDE
      Solution: Save PNG file as backup before attempting display
    
    - Report Lost if Display Fails:
      Cause: No file saved before display attempt
      Solution: Always save() before show()

Graphics Backends Explained:
    TkAgg:
    - Best for: Windows, Linux, Mac local development
    - Pros: Reliable, widely available, simple
    - Cons: Requires tkinter library
    
    Qt5Agg:
    - Best for: Advanced features, animations
    - Pros: Modern, feature-rich, non-blocking
    - Cons: Requires PyQt5 (heavier dependency)
    
    Agg:
    - Best for: Headless/server environments
    - Pros: No GUI dependencies, pure file rendering
    - Cons: Non-interactive (files only)
    
    WebAgg:
    - Best for: Web applications
    - Pros: Browser-based, networked
    - Cons: Complex setup

Backend Detection:
    matplotlib.get_backend() returns the active backend name
    Example outputs:
    - 'TkAgg' (ideal for development)
    - 'Qt5Agg' (feature-rich alternative)
    - 'Agg' (file-only, no display)
    - 'MacOSX' (macOS native)

Workflow:
    1. ENVIRONMENT DIAGNOSTIC: Detect current backend
    2. DATA CREATION: Generate sample PMO data
    3. VISUALIZATION: Attempt to create and display chart
    4. ERROR HANDLING: Catch display exceptions gracefully
    5. FALLBACK: Save PNG file as guaranteed deliverable
    6. FEEDBACK: Report success/failure to user

The Triple-Check Pattern (Fail-Safe):
    1. Try to show window (user sees chart immediately)
    2. Pause briefly (allow window to render)
    3. Save file (guarantee report exists)
    4. Check success and inform user
    
    This ensures: User gets visual feedback if possible,
    file report always available for email/printing

Expected Output on Successful Run:
    --- PMO Visualizer Debug Mode ---
    Current Graphics Backend: TkAgg
    [Chart window appears with bar chart]
    SUCCESS: Chart saved as 'pmo_chart_test2.png'
    Check your folder for the image file!

Expected Output on Failed Display:
    --- PMO Visualizer Debug Mode ---
    Current Graphics Backend: TkAgg
    Attempting to open chart window...
    [No window appears, but script continues]
    SUCCESS: Chart saved as 'pmo_chart_test2.png'
    Check your folder for the image file!
    --- Diagnostic Complete ---

Dependencies:
    - matplotlib: Figure creation, backend detection
    - pandas: Sample data creation
    - os: File path handling (imported but not heavily used)

Data Structure (Diagnostic):
    Minimal data for testing purposes:
    - Project A: 85% efficiency
    - Project B: 92% efficiency
    - Project C: 78% efficiency
    
    These values are intentionally simple for testing visualization,
    not realistic PMO data

Troubleshooting Guide:
    If chart window doesn't appear:
    
    Step 1: Check file saved successfully
    → Look for pmo_chart_test2.png in current folder
    → If found: Backend issue (file saving works)
    → If missing: Fundamental issue (investigate error message)
    
    Step 2: Try different backend
    → Edit script: plt.switch_backend('Qt5Agg')
    → Rerun script: does window appear now?
    
    Step 3: Install missing dependencies
    → For TkAgg: pip install tk (or apt-get install python3-tk)
    → For Qt5: pip install pyqt5
    
    Step 4: Check VS Code terminal settings
    → Some IDEs prevent GUI windows
    → Run script in native terminal instead of IDE

Examples:
    Run diagnostic to test Matplotlib display:
    
    >>> exec(open('PMO Visualizer_debbugging.py').read())
    --- PMO Visualizer Debug Mode ---
    Current Graphics Backend: TkAgg
    
    [Chart appears on screen]
    Attempting to open chart window...
    SUCCESS: Chart saved as 'pmo_chart_test2.png'
    Check your folder for the image file!
    
    --- Diagnostic Complete ---
    Press Enter to close this terminal...

Advanced Troubleshooting:
    Frozen/Hanging Script:
    - Problem: plt.show(block=True) blocks execution
    - Solution: Use plt.show(block=False) + plt.pause(3)
    - Why: block=False returns immediately, pause(3) gives time to render
    
    Multiple Windows Opening:
    - Problem: Script run multiple times, old windows still visible
    - Solution: Call plt.close('all') at start to clear previous figures
    - Implementation: Add to script: plt.close('all')
    
    Image Quality Issues:
    - Problem: Chart looks pixelated or blurry
    - Solution: Increase DPI: plt.savefig(file, dpi=300)
    - Trade-off: Higher DPI = larger file size

Roadmap:
    V1.1: Add backend auto-detection and suggestion
    V1.2: List available backends with installation instructions
    V2: Interactive diagnostic (menu to test different backends)
    V2.1: Automated environment report generation
    V3: Matplotlib configuration validator (checks all settings)

Environment Variables (Advanced):
    MPLBACKEND=Agg  (Force backend via environment variable)
    Example: MPLBACKEND=TkAgg python script.py
    Useful for: Server deployments, CI/CD pipelines

For Production Use:
    - Always use Agg backend on servers (headless)
    - Set explicit backend at script start (not just in try/except)
    - Document backend requirements in README
    - Test in target environment before deployment
    - Consider using different code paths for dev vs production

Related Modules:
    - PMO Visualizer (V1.8): Original visualization module
    - PMO Visualizer (V2): Dual-axis dashboard
    - Scripts/Utils/: Chart generation helpers with backend config
"""

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import os
from typing import Optional, Dict, List, Any

def run_debug() -> None:
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