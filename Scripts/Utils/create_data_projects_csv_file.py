"""Sample Project Data CSV Generator

Creates a dummy 'projects.csv' file with sample project data for testing and
demonstration purposes. Includes projects across multiple departments with
various statuses and budget allocations.

This script is useful for:
- Testing ETL pipelines without real data
- Demonstrating PMO reporting functionality
- Creating reproducible test scenarios
"""

import csv
from typing import List, List

def create_projects_csv() -> None:
    """
    Generate sample projects.csv file with dummy project data.

    Creates a CSV file containing 7 sample projects across IT, Product, Marketing,
    Security, and Data departments. Each row includes ProjectName, Deadline, Status,
    Manager, Budget, and Department.

    Returns:
        None: Writes 'projects.csv' to current working directory.

    Output File:
        - Filename: projects.csv
        - Location: Current working directory
        - Format: CSV with header row
        - Rows: 7 sample projects

    Example:
        >>> create_projects_csv()
        projects.csv has been created successfully.
    """
    data: List[List] = [
        ["ProjectName", "Deadline", "Status", "Manager", "Budget", 'Department'],
        ["Website Redesign", "2025-12-15", "In Progress", "Alice Chen", 12500, 'IT'],
        ["Mobile App MVP", "2026-03-10", "Planned", "Bob Smith", 45000, 'Product'],
        ["Q4 Marketing Campaign", "2025-11-30", "Completed", "Sarah Jenkins", 8200, 'Marketing'],
        ["Cloud Migration", "2026-06-20", "On Hold", "David Ross", 32000, 'IT'],
        ["Security Audit", "2025-10-15", "In Progress", "Elena Rodriguez", 5000, 'Security'],
        ["Data Warehouse Setup", "2027-01-25", "Planned", "Michael Scott", 18000, 'Data'],
        ["AI Chatbot Integration", "2026-05-12", "In Progress", "Jim Halpert", 22000, 'IT']
    ]

    with open('projects.csv', 'w', newline='') as file:
        writer: csv.writer = csv.writer(file)
        writer.writerows(data)

    print("projects.csv has been created successfully.")

if __name__ == "__main__":
    create_projects_csv()
