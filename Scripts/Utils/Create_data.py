"""Sample Project Task Data Generator

Generates a sample CSV file ('project_status.csv') containing 10 rows of project task data
with task IDs, names, status, budgets, and actual spending. Designed for testing and
demonstration of PMO data processing pipelines.

Features:
- Type-hinted data structures
- Automatic directory creation
- Append mode for repeated runs without data loss
- Audit-ready CSV format
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Any

# Sample data with mixed task statuses and budget variance
sample_data: Dict[str, List[Any]] = {
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


def save_audit_report(df_input: pd.DataFrame, folder_name: str = "data") -> None:
    """
    Create directory and save DataFrame to CSV file for audit purposes.

    Creates a 'data' directory (if not exists) and exports the input DataFrame to
    'project_status.csv'. Supports append mode for multiple runs without overwriting.

    Args:
        df_input: DataFrame containing project task data to be exported.
                  Must have columns: Task_ID, Task_Name, Status, Budget_Allocated, Actual_Spent
        folder_name: Directory to store output file. Default is 'data'.
                     Relative path from current working directory.

    Returns:
        None: Writes CSV file to disk with side effect.

    Output File:
        - Filename: project_status.csv
        - Location: data/ directory (created if missing)
        - Mode: Append (won't overwrite existing data)
        - Includes header only on first write

    Note:
        - Uses tight integration with pathlib.Path for cross-platform compatibility
        - Automatically creates parent directories with parents=True, exist_ok=True
        - Append mode preserves previous runs' data (useful for time-series audits)

    Example:
        >>> df = pd.DataFrame(sample_data)
        >>> save_audit_report(df)
        # Creates data/project_status.csv with header on first run
    """
    # Create 'data' directory with proper path handling
    output_dir: Path = Path.cwd() / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path: Path = output_dir / "project_status.csv"

    # Check if file exists to determine header mode
    file_exists: bool = file_path.exists()

    # Convert input data to DataFrame and export in append mode
    df: pd.DataFrame = df_input if isinstance(df_input, pd.DataFrame) else pd.DataFrame(df_input)
    df.to_csv(file_path, mode='a', index=False, header=not file_exists)

    print("Ficheiro 'project_status.csv' gerado com sucesso para auditoria.")


if __name__ == "__main__":
    """Execute data generation when script is run directly."""
    save_audit_report(pd.DataFrame(sample_data))