"""Project Structure Initialization and File Organization Module.

Provides utilities for creating standardized project directories and managing
file organization by type (data, logs, scripts). Implements professional
project scaffolding patterns used in production systems.

Key Functionality:
    1. organizar_projeto() - Create standard project folder structure
    2. gerar_requirements() - Generate requirements.txt from library list
    3. movearquivos() - Organize files by extension into appropriate folders

Project Structure Created:
    ├── data/      (datasets, CSV, Excel files)
    ├── logs/      (log files, error messages)
    ├── scripts/   (Python scripts, utilities)
    ├── archive/   (old versions, backups)
    └── requirements.txt (dependency manifest)

Architecture Pattern:
    This module follows Single Responsibility Principle with three independent:
    - organizar_projeto(): Creates folder structure
    - gerar_requirements(): Generates dependency manifest
    - movearquivos():  Organizes existing files by type

File Organization Strategy:
    Data files (.csv, .xlsx) → data/ folder
    Log files (.log, .json)  → logs/ folder
    Others remain in place   → Requires manual organization
    
    If target file already exists, appends numeric suffix: file.csv → file2.csv

Use Cases:
    - Initialize new Python projects with standard structure
    - Organize messy data folders after bulk exports
    - Setup workflow before running analysis pipelines
    - Quick project scaffolding for teams

Examples:
    Initialize new project with complete setup:
    
    >>> organizar_projeto()
    >>> gerar_requirements()
    >>> movearquivos()
    >>> # Result: Folders created, requirements.txt generated, files organized
    
    Create structure only:
    
    >>> organizar_projeto()
    >>> # Result: Empty folder structure ready for use
"""

from pathlib import Path
from typing import List, Optional, Dict


def organizar_projeto() -> bool:
    """Create standard folder structure for Python projects.
    
    Establishes a professional directory hierarchy following industry best
    practices. Provides clear separation of concerns and enables team members
    to quickly understand project organization.
    
    Folders Created:
        - data        (Input and output datasets)
        - logs        (Application logs and audit trails)
        - scripts     (Core project code)
        - archive     (Old versions and backups)
    
    Args:
        None
    
    Returns:
        bool: True if all folders created successfully, False if errors occurred.
    
    Raises:
        No exceptions raised. PermissionError caught and logged to console.
        Function continues even if some folders cannot be created.
    
    Notes:
        IDEMPOTENCY:
        This function is safe to call multiple times. If folders already exist,
        the Path.exists() check prevents errors and avoids duplicate messages.
        
        SCALABILITY:
        This structure accommodates projects from startup to enterprise scale:
        - Single developer: One scripts folder for all analysis
        - Team project: Multiple subfolders per category for parallel work
        - Production system: Separate data sources from processed outputs
        
        NAMING CONVENTION:
        Folder names use singular (data, logs, scripts) rather than plural.
        This is preferred in professional projects and tool conventions
        (e.g., "src" not "sources", "bin" not "binaries", "data" not "datasets").
    
    Examples:
        Initialize project structure:
        
        >>> success = organizar_projeto()
        >>> if success:
        ...     print("Project ready for development")
        ... else:
        ...     print("Some folders could not be created - check permissions")
        
        Check created structure:
        
        >>> organizar_projeto()
        >>> Path("scripts").exists()
        True
    """
    # List of top-level directories to create
    pastas: List[str] = ["data", "logs", "scripts", "archive"]
    
    success: bool = True
    
    for pasta in pastas:
        try:
            p: Path = Path(pasta)
            if not p.exists():
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
    
    Dependencies Listed (Examples from typical projects):
        - pandas          (Data manipulation and analysis)
        - requests        (HTTP API client)
        - python-dotenv   (Environment variable management)
        - openpyxl        (Excel file manipulation)
    
    Args:
        None
    
    Returns:
        bool: True if requirements.txt created successfully, False if write failed.
    
    Raises:
        No exceptions raised. IOError caught and logged to console.
    
    Notes:
        DEPENDENCY MANAGEMENT:
        Starting with a basic list of core libraries enables quick setup.
        As the project grows, manually add additional dependencies or use:
        
            pip freeze > requirements.txt
        
        This command automatically exports all installed packages in your
        current environment to requirements.txt.
        
        VERSION PINNING:
        Production-grade requirements.txt should include version constraints:
        
            pandas==1.5.3
            requests>=2.28.0
            openpyxl~=3.1.0
        
        This prevents breaking changes when team members upgrade.
        Current implementation omits versions - adapt for production.
    
    Examples:
        Generate requirements.txt:
        
        >>> gerar_requirements()
        ✅ File requirements.txt generated.
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
    # Core libraries used in typical PM automation project
    libs: List[str] = [
        "pandas",               # Data analysis and manipulation
        "requests",             # HTTP client for APIs
        "python-dotenv",        # Environment variable management
        "openpyxl"              # Excel file reading/writing/formatting
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
        Extensions (.xlsx, .csv) → data/ folder
        Extensions (.log, .json)  → logs/ folder
        Others                    → Remain in place
    
    Rename Strategy:
        If target directory already contains a file with the same name,
        append numeric suffix before extension:
        
            project.csv (in data/) + project.csv (source) = project2.csv
            report.json (in logs/) + report.json (source) = report2.json
    
    Args:
        None
    
    Returns:
        Optional[Dict[str, int]]: Dictionary with move counts by category:
            {
                "data": 3,  (Files moved to data/)
                "logs": 2   (Files moved to logs/)
            }
            Returns None if current directory cannot be read.
    
    Raises:
        No exceptions raised to caller. Individual file move errors caught,
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
        Consider renaming strategy for production (timestamps, git hashes).
        
        IDEMPOTENCY CONCERN:
        Running this function twice on same directory behaves differently:
        First run: report.csv → data/report.csv
        Second run: Checks data/ exists and has report.csv, renames to report2.csv
        
        This is intentional to prevent data loss but may surprise users.
    
    Examples:
        Organize mixed files in project root:
        
        >>> # Current directory contains: project.csv, errors.log, config.json, README.md
        >>> results = movearquivos()
        >>> # Output:
        >>> # File moved to data/: project.csv
        >>> # File moved to logs/: errors.log
        >>> # File moved to logs/: config.json
        >>> # README.md remains in place
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
                targetdir: Path = Path("data")
                targetpath: Path = targetdir / file.name
                
                # If file with same name exists in target, add numeric suffix
                if targetpath.exists():
                    # Split filename and extension: "report.csv" → ("report", ".csv")
                    nam2: str = f"{file.stem}2{file.suffix}"
                    targetpath = targetdir / nam2
                    print(f"⚠️ Target file exists, renaming to: {nam2}")
                
                try:
                    # Create data folder if it doesn't exist
                    targetdir.mkdir(exist_ok=True, parents=True)
                    file.rename(targetpath)
                    move_counts["data"] += 1
                    print(f"✅ File moved to data/: {file.name}")
                except Exception as e:
                    print(f"❌ Error moving {file.name}: {str(e)}")
                
                continue  # Skip log check for this file
            
            # Check log file extensions (.log, .json)
            if file.suffix.lower() in [".log", ".json"]:
                targetdir = Path("logs")
                targetpath = targetdir / file.name
                
                # If file with same name exists in target, add numeric suffix
                if targetpath.exists():
                    nam2 = f"{file.stem}2{file.suffix}"
                    targetpath = targetdir / nam2
                    print(f"⚠️ Target file exists, renaming to: {nam2}")
                
                try:
                    # Create logs folder if it doesn't exist
                    targetdir.mkdir(exist_ok=True, parents=True)
                    file.rename(targetpath)
                    move_counts["logs"] += 1
                    print(f"✅ File moved to logs/: {file.name}")
                except Exception as e:
                    print(f"❌ Error moving {file.name}: {str(e)}")
        
        print(f"\n✅ Organization complete: {move_counts['data']} data + {move_counts['logs']} log files sorted")
        return move_counts
        
    except PermissionError:
        print("❌ Permission denied accessing current directory")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return None


if __name__ == "__main__":
    # Full project initialization sequence
    print("--- Project Initialization Sequence ---\n")
    
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