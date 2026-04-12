import pandas as pd
from pathlib import Path
from typing import Dict, List, Any

# This script generates a sample CSV file named 'project_status.csv' with 10 rows of project task data.
# 1. Using type hints in a data dictionary
# This says: "The keys are strings, and the values are lists containing anything."
data: Dict[str, List[Any]] = {
    'Task_ID': ['T001', 'T002', 'T003', 'T004', 'T005', 'T006', 'T007', 'T008', 'T009', 'T010'],       
    'Task_Name': [
        'Project Charter and Kickoff', 'Stakeholder Analysis', 'Market Research',
        'Database Schema Design', 'Frontend Framework Setup', 'API Integration Development',
        'Security Vulnerability Audit', 'User Interface Testing', 'Drafting Technical Manuals',        
        'Cloud Infrastructure Setup'
    ],
    'Status': [
        'Completed', 'Completed', 'In Progress', 'Delayed', 'In Progress',
        'Delayed', 'In Progress', 'In Progress', 'In Progress', 'In Progress'
    ],
    'Budget_Allocated': [1500, 2000, 5000, 3500, 6000, 8000, 4500, 3000, 2500, 5000],
    'Actual_Spent': [1450, 2000, 3200, 4100, 2500, 9200, 1200, 500, 0, 1500]
}
# 2. Creating a function with type hints
# 'df_input' must be a DataFrame. The function returns 'None'.
def save_audit_report(df_input: pd.DataFrame, folder_name: str = "data") -> None:
    """Creates directory and saves the DataFrame to CSV."""
    # 1. Use lowercase for variables (clean code principle)
    # 2. Ensure the 'data' directory exists
    output_dir: Path = Path.cwd() / "data"
    output_dir.mkdir(parents=True, exist_ok=True) 
    file_path: Path = output_dir / "project_status.csv"
    # Logic for header
    file_exists: bool = file_path.exists()
    # We use pandas to create a DataFrame and then export it to a CSV file in the current working directory.
    df: pd.DataFrame = pd.DataFrame(data)
    # 3. Export the DataFrame to CSV, appending if the file already exists (useful for testing multiple runs without overwriting)
    df.to_csv(file_path, mode='a', index=False, header=not file_exists)
    print("Ficheiro 'project_status.csv' gerado com sucesso para auditoria.")
 # 4. Run the function to create the CSV file
if __name__ == "__main__":
    save_audit_report(pd.DataFrame(data))