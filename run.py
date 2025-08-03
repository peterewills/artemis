import os
import sys
import uvicorn

if __name__ == "__main__":
    # Require ARTEMIS_API_KEY to be set
    if not os.getenv("ARTEMIS_API_KEY"):
        print("❌ Error: ARTEMIS_API_KEY environment variable is required but not set.")
        print("Please set ARTEMIS_API_KEY before running the application.")
        sys.exit(1)
    
    print(f"🔑 Using ARTEMIS_API_KEY from environment")
    
    from artemis.config import settings

    uvicorn.run(
        "artemis.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
