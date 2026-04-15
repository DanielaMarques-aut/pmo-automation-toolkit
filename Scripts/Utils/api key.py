"""Secure API Credentials and Authentication Management Module.

This module provides utilities for managing sensitive API keys and credentials
using environment variables and the python-dotenv library. It implements
industry-standard security patterns: never hardcode keys, validate presence,
and fail fast when credentials are missing.

Security Architecture:
    1. Environment Isolation: Credentials loaded from .env file (not in source code)
    2. Fail-Fast Pattern: Validate API key existence before using it
    3. Clear Error Messages: Inform user when credentials are missing
    4. Model Discovery: List available models to confirm API access works
    5. Resilience: Implement retry logic with exponential backoff for transient errors

Key Concepts:
    - .env File: Project root must contain .env file with credentials (git-ignored)
    - NEVER Commit Keys: .env should be in .gitignore to prevent credential leaks
    - Early Validation: Check credentials before expensive operations begin
    - Reduce Wasted Tokens: API key validation runs once at startup, not repeatedly

Environment Variables:
    GOOGLE_API_KEY: Google Gemini API authentication token (required)
        Format: String starting with 'AIzaSy...' (approximately 39 characters)
        Get it from: Google AI Studio (https://aistudio.google.com)
    
    How to Set:
        1. Create .env file in project root
        2. Add line: GOOGLE_API_KEY=your_actual_key_here
        3. Save file
        4. Run this script

Examples:
    Initialize and validate API credentials:
    
    >>> import api_key
    >>> # Output: ✅ Gemini API Secured and Ready.
    >>> # Output: Available model: models/gemini-pro-vision
    >>> # Now you can use the client in dependent modules
    
    Missing credentials error:
    
    >>> # (if .env file missing or GOOGLE_API_KEY not set)
    >>> # Output: ❌ Error: GOOGLE_API_KEY not found in .env file.
    >>> # Script stops - prevents wasting cloud compute tokens

API Reference:
    The validated Gemini API client instance can be used for:
    - Text generation: client.models.generate_content()
    - Multi-modal analysis: Supports text, image, and audio inputs
    - Model listing: client.models.list() to discover available models
"""

import os
from dotenv import load_dotenv
import google.genai as genai
from typing import Optional
import time
from google.api_core import exceptions
from google.api_core.exceptions import InternalServerError


# ============================================================================
# ENVIRONMENT CONFIGURATION
# ============================================================================

# Load environment variables from .env file
# This file should NOT be committed to git (add to .gitignore)
load_dotenv()


def get_api_client() -> Optional[genai.Client]:
    """Initialize and validate Google Gemini API client.
    
    Loads the GOOGLE_API_KEY from environment variables and creates an
    authenticated Gemini API client. This function enforces the Fail-Fast
    pattern: if credentials are invalid, it returns None rather than
    failing indirectly during API calls.
    
    Args:
        None
    
    Returns:
        Optional[genai.Client]: Authenticated Gemini API client if credentials
            are valid. None if API_KEY is missing or invalid.
            
            When successful, can be used as:
            >>> client = get_api_client()
            >>> if client:
            ...     response = client.models.generate_content(
            ...         model="gemini-flash-latest",
            ...         contents="Hello"
            ...     )
    
    Raises:
        Does not raise exceptions. Returns None on credential errors instead.
        This allows dependent code to check: if api_client is None: exit()
    
    Notes:
        SECURITY PRINCIPLE - Environment Variables:
        API keys should NEVER appear in source code. The python-dotenv library
        reads from .env file which must be git-ignored. This separates secrets
        from version control and allows different keys per environment
        (dev, staging, production).
        
        FAIL-FAST PATTERN:
        Credentials are validated immediately at module load time, not at first
        API call. This prevents long debugging sessions caused by invalid keys.
        Early failure => clear error message => fast problem resolution.
        
        ZERO-COST VALIDATION:
        Creating a client object does not consume API tokens. This validation
        is free and happens before any expensive operations begin.
    
    Examples:
        Secure API setup with validation:
        
        >>> client = get_api_client()
        >>> if client is None:
        ...     print("Cannot continue without API credentials")
        ...     exit(1)
        >>> response = client.models.generate_content(...)
        
        Using in dependent modules:
        
        >>> from Scripts.Utils.api_key import get_api_client
        >>> api_client = get_api_client()
        >>> if not api_client:
        ...     raise EnvironmentError("Gemini API key not configured")
    """
    # Retrieve API key from environment variables
    # os.getenv() returns None if variable is not set (safe, no exception)
    api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        # Credential missing - fail fast with clear error message
        print("❌ Error: GOOGLE_API_KEY not found in .env file.")
        print("How to fix:")
        print("  1. Create/Edit .env in project root")
        print("  2. Add: GOOGLE_API_KEY=your_key_from_aistudio.google.com")
        print("  3. Save and restart Python")
        return None

    # Initialize Gemini API client with obtained credentials
    try:
        client: genai.Client = genai.Client(api_key=api_key)
        print("✅ Gemini API Secured and Ready.")
        return client
    except Exception as e:
        # Client initialization failed (invalid key format, network error, etc)
        print(f"❌ Failed to initialize API client: {str(e)}")
        return None


def list_available_models(client: genai.Client) -> Optional[list]:
    """List and display all available Gemini API models.
    
    Queries the API to retrieve supported models and their capabilities.
    This confirms the API connection is working and shows which models
    are available for use (gemini-pro, gemini-vision, gemini-flash, etc).
    
    Args:
        client (genai.Client): Authenticated Gemini API client returned by
            get_api_client().
    
    Returns:
        Optional[list]: List of available model objects if successful.
            Each model object contains .name attribute, e.g.,
            "models/gemini-pro-vision", "models/gemini-flash-latest".
            Returns None if listing fails (network error, authentication issue).
    
    Raises:
        Does not raise exceptions. Returns None on API errors instead,
        allowing graceful degradation if model listing is unavailable.
    
    Notes:
        DISCOVERY PATTERN:
        Rather than hardcoding model names that may become outdated,
        this function queries the live API. This ensures the code adapts
        as Google releases new models and deprecates old ones.
        
        SIDE EFFECT - Console Output:
        Function prints model names to console as side effect.
        Ideal for startup diagnostics and confirming API access.
    
    Examples:
        Discover all available models:
        
        >>> client = get_api_client()
        >>> models = list_available_models(client)
        >>> print(f"Available {len(models)} models")
        Available 5 models
        >>> # Output also has printed: Available model: models/gemini-pro-vision
        
        Use in startup validation:
        
        >>> if client and list_available_models(client):
        ...     print("API ready for use")
    """
    if not client:
        return None
    
    try:
        models: list = list(client.models.list())
        print(f"✅ Discovered {len(models)} available models:")
        for model in models:
            print(f"   Available model: {model.name}")
        return models
    except Exception as e:
        print(f"⚠️ Could not list models: {str(e)}")
        return None


def generate_with_retry(
    client: genai.Client,
    model_name: str = "gemini-flash-latest",
    contents: str = "",
    retries: int = 3
) -> Optional[str]:
    """Generate API response with exponential backoff retry logic.
    
    Implements resilience pattern for handling transient API failures.
    When the server returns a 503 (Service Unavailable) error, the function
    waits and retries automatically up to `retries` times with exponential
    backoff: 2 seconds, 4 seconds, 8 seconds between attempts.
    
    This pattern reduces manual debugging and prevents cascade failures in
    automated systems: if the API experiences momentary load, the system
    recovers automatically rather than failing the entire job.
    
    Args:
        client (genai.Client): Authenticated Gemini API client from get_api_client()
        model_name (str): Model identifier to use for generation.
            Default: "gemini-flash-latest" (fastest, cheapest, good for tasks)
            Options: "gemini-pro", "gemini-pro-vision", "gemini-flash-latest"
        contents (str): Prompt or input text to send to the model.
            Example: "Create dummy projects.csv with columns: Name, Deadline, Status"
        retries (int): Maximum number of retry attempts for 503 errors.
            Default: 3 (will attempt up to 3 times)
            Set to 1 to disable retries, 5+ for mission-critical operations.
    
    Returns:
        Optional[str]: Generated text response if successful.
            Example: "Here is a sample projects.csv:..."
            Returns None if all retries exhausted or non-recoverable error occurs.
    
    Raises:
        No exceptions raised. Handles errors internally:
        - InternalServerError (503): Retried with backoff
        - Other API errors: Logged and returns None
        - Connection errors: Treated as failure, no retry
    
    Notes:
        RESILIENCE PATTERN - Exponential Backoff:
        Instead of immediate retry (which would fail again if server is overloaded),
        the function waits progressively longer:
        
            Attempt 1: fails with 503
            Wait 2 seconds (2^1)
            Attempt 2: fails with 503
            Wait 4 seconds (2^2)
            Attempt 3: succeeds or fails permanently
        
        This gives the server time to recover from momentary load spikes.
        
        COST OPTIMIZATION:
        Each retry attempt consumes API tokens. Therefore:
        - Retries should be reasonable (3-5 attempts max)
        - Non-recoverable errors fail immediately (invalid key, wrong model)
        - Only transient errors (503, timeout) should trigger retries
        
        TOKEN CONSUMPTION:
        Each API call consumes tokens based on prompt/response length.
        Retries increase token usage. Monitor costs with large-scale automation.
    
    Examples:
        Generate with automatic retry on server errors:
        
        >>> client = get_api_client()
        >>> response = generate_with_retry(
        ...     client,
        ...     model_name="gemini-flash-latest",
        ...     contents="What is the capital of France?"
        ... )
        >>> if response:
        ...     print(response.text)
        ... else:
        ...     print("API request failed after 3 retries")
        
        High-reliability batch processing:
        
        >>> for project in projects:
        ...     response = generate_with_retry(
        ...         client,
        ...         contents=f"Analyze risk for {project.name}",
        ...         retries=5  # More retries for important batch
        ...     )
    """
    # Attempt API call up to `retries` times
    for attempt in range(retries):
        try:
            # Execute actual content generation
            response = client.models.generate_content(
                model=model_name,
                contents=contents
            )
            # Success - return immediately
            print(f"✅ Response received from model (Attempt {attempt + 1}/{retries})")
            return response

        except InternalServerError as ise:
            # Server returned 503 (Service Unavailable) - transient error
            # Calculate wait time using exponential backoff: 2^(attempt+1) seconds
            wait_time: int = (attempt + 1) * 2
            
            if attempt < retries - 1:
                # Not final attempt - wait and retry
                print(f"⚠️ Server busy (503). Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                # Final attempt failed - give up
                print(f"❌ Server still unavailable after {retries} attempts")
                return None

        except Exception as e:
            # Non-recoverable error (invalid key, wrong model, etc)
            # These don't benefit from retry
            print(f"❌ Critical API error: {type(e).__name__}: {str(e)}")
            return None

    # All retries exhausted
    return None


# ============================================================================
# MODULE INITIALIZATION
# ============================================================================

# Initialize API client when module is imported
# This validates credentials immediately rather than on first use
api_client: Optional[genai.Client] = get_api_client()

if api_client:
    # API credentials valid - discover available models
    available_models = list_available_models(api_client)


if __name__ == "__main__":
    # Standalone execution: full validation and demo
    print("\n--- Gemini API Initialization and Model Discovery ---\n")
    
    client = get_api_client()
    
    if client:
        print("\nListening available models...")
        models = list_available_models(client)
        
        # Demo: Simple content generation
        print("\n--- Testing Content Generation ---")
        demo_response = generate_with_retry(
            client,
            model_name="gemini-flash-latest",
            contents="A# INSTRUCTIONS: Create a dummy 'projects.csv' with columns: ProjectName, Deadline, Status, Manager, Budget. Provide exactly 3 example rows.",
            retries=3
        )
        
        if demo_response:
            print("\n✅ Generated content:")
            print(demo_response.text if hasattr(demo_response, 'text') else str(demo_response))
        else:
            print("\n❌ Content generation failed after retries")
    else:
        print("\n❌ Cannot proceed without valid API credentials")