"""
API Key authentication for DevAssist
"""
from fastapi import Header, HTTPException, status, Request
from config import settings


class AuthenticationError(Exception):
    """Custom exception for authentication failures"""
    pass


async def verify_api_key(
    request: Request,
    x_api_key: str = Header(None, description="API Key for authentication")
) -> str:
    """
    Verify API key from request header
    
    Args:
        request: FastAPI request object
        x_api_key: API key from X-API-Key header
        
    Returns:
        The validated API key
        
    Raises:
        HTTPException: If API key is invalid or missing
    """
    # Allow OPTIONS requests (CORS preflight) without authentication
    if request.method == "OPTIONS":
        return "preflight"
    
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    valid_keys = settings.api_keys_list
    
    if x_api_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    return x_api_key


def get_api_key_header():
    """
    Dependency function to get API key from header
    Can be used as a dependency in route decorators
    """
    return Header(..., alias="X-API-Key", description="API Key for authentication")

# Made with Bob
