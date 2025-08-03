import os
import uvicorn
from artemis.config import settings

if __name__ == "__main__":
    # Note: ARTEMIS_API_KEY is checked at request time in auth.py
    print("🚀 Starting Artemis API server...")
    
    # Debug: Log environment info
    print("🔍 Environment check at startup:")
    print(f"  - ARTEMIS_API_KEY: {'set' if os.getenv('ARTEMIS_API_KEY') else 'NOT SET'}")
    print(f"  - PORT: {os.getenv('PORT', 'not set')}")
    print(f"  - RAILWAY_ENVIRONMENT: {os.getenv('RAILWAY_ENVIRONMENT', 'not set')}")
    
    # Log all env vars that might be relevant (without exposing values)
    relevant_vars = [k for k in os.environ.keys() if 'RAILWAY' in k or 'ARTEMIS' in k or k == 'PORT']
    if relevant_vars:
        print(f"  - Found environment variables: {', '.join(relevant_vars)}")

    uvicorn.run(
        "artemis.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
