"""Project Structure Initialization and File Organization Module.

This module provides utilities for creating standardized project directories
and managing file organization by type (data, logs, scripts). It implements
professional project scaffolding patterns used in production systems.

Key Functionality:
    1. organizar_projeto() - Create standard IA-Ops project folder structure
    2. gerar_requirements() - Generate requirements.txt from library list
    3. movearquivos() - Organize files by extension into appropriate folders

Project Structure:
    ├── Data/
    │   ├── Raw/          (Source data, CSVs, API responses)
    │   └── Output/       (Processed reports, cleaned datasets)
    ├── Logs/             (Log files, audit trails, error messages)
    ├── Scripts/
    │   ├── Utils/        (Utility functions, helpers)
    │   ├── Analysis/     (Data analysis, processing scripts)
    │   └── Setup/        (Initialization, configuration, setup scripts)
    ├── Testes/           (Test files, unit tests, integration tests)
    └── Docs/
        └── Reports/      (Documentation, README, final reports)

Architecture Pattern:
    This module follows the Single Responsibility Principle with three
    independent functions:
    - organizar_projeto(): Creates folder structure
    - gerar_requirements(): Generates dependency manifest
    - movearquivos(): Organizes existing files
    
    Each function can be used independently or called together for full setup.

File Organization Strategy:
    Data files (.csv, .xlsx) → Data/ folder
    Log files (.log, .json)  → Logs/ folder
    Others remain in place   → Requires manual organization
    
    If target file already exists, appends numeric suffix: file.csv → file2.csv

Examples:
    Initialize new project with complete setup:
    
    >>> organizar_projeto()
    >>> gerar_requirements()
    >>> movearquivos()
    >>> # Result: Folders created, requirements.txt generated, files organized
    
    Create structure only:
    
    >>> organizar_projeto()
    >>> # Result: Empty folder structure ready for use
    
    Organize existing files:
    
    >>> movearquivos()
    >>> # Files with .csv, .xlsx moved to Data/
    >>> # Files with .log, .json moved to Logs/
"""

from pathlib import Path
from typing import List, Optional, Dict


def organizar_projeto() -> bool:
    """Create standard folder structure for a scalable AI-Ops project.
    
    Establishes a professional directory hierarchy following industry best
    practices for machine learning operations (MLOps) and data engineering
    projects. This scaffolding provides clear separation of concerns and
    enables team members to quickly understand project organization.
    
    Folders Created:
        - Data/        (Input and output datasets)
        - Logs/        (Application logs and audit trails)
        - Scripts/     (Core project code)
        - Testes/      (Unit and integration tests)
        - Docs/        (Documentation and reports)
    
    Subfolders Created:
        - scripts/Utils/     (Reusable utility functions)
        - scripts/Analysis/  (Data analysis and transformation)
        - scripts/Setup/     (Initialization and configuration)
        - docs/Reports/      (Final reports and documentation)
        - Data/Raw/          (Raw input data)
        - Data/Output/       (Processed and cleaned data)
    
    Args:
        None
    
    Returns:
        bool: True if all folders created successfully, False if any errors occurred.
    
    Raises:
        No exceptions raised. PermissionError is caught and printed.
        Function continues even if some folders cannot be created.
    
    Notes:
        IDEMPOTENCY:
        This function is safe to call multiple times. If folders already exist,
        the Path.exists() check prevents errors and duplicate messages.
        
        SCALABILITY:
        This structure accommodates projects from startup to enterprise scale:
        - Single data scientist: One Scripts/Analysis folder per analysis
        - Team project: Multiple subfolders per category for parallel work
        - Production system: Separate Data/Raw (source) from Data/Output (products)
        
        NAMING CONVENTION - Single Names:
        Folder names use singular (Data, Logs, Docs, Scripts) rather than plural.
        This is preferred in professional projects and tool conventions
        (e.g., "src" not "sources", "bin" not "binaries").
    
    Examples:
        Initialize project structure:
        
        >>> success = organizar_projeto()
        >>> if success:
        ...     print("Project ready for development")
        ... else:
        ...     print("Some folders could not be created - check permissions")
        >>> import os
        >>> "Data" in os.listdir(".")
        True
        
        Check created structure:
        
        >>> organizar_projeto()
        >>> Path("Scripts").exists()
        True
        >>> Path("Scripts/Utils").exists()
        True
    """
    # List of top-level directories to create
    pastas: List[str] = ["Data", "Logs", "Scripts", "Testes", "Docs"]
    
    # List of subdirectories following hierarchical naming
    # Format: parent/child allows pathlib to handle nesting
    subpastas: List[str] = [
        "Scripts/Utils",        # Utility functions and helpers
        "Scripts/Analysis",     # Data analysis and processing
        "Scripts/Setup",        # Initialization and configuration
        "Docs/Reports",         # Output reports and documentation
        "Data/Raw",             # Raw source data from APIs or files
        "Data/Output"           # Processed data, clean datasets
    ]
    
    # Create all top-level folders
    success: bool = True
    all_folders: List[str] = pastas + subpastas
    
    for pasta in all_folders:
        try:
            p: Path = Path(pasta)
            if not p.exists():
                # Create folder with parent directories as needed
                p.mkdir(parents=True, exist_ok=True)
                print(f"✅ Folder '{pasta}' created.")
            else:
                print(f"ℹ️ Folder '{pasta}' already exists.")
        except PermissionError:
            print(f"❌ Permission denied creating '{pasta}'")
            success = False
        except Exception as e:
            print(f"❌ Error creating '{pasta}': {str(e)}")
            success = False
    
    return success


def gerar_requirements() -> bool:
    """Generate requirements.txt file listing project dependencies.
    
    Creates a requirements.txt manifest in the project root containing all
    Python packages needed for the project. This enables reproducible
    environments: team members can run 'pip install -r requirements.txt'
    to install identical versions.
    
    Dependencies Listed (Examples from PMO Systems):
        - pandas          (Data manipulation and analysis)
        - requests        (HTTP API client)
        - python-dotenv   (Environment variable management)
        - openpyxl        (Excel file manipulation)
        - google-genai    (Google Gemini AI API client)
    
    Args:
        None
    
    Returns:
        bool: True if requirements.txt created successfully, False if write failed.
    
    Raises:
        No exceptions raised. IOError is caught and logged to console.
    
    Notes:
        DEPENDENCY MANAGEMENT:
        Starting with a basic list of core libraries enables quick setup.
        As the project grows, manually add additional dependencies or use:
        
            pip freeze > requirements.txt
        
        This command automatically exports all installed packages in your
        current environment to requirements.txt.
        
        VERSION PINNING:
        production-grade requirements.txt should include version constraints:
        
            pandas==1.5.3
            requests>=2.28.0
            google-genai~=0.3.0
        
        This prevents breaking changes when team members upgrade.
        Current implementation omits versions - adapt for production use.
    
    Examples:
        Generate requirements.txt:
        
        >>> gerar_requirements()
        ✅ Ficheiro requirements.txt gerado.
        >>> with open("requirements.txt") as f:
        ...     print(f.read())
        pandas
        requests
        python-dotenv
        ...
        
        Using for team setup:
        
        >>> gerar_requirements()
        >>> # Team member runs:
        >>> # pip install -r requirements.txt
        >>> # Gets identical package versions
    """
    # Core libraries used in typical PMO automation project
    libs: List[str] = [
        "pandas",               # Data analysis and manipulation
        "requests",             # HTTP client for APIs
        "python-dotenv",        # Environment variable management
        "openpyxl",             # Excel file reading/writing/formatting
        "google-genai"          # Google Gemini AI API
    ]
    
    try:
        # Write each library name to requirements.txt (one per line)
        with open("requirements.txt", "w", encoding="utf-8") as f:
            for lib in libs:
                f.write(f"{lib}\n")
        print("✅ File requirements.txt generated.")
        return True
    except IOError as e:
        print(f"❌ Error writing requirements.txt: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False


def movearquivos() -> Optional[Dict[str, int]]:
    """Organize files in current directory by type into designated folders.
    
    Scans the current directory and moves files to appropriate subdirectories
    based on file extension. This simplifies project organization for users
    working with mixed file types.
    
    Organization Rules:
        Extensions (.xlsx, .csv) → Data/ folder
        Extensions (.log, .json)  → Logs/ folder
        Others                    → Remain in place
    
    Rename Strategy:
        If target directory already contains a file with the same name,
        append numeric suffix before extension:
        
            project.csv (in Data/) + project.csv (source) = project2.csv
            report.json (in Logs/) + report.json (source) = report2.json
    
    Args:
        None
    
    Returns:
        Optional[Dict[str, int]]: Dictionary with move counts by category:
            {
                "data": 3,  (Files moved to Data/)
                "logs": 2   (Files moved to Logs/)
            }
            Returns None if current directory cannot be read.
    
    Raises:
        No exceptions raised to caller. Individual file move errors are caught,
        logged to console, and processing continues with next file.
        
        Possible errors handled internally:
        - FileNotFoundError: Target folder doesn't exist (creates it)
        - PermissionError: Cannot move file (logs error, continues)
        - OSError: Cross-filesystem move failure (logs error, continues)
    
    Notes:
        SIDE EFFECTS - Console Output:
        Prints status message for each file at console.
        Production version might reduce verbosity using logging module.
        
        EDGE CASE - Naming Conflicts:
        When target directory has file with same name, numeric suffix added.
        This preserves both files but may leave confusing names like "report2.csv".
        Consider renaming strategy for production use (timestamps, git hashes).
        
        IDEMPOTENCY CONCERN:
        Running this function twice on same directory behaves differently:
        First run: report.csv → Data/report.csv
        Second run: Checks Data/ exists and has report.csv, renames to report2.csv
        
        This is intentional to prevent data loss but may surprise users.
    
    Examples:
        Organize mixed files in project root:
        
        >>> # Current directory contains: project.csv, errors.log, config.json, README.md
        >>> results = movearquivos()
        >>> # Output:
        >>> # File moved to Data/: project.csv
        >>> # File moved to Logs/: errors.log
        >>> # File moved to Logs/: config.json
        >>> # README.md remains in place (not matching extension rules)
        >>> print(results)
        {'data': 1, 'logs': 2}
        
        Using in startup sequence:
        
        >>> organizar_projeto()         # Create folder structure
        >>> movearquivos()              # Organize existing files
        >>> gerar_requirements()        # Generate dependency list
        >>> # Project now organized and ready for use
    """
    source_dir: Path = Path(".")
    move_counts: Dict[str, int] = {"data": 0, "logs": 0}
    
    try:
        # Scan current directory for all files
        for file in source_dir.iterdir():
            # Only process files, skip directories
            if not file.is_file():
                continue
            
            # Check data file extensions (.xlsx, .csv)
            if file.suffix.lower() in [".xlsx", ".csv"]:
                targetdir: Path = Path("Data")
                targetpath: Path = targetdir / file.name
                
                # If file with same name exists in target, add numeric suffix
                if targetpath.exists():
                    # Split filename and extension: "report.csv" → ("report", ".csv")
                    nam2: str = f"{file.stem}2{file.suffix}"
                    targetpath = targetdir / nam2
                    print(f"⚠️ Target file exists, renaming to: {nam2}")
                
                try:
                    # Create Data folder if it doesn't exist
                    targetdir.mkdir(exist_ok=True, parents=True)
                    file.rename(targetpath)
                    move_counts["data"] += 1
                    print(f"✅ File moved to Data/: {file.name}")
                except Exception as e:
                    print(f"❌ Error moving {file.name}: {str(e)}")
                
                continue  # Skip log check for this file
            
            # Check log file extensions (.log, .json)
            if file.suffix.lower() in [".log", ".json"]:
                targetdir = Path("Logs")
                targetpath = targetdir / file.name
                
                # If file with same name exists in target, add numeric suffix
                if targetpath.exists():
                    nam2 = f"{file.stem}2{file.suffix}"
                    targetpath = targetdir / nam2
                    print(f"⚠️ Target file exists, renaming to: {nam2}")
                
                try:
                    # Create Logs folder if it doesn't exist
                    targetdir.mkdir(exist_ok=True, parents=True)
                    file.rename(targetpath)
                    move_counts["logs"] += 1
                    print(f"✅ File moved to Logs/: {file.name}")
                except Exception as e:
                    print(f"❌ Error moving {file.name}: {str(e)}")
        
        print(f"\n✅ Organization complete: {move_counts['data']} data + {move_counts['logs']} log files sorted")
        return move_counts
        
    except PermissionError:
        print("❌ Permission denied accessing current directory")
        return None
    except Exception as e:
        print(f"❌ Unexpected error in movearquivos(): {str(e)}")
        return None


if __name__ == "__main__":
    # Full project initialization sequence
    print("--- Starting IA-Ops Project Initialization ---\n")
    
    # 1. Create folder structure
    print("Step 1: Creating folder structure...")
    if organizar_projeto():
        print("✅ Folder structure created\n")
    else:
        print("⚠️ Some folders could not be created\n")
    
    # 2. Generate requirements.txt
    print("Step 2: Generating requirements.txt...")
    if gerar_requirements():
        print("✅ Requirements file created\n")
    else:
        print("⚠️ Could not create requirements.txt\n")
    
    # 3. Organize existing files
    print("Step 3: Organizing existing files...")
    results = movearquivos()
    if results:
        print(f"✅ Files organized: {results}\n")
    else:
        print("⚠️ Could not organize files\n")
    
    print("--- Project initialization complete ---")