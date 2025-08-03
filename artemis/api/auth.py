"""API authentication utilities."""

import os
from fastapi import Header, HTTPException, status
from typing import Optional


async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> None:
    """
    Verify the API key.

    ARTEMIS_API_KEY must be set in environment.
    Requests must include X-API-Key header with matching value.
    """
    # Get API key from environment (required to be set in run.py)
    api_key = os.environ["ARTEMIS_API_KEY"]

    # If API key is not provided in request
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="X-API-Key header required"
        )

    # If API key doesn't match
    if x_api_key != api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key"
        )
