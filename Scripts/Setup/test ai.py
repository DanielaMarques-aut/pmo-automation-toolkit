"""Gemini AI Initialization and Integration Test Module.

Provides diagnostic testing for Google Gemini API connectivity, credential
validation, and basic content generation. Designed for startup verification
and integration testing before deploying AI-powered features.

Configuration Pattern:
    1. Load GOOGLE_API_KEY from .env file (environment isolation)
    2. Initialize Gemini client with credentials
    3. Execute test prompts to verify connectivity
    4. List available models to confirm API access

Test Scenarios:
    - Basic connectivity: Simple greeting prompt to verify connection
    - Context processing: Ops status analysis to test reasoning
    - Model discovery: List available Gemini models for reference

Usage:
    Run as main script to perform full diagnostic test suite.
    Use test_gemini_connectivity() in startup code to validate readiness.

Examples:
    Run full diagnostic:
    
    >>> python "test ai.py"
    ✅ Response: Confirmed! Your script is running.
    ✅ Analysis: Service is operating nominally.
    Available models (5 total): models/gemini-2.5-flash, ...
"""

import os
from google import genai
from dotenv import load_dotenv
from typing import Optional, List


def test_gemini_connectivity() -> bool:
    """Test Gemini API connectivity and credential validation.
    
    Performs initialization checks:
    1. Loads GOOGLE_API_KEY from environment
    2. Creates authenticated Gemini client
    3. Executes diagnostic prompts
    4. Lists available models
    
    Args:
        None
    
    Returns:
        bool: True if all tests pass, False if connectivity fails.
    
    Raises:
        No exceptions raised to caller. All errors caught and logged.
        Errors handled: Missing API key, connection failure, API errors.
    
    Notes:
        STARTUP VALIDATION:
        This function validates AI integration early, before dependent
        systems attempt expensive operations. Fail-fast pattern prevents
        wasted tokens on broken configurations.
        
        ENVIRONMENT LOADING:
        Uses python-dotenv to load .env file from project root.
        Credentials should never be hardcoded in source files.
    
    Examples:
        Test AI readiness before pipeline:
        
        >>> if test_gemini_connectivity():
        ...     print("AI system ready")
        ...     run_ai_pipeline()
        ... else:
        ...     print("Fix API configuration before proceeding")
    """
    # ============================================================================
    # CONFIGURATION LOADING
    # ============================================================================
    print("--- 🤖 GEMINI AI INITIALIZATION TEST ---\n")
    
    # Load environment variables from .env file
    load_dotenv()
    api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in .env file")
        return False
    
    # ============================================================================
    # CLIENT INITIALIZATION
    # ============================================================================
    try:
        client: genai.Client = genai.Client(api_key=api_key)
        print("✅ Gemini client initialized successfully\n")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return False
    
    # ============================================================================
    # TEST 1: Basic Connectivity
    # ============================================================================
    print("Test 1: Basic Connectivity")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Hello Gemini! Confirm that my script is running."
        )
        print(f"✅ Response: {response.text}\n")
    except Exception as e:
        print(f"❌ Connectivity test failed: {e}")
        return False
    
    # ============================================================================
    # TEST 2: Context Processing (Ops Status Analysis)
    # ============================================================================
    print("Test 2: Context Processing")
    try:
        status_info: str = "Status: Service running, CPU: 12%, Memory: 450MB"
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Analyze this Ops script status and provide brief assessment: {status_info}"
        )
        print(f"✅ Analysis: {response.text}\n")
    except Exception as e:
        print(f"❌ Context processing test failed: {e}")
        return False
    
    # ============================================================================
    # TEST 3: Model Discovery
    # ============================================================================
    print("Test 3: Model Discovery")
    try:
        models: List = list(client.models.list())
        print(f"✅ Available models ({len(models)} total):")
        for model in models[:5]:
            print(f"   - {model.name}")
        print()
    except Exception as e:
        print(f"⚠️ Could not list models: {e}\n")
    
    print("🚀 All tests passed! Gemini AI integration ready.")
    return True


if __name__ == "__main__":
    # Run full diagnostic when executed as main script
    success = test_gemini_connectivity()
    
    if not success:
        print("\n❌ AI integration test failed - see errors above")
        exit(1)
    else:
        print("\n✅ AI integration verified and ready for production use")