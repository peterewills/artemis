"""API authentication utilities."""

from fastapi import Header, HTTPException, status
from typing import Optional
from artemis.config import settings


async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> None:
    """
    Verify the API key if one is configured.

    If API_KEY is not set in environment, authentication is disabled.
    If API_KEY is set, requests must include X-API-Key header with matching value.
    """
    # If no API key is configured, skip authentication
    if not settings.api_key:
        return

    # If API key is configured but not provided in request
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="X-API-Key header required"
        )

    # If API key doesn't match
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key"
        )
