"""
Title: Final Report Exporter
Principle: Single Responsibility. This module only handles file output.
"""
from datetime import datetime
import os

def save_executive_summary(content: str, folder: str = "Data/Output/ReportsAi") -> str:
    """
    Saves the AI insight into a timestamped file.
    Principle: Fail-Fast - Checks if folder exists.
    """
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    file_path = f"{folder}/summary_{timestamp}.txt"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"--- PMO EXECUTIVE REPORT | {datetime.now()} ---\n")
        f.write(content)
    
    return file_path