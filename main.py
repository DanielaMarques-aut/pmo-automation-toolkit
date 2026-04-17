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

# Add Scripts directories to path for imports
sys.path.insert(0, str(Path(__file__).parent / "Scripts" / "Analysis"))
sys.path.insert(0, str(Path(__file__).parent / "Scripts" / "Utils"))
sys.path.insert(0, str(Path(__file__).parent / "Scripts" / "Setup"))

# Configure logging
LOG_DIR = Path("Logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f"main_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("PMO_Engine")


# ============================================================================
# VALIDATION & SETUP FUNCTIONS
# ============================================================================

def validate_environment() -> bool:
    """
    Verify that all required files and directories exist.
    
    Checks:
    - .env file exists (for API keys)
    - Data/Raw/ directory exists
    - Scripts/Analysis/ directory exists
    - Scripts/Utils/ directory exists
    
    Returns:
        bool: True if all validations pass, False otherwise.
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
    
    # Check directories
    for dir_path in required_dirs:
        if not dir_path.exists():
            logger.error(f"❌ Directory not found: {dir_path}")
            return False
    
    logger.info("✅ Environment validation passed")
    return True


def validate_data_sources() -> bool:
    """
    Verify that required data source files exist.
    
    Checks for:
    - projects.csv in Data/Raw/
    - project_status.csv in Data/Raw/
    - dados_pmo_segunda.csv in Data/Raw/
    
    Returns:
        bool: True if at least one data source exists, False otherwise.
    """
    logger.info("📊 Checking data sources...")
    
    data_dir = Path("Data/Raw")
    required_files = [
        "projects.csv",
        "project_status.csv",
        "dados_pmo_segunda.csv"
    ]
    
    found_files = []
    for file in required_files:
        file_path = data_dir / file
        if file_path.exists():
            found_files.append(file)
            logger.info(f"  ✅ Found: {file}")
        else:
            logger.warning(f"  ⚠️ Missing: {file}")
    
    if not found_files:
        logger.error("❌ No data source files found in Data/Raw/")
        return False
    
    logger.info(f"✅ Data validation passed ({len(found_files)} sources found)")
    return True


# ============================================================================
# WORKFLOW FUNCTIONS
# ============================================================================

def run_full_analysis() -> None:
    """
    Execute the complete PMO analysis workflow.
    
    Orchestrates:
    1. Data validation
    2. PMO Consolidated Engine (main analysis with AI insights)
    3. Report generation
    4. Visualization creation
    5. Alert notification
    
    Output Files:
    - Data/Output/budget_distribution.png
    - Data/Output/audit_report_YYYY-MM-DD_HH-MM.txt
    - Logs/pmo_audit.log
    
    Returns:
        None
    """
    logger.info("\n" + "="*70)
    logger.info("🚀 STARTING FULL PMO ANALYSIS")
    logger.info("="*70)
    
    try:
        if not validate_data_sources():
            logger.error("Cannot proceed: data sources missing")
            return
        
        # Import and run PMO Consolidated Engine
        from PMO_Consolidated_Engine_v1_5 import main as pmo_engine_main
        from Data_Auditor_project_status_using_Groupby import run_consolidated_audit as data_auditor_main
        from Agregação_de_dados_V1 import run_analysis as run_analysis_main


        
        logger.info("📈 Executing PMO Consolidated Engine...")
        pmo_engine_main()
        
        logger.info("📈 Executing data auditor..")
        data_auditor_main(Path.cwd() / "data" /"raw"/ "projects.csv")

        logger.info("📈 Executing full analysis..")
        run_analysis_main()

        logger.info("✅ Full analysis completed successfully")
        logger.info("="*70 + "\n")
        
    except ImportError as e:
        logger.error(f"❌ Failed to import PMO engine: {e}")
    except Exception as e:
        logger.error(f"❌ Error during full analysis: {e}", exc_info=True)


def run_quick_audit() -> None:
    """
    Execute a quick health check on current projects.
    
    Runs Data_Auditor module to:
    - Identify overdue projects
    - Detect over-budget items
    - Generate variance analysis
    - Create quick visual report
    
    Output Files:
    - Variance visualization chart
    - Console alert summary
    
    Returns:
        None
    """
    logger.info("\n" + "="*70)
    logger.info("⚡ STARTING QUICK AUDIT")
    logger.info("="*70)
    
    try:
        if not validate_data_sources():
            logger.error("Cannot proceed: data sources missing")
            return
        
        # Import and run Data Auditor
        from Data_Auditor import audit_project_health
        
        logger.info("🔍 Running project health audit...")
        audit_project_health(Path("Data/Raw/projects.csv"))
        
        logger.info("✅ Quick audit completed successfully")
        logger.info("="*70 + "\n")
        
    except ImportError as e:
        logger.error(f"❌ Failed to import Data Auditor: {e}")
    except Exception as e:
        logger.error(f"❌ Error during quick audit: {e}", exc_info=True)


def generate_visualizations() -> None:
    """
    Create all visualization dashboards and charts.
    
    Runs PMO_Visualizer to generate:
    - Budget distribution pie charts
    - Project status bar charts
    - Timeline gantt-style visualizations
    - Department summary dashboards
    
    Output Files:
    - Data/Output/pmo_dashboard_*.png
    - Data/Output/budget_analysis_*.png
    - Data/Output/status_overview_*.png
    
    Returns:
        None
    """
    logger.info("\n" + "="*70)
    logger.info("📊 GENERATING VISUALIZATIONS")
    logger.info("="*70)
    
    try:
        if not validate_data_sources():
            logger.error("Cannot proceed: data sources missing")
            return
        
        # Import and run PMO Visualizer (try multiple versions)
        try:
            import pandas as pd
            df= pd.read_csv(Path("Data/Raw/projects.csv"))
            dept_summary = df.groupby('Department')['Budget'].sum().to_dict()
            from bar_graph_file import generate_budget_chart as visualizer_main
            logger.info("Using PMO Visualizer v2.4...")
        except ImportError:
            try:
                from PMO_Visualizer_v2_3 import main as visualizer_main
                logger.info("Using PMO Visualizer v2.3...")
            except ImportError:
                logger.warning("Latest visualizer versions not found, using fallback...")
                visualizer_main = None
        
        if visualizer_main:
            logger.info("📈 Creating visualization dashboards...")
            visualizer_main(dept_summary,"Data/Output/budget_distribution.png") 
        else:
            logger.warning("⚠️ Visualizer module not available")
        
        logger.info("✅ Visualization generation completed")
        logger.info("="*70 + "\n")
        
    except Exception as e:
        logger.error(f"❌ Error during visualization: {e}", exc_info=True)


def view_recent_reports() -> None:
    """
    Display list of recently generated reports and audit files.
    
    Shows:
    - Recent audit reports (Data/Output/audit_report_*.txt)
    - Generated visualizations (Data/Output/*.png)
    - Recent logs (Logs/*.log)
    
    Returns:
        None
    """
    logger.info("\n" + "="*70)
    logger.info("📂 RECENT REPORTS & FILES")
    logger.info("="*70)
    
    output_dir = Path("Data/Output")
    logs_dir = Path("Logs")
    
    # List reports
    if output_dir.exists():
        reports = sorted(output_dir.glob("audit_report_*.txt"), reverse=True)
        if reports:
            logger.info("\n📋 Audit Reports:")
            for i, report in enumerate(reports[:10], 1):
                size = report.stat().st_size
                modified = datetime.fromtimestamp(report.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                logger.info(f"  {i}. {report.name} ({size} bytes) - {modified}")
        else:
            logger.info("  No audit reports found")
        
        # List visualizations
        charts = sorted(output_dir.glob("*.png"), reverse=True)
        if charts:
            logger.info("\n📊 Visualizations:")
            for i, chart in enumerate(charts[:10], 1):
                size = chart.stat().st_size
                modified = datetime.fromtimestamp(chart.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                logger.info(f"  {i}. {chart.name} ({size} bytes) - {modified}")
        else:
            logger.info("  No visualizations found")
    else:
        logger.info("  Data/Output directory not found")
    
    # List logs
    if logs_dir.exists():
        recent_logs = sorted(logs_dir.glob("*.log"), reverse=True)
        if recent_logs:
            logger.info("\n📝 Recent Logs:")
            for i, log_file in enumerate(recent_logs[:5], 1):
                size = log_file.stat().st_size
                modified = datetime.fromtimestamp(log_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                logger.info(f"  {i}. {log_file.name} ({size} bytes) - {modified}")
        else:
            logger.info("  No logs found")
    
    logger.info("="*70 + "\n")

def run_strategic_mitigation() -> None:
    """
    INTEGRATION GOAL: Connects PMO AI Architecture (V1.5).
    Focus: Risk Mitigation Plans.
    """
    path = Path("Scripts/Analysis/PMO_AI_Architecture_V1_6.py")
    if not path.exists():
        logger.error(f"❌ Required script not found: {path}")
        
    logger.info("🛡️ STARTING STRATEGIC RISK MITIGATION (V1.5)")
    try:
        import pandas as pd
        # Programming Base: Fail-fast check for specific AI script
        from PMO_Consolidated_Engine_v1_5 import get_ai_insight  as run_mitigation
        df= pd.read_csv(Path("Data/Raw/projects.csv"))
        dept_summary = df.groupby('Department')['Budget'].sum().to_dict()
        run_mitigation(dept_summary)
        from Exporter import save_executive_summary as save_summary
        content = f"AI-generated mitigation plan based on project KPIs and risk profiles.{run_mitigation(dept_summary)}"
        save_summary(content)
        logger.info("✅ Mitigation plan generated.")
    except ImportError as e:
        logger.error(f"❌ ImportError occurred: {e}")

def show_menu() -> str:
    """
    Display interactive CLI menu and get user selection.3
    
    Menu Options:
    1. Run Full PMO Analysis
    2. Quick Project Audit
    3. Strategic Risk Mitigation (AI V1.5) ⭐ NEW
    4. Department Alerts (V1.1) ⭐ NEW
    5. Generate Visualizations
    6. View Recent Reports
    7. Exit
    
    Returns:
        str: User's selected option (1-7)
    """
    print("\n" + "="*70)
    print("🏢 PMO AUTOMATION ENGINE - MAIN MENU")
    print("="*70)
    print("\n📋 Available Operations:\n")
    print("  1️⃣  Run Full PMO Analysis")
    print("      └─ Complete workflow: data validation → AI analysis → reports → notifications\n")
    print("  2️⃣  Quick Project Audit")
    print("      └─ Fast health check: overdue projects, budget variance, risks\n")
    print("  3️⃣  Strategic Risk Mitigation (AI V1.5) ⭐ NEW")
    print("      └─ AI-generated mitigation plans based on project KPIs and risk profiles\n")
    print("  4️⃣  Department Alerts (V1.1) ⭐ NEW")
    print("      └─ Alert system for at-risk projects\n")
    print("  5️⃣  Generate Visualizations")
    print("      └─ Create dashboards: budget charts, status overview, timelines\n")
    print("  6️⃣  View Recent Reports")
    print("      └─ Browse generated files: audit reports, visualizations, logs\n")
    print("  7️⃣  Exit")
    print("      └─ Close application\n")
    print("="*70)
    
    while True:
        choice = input("🎯 Select option (1-7): ").strip()
        if choice in ["1", "2", "3", "4", "5", "6", "7"]:
            return choice
        print("❌ Invalid selection. Please enter 1-7.")

def Run_department_alerts() -> None:
    """
    INTEGRATION GOAL: Connects PMO AI Architecture (V1.5).
    Focus: Department Alerts.
    """
    path = Path("Scripts/Analysis/PMO_AI_Architecture_V1_6.py")
    if not path.exists():
        logger.error(f"❌ Required script not found: {path}")
        
    logger.info("⚠️ STARTING DEPARTMENT ALERTS (V1.1)")
    try:
        import pandas as pd
        import datetime
        # Programming Base: Fail-fast check for specific AI script
        from PMO_Consolidated_Engine_v1_5 import alert_overdue_projects as run_alerts
        df= pd.read_csv(Path("Data/Raw/projects.csv"))
        df['Deadline'] = pd.to_datetime(df['Deadline'])
        today = datetime.datetime.now()
        overdue_count: int = df[(df['Deadline'] < today) & (df['Status'] != 'Completed')].shape[0]
        print(f"Total overdue projects: {overdue_count}")
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
    Main application loop for PMO Automation Engine.
    
    Orchestrates:
    1. Environment validation
    2. Interactive menu display
    3. Strategic risk mitigation (AI V1.5)
    4. Department alerts (V1.1)
    5. Visualization generation
    6. Error handling and logging
    7. Application shutdown
    
    Returns:
        None
    """
    logger.info("🚀 PMO AUTOMATION ENGINE STARTED")
    logger.info(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Validate environment before showing menu
    if not validate_environment():
        logger.error("❌ Environment validation failed. Please check your setup.")
        return
    
    # Main application loop
    while True:
        try:
            option = show_menu()
            
            if option == "1":
                run_full_analysis()
            elif option == "2":
                run_quick_audit()
            elif option == "3":
                run_strategic_mitigation()
            elif option == "4":
                Run_department_alerts()   
            elif option == "5":
                generate_visualizations()
            elif option == "6":
                view_recent_reports()
            elif option == "7":
                logger.info("👋 Shutting down PMO Engine...")
                logger.info(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("\n✅ Thank you for using PMO Automation Engine!")
                break
        
        except KeyboardInterrupt:
            logger.info("⏸️ Application interrupted by user")
            print("\n\n⏸️ Application interrupted. Goodbye!")
            break
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}", exc_info=True)
            print(f"\n❌ An error occurred: {e}")
            print("Please check the logs for more details.\n")


if __name__ == "__main__":
    main()
