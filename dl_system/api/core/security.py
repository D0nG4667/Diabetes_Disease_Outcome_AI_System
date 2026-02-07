from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    """
    Validate API Key query parameter or header.
    """
    if settings.API_KEY:
        if not api_key:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API Key header 'X-API-Key' missing",
            )
        if api_key != settings.API_KEY:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
    return api_key
