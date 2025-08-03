import os
import sys
import uvicorn

if __name__ == "__main__":
    # Check for required ARTEMIS_API_KEY at startup
    if not os.getenv("ARTEMIS_API_KEY"):
        print("❌ Error: ARTEMIS_API_KEY environment variable is required but not set.")
        print("Please set ARTEMIS_API_KEY before running the application.")
        sys.exit(1)
    
    print("🚀 Starting Artemis API server...")
    
    from artemis.config import settings

    uvicorn.run(
        "artemis.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
