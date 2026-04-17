"""
Title: Final Report Exporter
Principle: Single Responsibility. This module only handles file output.
"""
from datetime import datetime
import os

def save_executive_summary(content: str, folder: str = "Data/Output/ReportsAi") -> str:
    """

    Saves a generated AI executive summary to a timestamped text file.

    This function follows the Fail-Fast principle by ensuring the destination 
    directory exists before attempting I/O operations. It standardizes report 
    naming conventions for automated risk tracking.

    Args:
        content (str): The raw text or Markdown content of the executive report.
        folder (str): The target directory path. Defaults to "Data/Output/ReportsAi".

    Returns:
        str: The absolute or relative path to the newly created report file.

    Raises:
        OSError: If the directory cannot be created or the file is not writable.
    
    Principle: Fail-Fast - Checks if folder exists.
    """
    #Verify if the folder exists, if not create it. This ensures that the function doesn't fail when trying to save the file. It adheres to the principle of Fail-Fast by checking for potential issues early on.
    os.makedirs(folder, exist_ok=True)
    timestamp: str = datetime.now().strftime("%Y%m%d_%H%M")
    file_path: str = f"{folder}/summary_{timestamp}.txt"
 # writes the report content to a file with a timestamped name in the specified folder. It ensures the folder exists and returns the path to the saved file.   
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"--- PMO EXECUTIVE REPORT | {datetime.now()} ---\n")
        f.write(content)
    
    return file_path