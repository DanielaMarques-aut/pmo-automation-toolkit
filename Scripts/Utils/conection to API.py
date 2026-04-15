"""API Connection Testing Module.

This module provides utilities for testing HTTP API connectivity using the JSONPlaceholder
public API service. It implements logging-based diagnostics and fail-fast error handling
patterns for network operations.

Key Concepts:
    - Fail-Fast Pattern: Validate connectivity immediately before expensive operations
    - Logging Infrastructure: Track API interactions for debugging and audit trails
    - Public API Testing: JSONPlaceholder provides safe test endpoints without credentials
    - Status Code Validation: Distinguish between successful (200) and error responses

Architecture:
    The module uses Python's requests library for HTTP operations and the logging
    framework for structured event tracking. All network errors are caught and logged
    to prevent cascade failures in dependent systems.

Examples:
    Basic API connectivity test:
    
    >>> test_api_connection()
    ✅ Conexão estabelecida com sucesso!
    Tarefa recebida da Nuvem: delectus aut autem
    
    Error handling when API is unavailable:
    
    >>> test_api_connection()  # (if service down)
    ⚠️ Erro de conexão: Status 500
"""

import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
import logging
from typing import Optional, Dict, Any

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# API CONNECTION FUNCTIONS
# ============================================================================

def test_api_connection(
    url: str = "https://jsonplaceholder.typicode.com/todos/1",
    timeout: int = 5
) -> Optional[Dict[str, Any]]:
    """Test HTTP API connectivity using a public test endpoint.
    
    Establishes a connection with JSONPlaceholder, a public API service designed
    for testing HTTP requests. This function validates network connectivity and
    API response parsing without requiring authentication credentials.
    
    Args:
        url (str): The API endpoint URL to test. Defaults to JSONPlaceholder /todos/1.
            Example: "https://jsonplaceholder.typicode.com/posts/1"
        timeout (int): Request timeout in seconds. Defaults to 5 seconds.
            Example: 10 for slower networks.
    
    Returns:
        Optional[Dict[str, Any]]: Parsed JSON response as dictionary, or None if
            connection failed. Typical response structure for todo endpoint:
            {
                "userId": 1,
                "id": 1,
                "title": "delectus aut autem",
                "completed": False
            }
    
    Raises:
        Handled internally and logged. Does not raise exceptions to caller:
        - ConnectionError: Network layer failure (no internet, DNS failure)
        - Timeout: Server took too long to respond
        - HTTPError: Non-200 status codes from server
        - ValueError: Response body is not valid JSON
    
    Notes:
        CLEAN CODE PRINCIPLE - Fail Early:
        This function validates connectivity before dependent systems attempt
        expensive operations. API failures are logged with context (status code,
        exception type) for troubleshooting.
        
        ARCHITECTURE PATTERN - Network Resilience:
        Production systems should wrap this in retry logic with exponential backoff.
        Current implementation provides single attempt with comprehensive logging.
    
    Examples:
        Successful connection:
        
        >>> data = test_api_connection()
        >>> if data:
        ...     print(f"Task: {data['title']}")
        ...     # Output: Task: delectus aut autem
        
        Custom endpoint test:
        
        >>> post_data = test_api_connection(
        ...     url="https://jsonplaceholder.typicode.com/posts/1"
        ... )
        >>> post_data.get('id')
        1
        
        Connection failure handling:
        
        >>> result = test_api_connection(timeout=0.001)  # Will timeout
        >>> if result is None:
        ...     print("API unreachable - check network or endpoint")
    """
    logger.info(f"🌐 Initiating API connectivity test to: {url}")
    
    try:
        # Execute HTTP GET request with timeout protection
        response = requests.get(url, timeout=timeout)
        
        # Validate HTTP status code (200-299 range indicates success)
        if response.status_code == 200:
            # Parse JSON response body
            data: Dict[str, Any] = response.json()
            logger.info("✅ API connection established successfully!")
            print(f"✅ Data received from cloud: {data.get('title', 'No title')}")
            return data
        else:
            # Non-2xx response indicates server-side error or not found
            logger.warning(
                f"⚠️ Connection error: HTTP {response.status_code} - "
                f"{response.reason}"
            )
            print(f"⚠️ Connection error: HTTP {response.status_code}")
            return None
            
    except Timeout:
        # Request exceeded timeout threshold (network slow or service unresponsive)
        logger.error(f"⏱️ Connection timeout after {timeout}s - API may be slow")
        print(f"⏱️ Connection timeout - server did not respond within {timeout}s")
        return None
        
    except ConnectionError as ce:
        # Network layer failure (no internet, DNS failure, connection refused)
        logger.error(f"🔗 Network connection failure: {str(ce)}")
        print(f"🔗 Network error - cannot reach API endpoint")
        return None
        
    except ValueError as ve:
        # Response body is not valid JSON
        logger.error(f"📄 Invalid JSON response: {str(ve)}")
        print(f"📄 API returned invalid data format")
        return None
        
    except RequestException as re:
        # Catch-all for requests library exceptions
        logger.error(f"💥 Critical API failure: {str(re)}")
        print(f"💥 Unexpected error contacting API: {type(re).__name__}")
        return None


if __name__ == "__main__":
    # Run connectivity test with default public API endpoint
    result = test_api_connection()
    if result:
        logger.info(f"Response contains {len(result)} fields")