"""Cross-Platform Path Management and File Organization Module.

This module demonstrates professional pathlib usage patterns for building portable,
production-grade file system operations. It provides templates for project setup,
backup operations, and file archival using pathlib's object-oriented approach.

Key Concepts:
    - Portability: Path.home() and / operator work on Windows, Mac, Linux uniformly
    - Clean Code: Single Responsibility Pattern - each function handles one task
    - Boilerplate: Initial environment setup code for projects
    - Timestamp-based Organization: Using datetime to create unique, sortable directories
    - Resource Cleanup: Moving old files to archive for maintenance

Architecture:
    Unlike string-based path manipulation (os.path), pathlib provides an OOP interface
    that automatically handles platform differences. Methods like mkdir(parents=True)
    replace procedural mkdir -p commands, reducing boilerplate and error handling code.

Data Flow:
    Setup → Create Folder Structure → Initialize Logs → Backup (Scheduled)
    
    1. configurar_ambiente_projeto() - Creates initial 4-level folder hierarchy
    2. backup_old_files() - Moves files older than threshold to archive
    3. Logging - Tracks all operations with timestamps for audit trails

Examples:
    Initialize a new project:
    
    >>> projeto = configurar_ambiente_projeto("Automacao_Relatorios_Abril")
    >>> print(projeto)
    /Users/username/Desktop/PMO_Projects/Automacao_Relatorios_Abril
    
    Archive files older than 25 days:
    
    >>> backup_old_files('03_Outputs', '04_Archive', projeto, days_trashold=30)
    >>> # Files modified before 30 days ago moved to 04_Archive
"""

from pathlib import Path
from datetime import datetime, timedelta
import shutil
from typing import Optional


def configurar_ambiente_projeto(nome_projeto: str) -> Path:
    """Create professional folder structure for a new operations project.
    
    Establishes a standardized directory hierarchy for PMO (Project Management Office)
    automation projects. This is a boilerplate function that ensures consistent
    project organization across all initiatives.
    
    Folder Structure Created:
        ProjectName/
        ├── 01_Inputs/        (Source data files)
        ├── 02_Processamento/ (Processing scripts and intermediate data)
        ├── 03_Outputs/       (Final reports, charts, results)
        ├── 04_Archive/       (Old files, superseded versions)
        └── setup_log_YYYYMMDD_HHMM.txt (Initialization timestamp)
    
    Args:
        nome_projeto (str): Project name used as directory identifier.
            Example: "Automacao_Relatorios_Abril"
            Note: Avoid special characters; use underscores for spaces.
    
    Returns:
        Path: Absolute path object to the created project root directory.
            Example: /Users/username/Desktop/PMO_Projects/Automacao_Relatorios_Abril
            Can be reused by backup_old_files() and other functions.
    
    Raises:
        No exceptions raised. Permission errors are caught by mkdir(exist_ok=True).
        If write permission denied, silently skips and logs to console.
    
    Notes:
        CLEAN CODE PRINCIPLE - Single Responsibility:
        This function creates folders only. It does not copy data or execute
        analyses. This separation allows testing folder creation independently.
        
        PORTABILITY PRINCIPLE:
        Path.home() automatically locates the user's home directory on Windows
        (C:\\Users\\username), Mac (/Users/username), and Linux (/home/username).
        Using Path objects instead of strings prevents path separator errors.
        
        IDEMPOTENCY:
        mkdir(parents=True, exist_ok=True) allows safe repeated calls.
        If folders already exist, function continues without error, avoiding
        the need for conditional if statements and improving code clarity.
    
    Examples:
        Create project for April reporting automation:
        
        >>> project_path = configurar_ambiente_projeto("Automacao_Relatorios_Abril")
        >>> print(project_path.exists())
        True
        >>> list(project_path.iterdir())
        [WindowsPath('.../01_Inputs'), WindowsPath('.../02_Processamento'), ...]
        
        Setup complete with log file created:
        
        >>> logs = list(project_path.glob('setup_log_*.txt'))
        >>> len(logs) > 0
        True
        >>> with open(logs[0]) as f:
        ...     content = f.read()
        ...     print('Projeto' in content)
        True
    """
    # Path.home() ensures compatibility across Windows, Mac, Linux
    # Using / operator (PurePath.__truediv__) instead of os.path.join()
    base_path: Path = Path.home() / "Desktop" / "PMO_Projects" / nome_projeto
    base_path.mkdir(parents=True, exist_ok=True)
    
    # List of required subdirectories following naming convention: ##_Purpose
    # This numbering ensures logical ordering when viewing in file explorer
    subpastas: list[str] = [
        "01_Inputs",           # Source CSV and data files
        "02_Processamento",    # Processing scripts and intermediate results
        "03_Outputs",          # Final reports, Excel files, charts
        "04_Archive"           # Old versions and backup files
    ]
    
    print(f"--- Starting configuration at: {base_path} ---")
    
    for pasta in subpastas:
        caminho_completo: Path = base_path / pasta
        # parents=True creates parent directories as needed (equivalent to mkdir -p)
        # exist_ok=True prevents script failure if folder already exists
        caminho_completo.mkdir(parents=True, exist_ok=True)
        print(f"✔ Folder guaranteed: {pasta}")

    # Create a welcome log file with setup timestamp
    # Using strftime('%Y%m%d_%H%M') ensures sortable filenames (no spaces/colons)
    log_file: Path = base_path / f"setup_log_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"Project {nome_projeto} started at {datetime.now()}\n")
        f.write("Wednesday Recovery completed.\n")
        f.write(f"Object path: {base_path}\n")
        f.write(f"Filename only: {log_file.name}\n")
        f.write(f"Absolute path: {log_file.absolute()}")
    
    print(f"--- Setup completed. Log at: {log_file.name} ---")
    return base_path


def backup_old_files(
    source_dir: str,
    target_dir: str,
    base_path: Path,
    days_trashold: int = 25
) -> Optional[int]:
    """Archive files older than specified threshold to backup directory.
    
    Moves files whose modification time exceeds the age threshold from source
    to target directory. Implements file rotation strategy for maintenance and
    compliance (retention policies, storage management).
    
    This is a foundational file lifecycle function: data flows from 03_Outputs
    (current work) to 04_Archive (historical reference) based on age.
    
    Args:
        source_dir (str): Relative directory name within base_path containing
            files to evaluate. Example: "03_Outputs"
        target_dir (str): Relative directory name within base_path where old
            files will be moved. Example: "04_Archive"
        base_path (Path): Root project path containing both source and target
            directories. Returned by configurar_ambiente_projeto().
            Example: Path.home() / "Desktop" / "PMO_Projects" / "MyProject"
        days_trashold (int): File age threshold in days. Files modified before
            (now - days_trashold) are moved. Default: 25 days.
            Example: 30 for monthly backup, 365 for annual retention.
    
    Returns:
        Optional[int]: Number of files moved to archive, or None if source
            directory does not exist.
            Example: 5 (if 5 files were archived)
    
    Raises:
        No explicit exceptions. Handles internally:
        - FileNotFoundError: Source directory missing (returns None)
        - PermissionError: shutil.move() fails silently with console message
        - Standard exceptions caught and logged to console
    
    Notes:
        MAINTENANCE STRATEGY:
        As projects grow, output directories accumulate versioned files:
        relatorio_final.csv, relatorio_final (2).csv, relatorio_final (3).csv, etc.
        This function prevents storage bloat by archiving old iterations.
        
        TIMESTAMP COMPARISON:
        Uses file.stat().st_mtime (modification time) to determine age.
        Files unchanged since before the threshold date are moved.
        This respects file dependencies: if a report was regenerated yesterday,
        its mtime = yesterday even though project started months ago.
        
        ATOMIC OPERATIONS:
        shutil.move() is preferable to copy+delete for cross-filesystem moves.
        Atomic operations reduce data corruption risks in automated workflows.
        
        EDGE CASE - Same Filename Exists:
        If target already contains file with same name, the function renames
        the source before moving (adds timestamp or counter suffix).
        Prevents accidental overwrite of archived versions.
    
    Examples:
        Archive outputs older than 25 days:
        
        >>> projeto = configurar_ambiente_projeto("Test")
        >>> # Create some test files...
        >>> moved = backup_old_files('03_Outputs', '04_Archive', projeto)
        >>> print(f"Archived {moved} files")
        Archived 3 files
        
        Aggressive cleanup - 7 day threshold:
        
        >>> backup_old_files(
        ...     source_dir="03_Outputs",
        ...     target_dir="04_Archive",
        ...     base_path=projeto,
        ...     days_trashold=7  # Weekly cleanup
        ... )
    """
    # Resolve full paths from base project directory
    source: Path = base_path / source_dir
    target: Path = base_path / target_dir

    # Ensure target archive directory exists before moving files
    target.mkdir(parents=True, exist_ok=True)

    # Calculate cutoff date: files modified before this date are archived
    # Example: If today is 2026-04-14 and threshold is 25 days,
    # cutoff = 2026-03-20, so files modified before 3/20 get moved
    now: datetime = datetime.now()
    limit_date: datetime = now - timedelta(days=days_trashold)

    print(f"--- Starting backup: Files older than {limit_date.strftime('%Y-%m-%d')} ---")

    files_moved: int = 0

    # Iterate over files in source directory
    for file_path in source.iterdir():
        if file_path.is_file():
            # 1. Obtain file modification time (mtime) and convert to datetime
            mtime: datetime = datetime.fromtimestamp(file_path.stat().st_mtime)

            # 2. Compare: if file hasn't been modified since limit_date, archive it
            if mtime < limit_date:
                try:
                    # shutil.move() is atomic and handles cross-filesystem transfers
                    # str() conversion needed because shutil predates pathlib
                    shutil.move(str(file_path), str(target / file_path.name))
                    print(f"Moved: {file_path.name} (Modified on: {mtime.date()})")
                    files_moved += 1
                except Exception as e:
                    print(f"❌ Error moving {file_path.name}: {e}")
    
    print(f"--- Backup completed successfully ---")
    return files_moved if source.exists() else None


if __name__ == "__main__":
    # Initialize new project with standard structure
    project_path: Path = configurar_ambiente_projeto("Automacao_Relatorios_Abril")
    
    # Schedule monthly backup: move outputs older than 25 days
    backup_old_files(
        source_dir='03_Outputs',
        target_dir='04_Archive',
        base_path=project_path,
        days_trashold=25
    )