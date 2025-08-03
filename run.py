import os
import uvicorn
from artemis.config import settings

if __name__ == "__main__":
    # Note: ARTEMIS_API_KEY is checked at request time in auth.py
    print("🚀 Starting Artemis API server...")

    uvicorn.run(
        "artemis.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
