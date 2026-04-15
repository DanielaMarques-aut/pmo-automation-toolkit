"""Environment Readiness Verification Module.

Provides pre-flight checks to validate project environment setup and verify
all dependencies are functional before automated job execution.

Checks Performed:
    - Folder Existence: Ensures Data/ folder created (auto-creates if missing)
    - Pandas Status: Validates pandas library is importable and functional
    - Ready Indication: Confirmation when environment is ready for scheduling

Usage Pattern:
    Run this function at startup or before scheduling automated tasks
    to detect configuration issues early and fail fast.

Purpose:
    Pre-flight validation prevents job failures: detect issues before expensive
    operations begin. Scheduled jobs can depend on this check succeeding.

Examples:
    Basic readiness check before scheduling:
    
    >>> is_ready, msg = check_readiness()
    >>> if is_ready:
    ...     schedule_job(time="05:30")
    ... else:
    ...     print(f"Cannot schedule: {msg}")
"""

import os
import pandas as pd
from typing import Tuple


def check_readiness() -> Tuple[bool, str]:
    """Verify environment setup and dependency availability.
    
    Performs startup checks:\n    1. Creates Data/ folder if missing
    2. Validates pandas library is functional
    3. Returns ready status with message
    
    Args:
        None
    
    Returns:
        Tuple[bool, str]: (is_ready, status_message)
            Example: (True, "All checks passed - environment ready for automation")
            Example: (False, "Folder setup failed: Permission denied")
    
    Raises:
        No exceptions. All errors caught and reported in return message.
        Function always completes and returns status.
    
    Notes:
        STARTUP VALIDATION PATTERN:
        Pre-flight checks detect configuration issues before job execution.
        Fail early (check at startup) rather than mid-job (expensive cleanup).
        
        AUTO-CREATE FOLDERS:
        If Data/ folder doesn't exist, creates it automatically with os.makedirs().
        This prevents "Folder not found" errors on first run.
        
        PANDAS FUNCTIONAL TEST:
        Creating a DataFrame is lightweight test that validates:
        - Library import successful
        - No DLL/C-extension loading errors
        - Memory allocation working
    
    Examples:
        Validate environment before scheduling:\n        >>> is_ready, msg = check_readiness()
        >>> if is_ready:
        ...     schedule_morning_job(time=\"05:30\")
        ... else:
        ...     print(f\"Cannot schedule: {msg}\")
        
        Use in main script:
        
        >>> status, message = check_readiness()
        >>> print(f\"Environment check: {message}\")
    """
    print("--- 🛠️ SUNDAY PRE-FLIGHT CHECK ---")
    
    # ============================================================================
    # CHECK 1: Folder Existence
    # ============================================================================
    path: str = r"C:\Users\daniq\carrer\Data"
    
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"✅ Folder created: {path}")
        else:
            print(f"✅ Folder exists: {path}")
    except Exception as e:
        print(f"❌ Error creating folder: {e}")
        return False, f"Folder setup failed: {str(e)}"
    
    # ============================================================================
    # CHECK 2: Pandas Functionality
    # ============================================================================
    try:
        test_df = pd.DataFrame({"Status": ["Ready"]})
        status_value: str = test_df['Status'][0]
        print(f"✅ Pandas Status: {status_value}")
    except Exception as e:
        print(f"❌ Pandas error: {e}")
        return False, f"Pandas check failed: {str(e)}"
    
    # ============================================================================
    # RESULT
    # ============================================================================
    print("\n🚀 Environment ready for 05:30 tomorrow!")
    return True, "All checks passed - environment ready for automation"


if __name__ == "__main__":
    is_ready, message = check_readiness()
    print(f"\nFinal Status: {message}")
