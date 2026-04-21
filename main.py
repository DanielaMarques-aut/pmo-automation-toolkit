"""
main.py - PMO Automation Engine Entry Point

Main orchestration module for the PMO (Project Management Office) automation system.
Provides a command-line interface for running various analysis and reporting workflows.

Architecture:
    - Unified entry point for all PMO operations
    - Interactive CLI menu for easy navigation
    - Orchestrates Scripts/Analysis/ workflows
    - Centralized error handling and logging
    - Integration with environment configuration

Workflows Supported:
    1. Full Analysis: Complete PMO audit with AI insights and visualizations
    2. Quick Audit: Fast health check on current project status
    3. Generate Reports: Create all visualization dashboards
    4. View Reports: Browse recently generated reports
    5. Data Validation: Verify data sources before processing

Dependencies:
    - Scripts/Analysis/PMO_Consolidated_Engine
    - Scripts/Analysis/Data_Auditor
    - Scripts/Analysis/PMO_Visualizer
    - Scripts/Utils/config
    - pathlib, logging, os, sys

Usage:
    python main.py
    
    Then select option from interactive menu:
    1. Run Full PMO Analysis
    2. Quick Project Audit
    3. Strategic Risk Mitigation (AI V1.5) ⭐ NEW
    4. Department Alerts & Escalation (V1.1) ⭐ NEW 
    5. Generate Visualizations
    6. View Recent Reports
    7. Exit

Author: Daniela Marques
Version: 1.0
Created: April 2026
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List
from venv import logger



# Configure logging


def setup_logging(log_dir: Path = Path("Logs")) -> logging.Logger:
    """
    Set up logging configuration for the PMO Automation Engine.
    
    Logs are saved to a file in the specified log directory with a timestamped filename.
    Also outputs logs to the console.
    Creates a timestamped log file and configures both file and stream 
    handlers to ensure visibility during CLI operations and audits.
    Args:
        log_dir (Path): Directory where log files will be stored. Default is "logs".
    
    Returns:
        logging.Logger: Configured logger instance for the application.
    Raises:
        OSError: If the directory cannot be created due to permission issues.

    """
    try:
        LOG_DIR:Path = Path("Logs")
        log_dir.mkdir(exist_ok=True)
    except OSError as e:    
        print(f"Error creating log directory: {e}")
    
    full_log_path = log_dir / f"main_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(full_log_path, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger("PMO_Engine")
    print(logger.log)  # This will print the logger object to confirm it's set up
   
    logging.info(f"Logging initialized. Session log: {full_log_path}")
    return log_dir

def VIEW_LATEST_LOGS(log_dir: Path = Path("Logs")) -> None:
    """Reads the last 10 lines of the system log file."""
    print("\n📜 --- ÚLTIMOS REGISTOS DO SISTEMA ---")
    # Implementation for viewing latest logs would go here
    try:
        filename=sorted(log_dir.glob("main_*.log"), reverse=True)[0]  # Get the latest log file
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[-10:]:
                print(line.strip())
    except FileNotFoundError:
        print("⚠️ Ficheiro de log ainda não criado.")



# ============================================================================
# VALIDATION & SETUP FUNCTIONS
# ============================================================================

def validate_environment(key: Path= Path(".env"), default: Optional[str] = None) -> bool:
    """
    Verify that all required files and directories exist.

    Retrieves an environment variable with Fail-Fast validation.
    
    Args:
        key (str): The name of the environment variable (e.g., 'GEMINI_API_KEY').
        default (Optional[str]): A fallback value if the key is missing.
        
     Returns:
        bool: True if all validations pass, False otherwise.
        
    Raises:
        ValueError: If the key is missing and no default is provided, 
            preventing unauthorized or broken API calls.
      Checks:
    - .env file exists (for API keys)
    - Data/Raw/ directory exists
    - Scripts/Analysis/ directory exists
    - Scripts/Utils/ directory exists
    
  
    """
    logger.info("🔍 Validating environment...")
    
    required_files = [Path(".env")]
    required_dirs = [
        Path("Data/Raw"),
        Path("Data/Output"),
        Path("Scripts/Analysis"),
        Path("Scripts/Utils"),
        Path("Logs")
    ]
    
    # Check files
    for file in required_files:
        if not file.exists():
            logger.warning(f"⚠️ File not found: {file} (optional if env vars are set)")
            raise ValueError(f"Environment variable '{file}' must be set via .env file.")
    
    # Check directories
    for dir_path in required_dirs:
        if not dir_path.exists():
            logger.error(f"❌ Directory not found: {dir_path}")
            raise ValueError(f"Environment variable '{dir_path}' must be set via .env file.")
            return False
    
    logger.info("✅ Environment validation passed")
    return True


def validate_data_sources(data_dir: Path = Path("Data/Raw")) -> bool:
    """
    Verify that required data source files exist.
    Validates the presence of mandatory CSV data sources in the specified directory.

    This function performs a pre-flight check to ensure the PMO engine has access
    to all required input files before attempting analysis. It logs individual
    file status (found/missing) and provides a summary count.

    Args:
        data_dir (Path): The directory path where raw data files 
            are expected. Defaults to "Data/Raw".

    Checks for:
    - projects.csv in Data/Raw/
    - project_status.csv in Data/Raw/
    - dados_pmo_segunda.csv in Data/Raw/

    
    Returns:
        bool: True if ALL required files are found, False if any are missing.
    """
    logger.info("📊 Checking data sources...")
    
    data_dir = Path("Data/Raw")
    required_files: list[str] = [
        "projects.csv",
        "project_status.csv",
        "dados_pmo_segunda.csv"
    ]
  
    found_files: list[str] = []
    for file in required_files:
        file_path = data_dir / file
        if file_path.exists():
            found_files.append(file)
            logger.info(f"  ✅ Found: {file}")
        else:
            logger.warning(f"  ⚠️ Missing: {file}")
    # Logic Check: Ensure we have a 1:1 match
    if len(found_files) != len(required_files):
       missing_count = len(required_files) - len(found_files)
       logger.error(f"❌ Validation failed: {missing_count} file(s) missing in {data_dir}")
       return False
    
    logger.info(f"✅ Data validation passed ({len(found_files)} sources found)")
    return True


# ============================================================================
# WORKFLOW FUNCTIONS
# ============================================================================

def run_full_analysis() -> None:
    """
    Execute the complete PMO analysis workflow.
     This function acts as the primary controller, executing sequential tasks:
    1. Data Validation: Ensures required CSVs are present.
    2. Engine Execution: Runs the AI-driven consolidated analysis.
    3. Data Auditing: Checks project status consistency using Groupby logic.
    4. Final Reporting: Aggregates all data into a final audit summary.
    5.Visualization creation
    6.Alert notification
  
   
    Output Side Effects:
        - Creates 'Data/Output/budget_distribution.png'
        - Generates 'Data/Output/audit_report_YYYY-MM-DD_HH-MM.txt'
        - Appends session logs to 'Logs/pmo_audit.log'

    Raises:
        ImportError: If any of the internal analysis modules are missing.
        Exception: Captures and logs any runtime errors during the workflow 
            execution to prevent a silent crash.
    """
    logger.info("\n" + "="*70)
    logger.info("🚀 STARTING FULL PMO ANALYSIS")
    logger.info("="*70)
    
    try:
        if not validate_data_sources():
            logger.error("Cannot proceed: data sources missing")
            return
        
       # Scoped imports to manage complex dependencies
        from Scripts.Analysis.PMO_Consolidated_Engine_v1_5 import main as pmo_engine_main
        from Scripts.Analysis.Data_Auditor_project_status_using_Groupby import run_consolidated_audit as data_auditor_main
        from Scripts.Analysis.Agregação_de_dados_V1 import run_analysis as run_analysis_main


        logger.info("📈 Executing PMO Consolidated Engine...")
        pmo_engine_main()
        
        logger.info("📈 Executing data auditor..")
        data_auditor_main(Path.cwd() / "data" /"raw"/ "projects.csv")

        logger.info("📈 Executing full analysis..")
        run_analysis_main()

        logger.info("✅ Full analysis completed successfully")
        logger.info("="*70 + "\n")
    except ImportError as e:
        logger.error(f"❌ Structural Error: Failed to import PMO engine components: {e}")
    except Exception as e:
        # exc_info=True provides the full stack trace in the log file
        logger.error(f"❌ Critical Failure during full analysis: {e}", exc_info=True)


def run_quick_audit() -> None:
    """
    Execute a quick health check on current projects.    
    This function targets immediate variances and overdue items without running
    the full AI consolidation suite. It is designed for rapid status updates.

    Runs Data_Auditor module to:
        Workflow:
        1. Validates presence of 'projects.csv'.
        2. Calculates budget vs. actual variance.
        3. Identifies projects past their 'Due Date'.
        4.etect over-budget items
    
    Output Files:
        - Variance visualization chart (PNG format in Data/Output).
        - Console-based alert summary for the PMO lead.

    Raises:
        ImportError: If the 'Data_Auditor' script is missing or renamed.
        Exception: General catch-all for file read/write issues during auditing.
    """
    logger.info("\n" + "="*70)
    logger.info("⚡ STARTING QUICK AUDIT")
    logger.info("="*70)
    
    try:
        if not validate_data_sources():
            logger.error("Cannot proceed: data sources missing")
            return
        
       # Targeted import for performance
        from Scripts.Analysis.Data_Auditor import audit_project_health
        
        logger.info("🔍 Running project health audit...")
        # Passing the specific CSV path as a Path object
        audit_project_health(Path("Data/Raw/projects.csv"))
        
        logger.info("✅ Quick audit completed successfully")
        logger.info("="*70 + "\n")
        
    except ImportError as e:
        logger.error(f"❌ Failed to import Data Auditor: {e}")
    except Exception as e:
        logger.error(f"❌ Error during quick audit: {e}", exc_info=True)


def generate_visualizations() -> None:
    """
    Triggers the generation of the PMO executive dashboard and charts.
     Aggregates processed data into visual formats suitable for stakeholder.
     This function includes a multi-tier fallback mechanism to attempt visualization 
    using the latest available script versions (v2.4.x down to v2.3.x).


      Visuals Generated:
        - Budget distribution charts.
        - Project status bar charts (Active, Delayed, Completed).
        - Timeline/Gantt-style visualizations.
        - Department-specific summary dashboards.

    
    Output Files:
    - Data/Output/pmo_dashboard_*.png
    - Data/Output/budget_analysis_*.png
    - Data/Output/status_overview_*.png
    
    Returns:
       None: Files are written directly to the Data/Output directory.
    Raises:
        ImportError: If the visualization module is missing or has unresolved dependencies.
        Exception: Captures any errors during data processing or file generation, 
            ensuring the application does not crash and logs the issue for review.
        

    Process Flow:
        1. Validates raw data sources.
        2. Aggregates budget data by department using Pandas.
        3. Attempts to load the primary visualizer (v2.4).
        4. Falls back to the secondary summary function (v2.3) if primary is missing.
        5. Outputs a distribution PNG if a visualizer is successfully bound.


    """
    logger.info("\n" + "="*70)
    logger.info("📊 GENERATING VISUALIZATIONS")
    logger.info("="*70)
    
    try:
        if not validate_data_sources():
            logger.error("Cannot proceed: data sources missing")
            return
        
       # --- Data Aggregation Layer ---
        import pandas as pd
        
        # Type Hinting for the processed summary
        dept_summary: dict[str, float]
        # --- Dynamic Visualizer Binding ---
        visualizer_main = None

        try:
           
            df: pd.DataFrame = pd.read_csv(Path("Data/Raw/projects.csv"))
            dept_summary: dict[str, float] = df.groupby('Department')['Budget'].sum().to_dict()
            from Scripts.Utils.bar_graph_file import generate_budget_chart as visualizer_main
            logger.info("Using PMO Visualizer v2.4...")
        except ImportError:
            try:
                from Scripts.Utils.bar_graph_Department_sumary_funcion import create_department_summary_chart as visualizer_main
                logger.info("Using PMO Visualizer v2.3...")
            except ImportError:
                logger.warning("Latest visualizer versions not found, using fallback...")
                visualizer_main = None
        # --- Execution Layer ---
        if visualizer_main:
            logger.info("📈 Creating visualization dashboards...")
            # Ensure pathing is handled as a string for legacy library compatibility
            output_file: str = "Data/Output/budget_distribution.png"
            visualizer_main(dept_summary, output_file)
        else:
            logger.warning("⚠️ Visualizer module not available")
        
        logger.info("✅ Visualization generation completed")
        logger.info("="*70 + "\n")
        
    except Exception as e:
        logger.error(f"❌ Error during visualization: {e}", exc_info=True)


def view_recent_reports() -> None:
    """ 
    Scans output and log directories to display a summarized list of recent files.
    This utility provides a quick CLI view of the engine's recent activity, 
    including files and modified timestamps. It targets audit reports, 
    visualizations, and system logs.
    
    Shows:
    - Recent audit reports (Data/Output/audit_report_*.txt)
    - Generated visualizations (Data/Output/*.png)
    - Recent logs (Logs/*.log)
    
    Returns:
        None:Outputs information directly to the logger/console.
    """

    logger.info("\n" + "="*70)
    logger.info("📂 RECENT REPORTS & FILES")
    logger.info("="*70)
    
    output_dir:Path = Path("Data/Output")
    logs_dir:Path = Path("Logs")

    # --- Audit Reports Section ---
    if output_dir.exists():
        # glob and sort by name descending (which works for YYYY-MM-DD filenames)
        reports: List[Path] = sorted(output_dir.glob("audit_report_*.txt"), reverse=True)
        if reports:
            logger.info("\n📋 Audit Reports:")
            for i, report in enumerate(reports[:10], 1):
                size: int = report.stat().st_size
                modified: str = datetime.fromtimestamp(report.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                logger.info(f"  {i}. {report.name} ({size} bytes) - {modified}")
        else:
            logger.info("  No audit reports found")
        
        # List visualizations
        charts: List[Path] = sorted(output_dir.glob("*.png"), reverse=True)
        if charts:
            logger.info("\n📊 Visualizations:")
            for i, chart in enumerate(charts[:10], 1):
                size: int = chart.stat().st_size
                modified: str = datetime.fromtimestamp(chart.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                logger.info(f"  {i}. {chart.name} ({size} bytes) - {modified}")
        else:
            logger.info("  No visualizations found")
    else:
        logger.info("  Data/Output directory not found")
        
    # --- System Logs Section ---
    if logs_dir.exists():
        recent_logs: List[Path] = sorted(logs_dir.glob("*.log"), reverse=True)
        if recent_logs:
            logger.info("\n📝 Recent Logs:")
            for i, log_file in enumerate(recent_logs[:5], 1):
                size: int = log_file.stat().st_size
                modified: str = datetime.fromtimestamp(log_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                logger.info(f"  {i}. {log_file.name} ({size} bytes) - {modified}")
        else:
            logger.info("  No logs found")
    
    logger.info("="*70 + "\n")

def run_strategic_mitigation() -> None:
    """
    INTEGRATION GOAL: Connects PMO AI Architecture (V1.5).
    Focus: Risk Mitigation Plans
    
    Executes the AI-driven Strategic Risk Mitigation workflow (V1.5).
    
    This function connects the PMO architecture to high-level AI insights to
    generate proactive mitigation plans based on departmental budget KPIs.

    Workflow:
        1. Validates the presence of the AI Architecture script.
        2. Aggregates departmental budget totals.
        3. Invokes the AI Engine to generate a mitigation strategy.
        4. Exports the generated content as an Executive Summary.

    Side Effects:
        - Logs detailed AI operation status.
        - Saves an 'executive_summary' via the Exporter module.

    Raises:
        ImportError: If the PMO_Consolidated_Engine or Exporter is missing.
        Exception: Captures and logs API failures or data processing errors.
    """
    
    path: Path = Path("Scripts/Analysis/PMO_AI_Architecture_V1_6.py")
    # Fail-fast check for architectural integrity
    if not path.exists():
        logger.error(f"❌ Required script not found: {path}")
        return
    logger.info("🛡️ STARTING STRATEGIC RISK MITIGATION (V1.5)")
    try:
        import pandas as pd
        # Programming Base: Fail-fast check for specific AI script
        from Scripts.Analysis.PMO_Consolidated_Engine_v1_5 import get_ai_insight  as run_mitigation
        # Data Preparation: Aggregate budget by department for AI input
        df: pd.DataFrame = pd.read_csv(Path("Data/Raw/projects.csv"))
        dept_summary: dict = df.groupby('Department')['Budget'].sum().to_dict()
        # AI Execution - Store result in a variable to avoid double-calling
       
        logger.info("🤖 Querying AI Engine for mitigation strategies...")
        mitigation_content: str = run_mitigation(dept_summary)
        # Content Export
        from Scripts.Utils.Exporter import save_executive_summary as save_summary
        content: str = f"AI-generated mitigation plan based on project KPIs and risk profiles.{run_mitigation(dept_summary)}"
        save_summary(content)
        logger.info("✅ Mitigation plan generated.")
    except ImportError as e:
        logger.error(f"❌ ImportError occurred: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected error during risk mitigation: {e}", exc_info=True)

def show_menu() -> str:
    """
    Display interactive CLI menu and get user selection.3
    Provides a structured interface for PMO users to navigate through analysis,
    auditing, risk mitigation, and reporting workflows.
    Menu Options:
    1. Run Full PMO Analysis
    2. Quick Project Audit
    3. Strategic Risk Mitigation (AI V1.5) ⭐ NEW
    4. Department Alerts (V1.1) ⭐ NEW
    5. Generate Visualizations
    6. View Recent Reports
    7. Exit
    8. View Latest Logs
    Returns:
        str: User's selected option (1-8)

    """
    # Detailed menu display for the user
    print("\n" + "="*70)
    print("🏢 PMO AUTOMATION ENGINE - MAIN MENU")
    print("="*70)
    print("\n📋 Available Operations:\n")
    menu_options = {
        "1": "Run Full PMO Analysis (Validation -> AI -> Reports)",
        "2": "Quick Project Audit (Health check & Variance)",
        "3": "Strategic Risk Mitigation (AI V1.5) ⭐ NEW",
        "4": "Department Alerts (V1.1) ⭐ NEW",
        "5": "Generate Visualizations (Dashboards & Charts)",
        "6": "View Recent Reports (Audit files & Logs)",
        "7": "Exit (Close application)",
        "8":"view latest logs"
    }

    for key, description in menu_options.items():
        print(f" [{key}] {description}")
    
    print("="*70)
    
    while True:
        choice:str = input("🎯 Select option (1-8): ").strip()
        if choice in menu_options:
            return choice
        print("❌ Invalid selection. Please enter 1-8.")

def Run_department_alerts() -> None:
    """
    INTEGRATION GOAL: Connects PMO AI Architecture (V1.5).
    Focus: Department Alerts.

    Connects to the PMO AI Architecture (V1.5) to broadcast department-level alerts.
    
    Analyzes project deadlines against the current system date and identifies
    uncompleted projects that are overdue.

    Workflow:
        1. Checks for mandatory AI script dependencies.
        2. Loads project data and converts 'Deadline' to datetime objects.
        3. Filters for (Deadline < Today) AND (Status != 'Completed').
        4. Triggers alert notifications via the Consolidated Engine.

    Raises:
        ImportError: If the PMO_AI_Architecture or Alert scripts are missing.
        Exception: Captures date parsing errors or file access issues.

    """
    path: Path = Path("Scripts/Analysis/PMO_AI_Architecture_V1_6.py")
    if not path.exists():
        logger.error(f"❌ Required script not found: {path}")
        return
    logger.info("⚠️ STARTING DEPARTMENT ALERTS (V1.1)")
    try:
        import pandas as pd
        import datetime
        # Programming Base: Fail-fast check for specific AI script
        from Scripts.Analysis.PMO_Consolidated_Engine_v1_5 import alert_overdue_projects as run_alerts
        # Data Loading & Type Conversion
        df: pd.DataFrame = pd.read_csv(Path("Data/Raw/projects.csv"))
        # Explicitly handling date conversion to avoid comparison errors
        df['Deadline']: pd.Series = pd.to_datetime(df['Deadline'], errors='coerce')
        today: datetime.datetime = datetime.datetime.now()
        # Filtering logic for overdue, uncompleted projects
        overdue_mask = (df['Deadline'] < today) & (df['Status'] != 'Completed')
        overdue_count: int = int(df[overdue_mask].shape[0])
        print(f"Total overdue projects: {overdue_count}")
        # Triggering the alert notification system
        run_alerts(overdue_count)
        logger.info("✅ Department alerts generated.")
    except ImportError as e:
        logger.error(f"❌ Script 'PMO AI Architecture (V1.5).py' not found in path.Error: {e}")
    except Exception as e:  
        logger.error(f"❌ Error during department alerts: {e}", exc_info=True)
# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main() -> None:
    """
    Primary application loop for the PMO Automation Engine.
    
    Coordinates environment validation, the interactive UI, and the 
    dispatching of sub-processes based on user selection.
    
    Orchestrates:
        1. Environment & Path Validation
        2. Interactive CLI Menu
        3. Feature Dispatching (AI, Audit, Alerts, Reporting)
        4. Global Error Handling & Shutdown
    """
    
    logger.info("🚀 PMO AUTOMATION ENGINE STARTED")
    logger.info(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
   # Validate environment (API keys, directories, etc.) before showing menu
    # Assuming validate_environment is defined in your config/setup section
    if not validate_environment():
        logger.error("❌ Environment validation failed. Please check your setup.")
        return
    
    # Main application loop
    while True:
        try:
            option: str = show_menu()
            
            if option == "1":
                setup_logging()  # Ensure logging is initialized before running analysis
                run_full_analysis()
                logger.info("✅ Full PMO Analysis workflow completed.")
            elif option == "2":
                setup_logging()
                run_quick_audit()
                logger.info("✅ Quick Project Audit completed.")
            elif option == "3":
                setup_logging()
                run_strategic_mitigation()
                logger.info("✅ Strategic Mitigation workflow completed.")
            elif option == "4":
                setup_logging()
                Run_department_alerts()   
                logger.info("✅ Department Alerts workflow completed.")
            elif option == "5":
                setup_logging()
                generate_visualizations()
                logger.info("✅ Visualization generation completed.")
            elif option == "6":
                setup_logging()
                view_recent_reports()
                logger.info("✅ Recent reports displayed.")
            elif option == "7":
                setup_logging()
                logger.info("👋 Shutting down PMO Engine...")
                logger.info(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("\n✅ Thank you for using PMO Automation Engine!")
                break
            elif option == "8":
                VIEW_LATEST_LOGS()
                logger.info("✅ Latest logs displayed.")
        
        except KeyboardInterrupt:
            logger.info("⏸️ Application interrupted by user")
            print("\n\n⏸️ Application interrupted. Goodbye!")
            break
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}", exc_info=True)
            print(f"\n❌ An error occurred: {e}")
            print("Please check the logs for more details.\n")


if __name__ == "__main__":
    # This ensures the engine only runs if executed directly, 
    # not if imported as a library.

    main()
