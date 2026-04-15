"""Environment Readiness Verification Module (Verbose Test Version).

Simplified pre-flight checks with verbose output for troubleshooting.
More detailed than folder_setup.py for development and debugging purposes.

Approach:
    - Direct execution (no function wrapper) for quick testing
    - Verbose status messages for each check
    - Ideal for manual verification before automation
    - Better for development; use folder_setup.py for production scheduling

Usage:
    Run directly for verbose environment diagnostics:
    
    >>> python teste.py
    --- 🛠️ SUNDAY PRE-FLIGHT CHECK ---
    Timestamp: 2026-04-15T14:30:45.123456
    Checking path: C:\\Users\\daniq\\carrer\\Data
    ✅ Folder exists: C:\\Users\\daniq\\carrer\\Data!
    ✅ Pandas Status: Ready
    
    🚀 Environment ready for 05:30 tomorrow!
"""

import os
import pandas as pd
from datetime import datetime


def check_readiness_verbose() -> bool:
    """Perform detailed environment readiness check with verbose output.
    
    Equivalent to folder_setup.check_readiness() but with explicit status
    messages for each step. Useful for development and debugging.
    
    Args:
        None
    
    Returns:
        bool: True if all checks pass, False otherwise.
    
    Raises:
        No exceptions. All errors caught and reported.
    
    Notes:
        VERBOSE TESTING:
        This function prints status for every operation, making it suitable
        for manual testing and debugging. For production scheduling, use
        the simpler folder_setup.check_readiness() instead.
        
        IDEMPOTENCY:
        Safe to call multiple times. Creates folder only if missing,
        prints exists message if already present.
    
    Examples:
        Use in test suite:
        
        >>> success = check_readiness_verbose()
        >>> assert success, "Environment not ready"
    """
    print("--- 🛠️ SUNDAY PRE-FLIGHT CHECK ---")
    print(f"Timestamp: {datetime.now().isoformat()}\n")
    
    # ============================================================================
    # CHECK 1: Verify Data Folder Path
    # ============================================================================
    path: str = r"C:\Users\daniq\carrer\Data"
    print(f"Checking path: {path}")
    
    try:
        # Create folder if missing
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"✅ Folder created: {path}!")
        
        # Verify folder now exists
        if os.path.exists(path):
            print(f"✅ Folder exists: {path}!")
        else:
            print(f"❌ Folder creation failed - path does not exist")
            return False
            
    except Exception as e:
        print(f"❌ Error accessing folder: {e}")
        return False
    
    # ============================================================================
    # CHECK 2: Test Pandas Functionality
    # ============================================================================
    try:
        test_df = pd.DataFrame({"Status": ["Ready"]})
        status_value: str = test_df['Status'][0]
        print(f"✅ Pandas Status: {status_value}")
    except Exception as e:
        print(f"❌ Pandas error: {e}")
        return False
    
    # ============================================================================
    # RESULT
    # ============================================================================
    print("\n🚀 Environment ready for 05:30 tomorrow!")
    return True


if __name__ == "__main__":
    # Direct execution for testing
    success = check_readiness_verbose()
    
    if success:
        print("\n✅ All checks passed")
        exit(0)
    else:
        print("\n❌ Some checks failed")
        exit(1)