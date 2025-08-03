import os
import uvicorn
from artemis.config import settings

if __name__ == "__main__":
    # Set API key if not already set
    if not os.getenv("API_KEY"):
        # Check for REACT_APP_ARTEMIS_API_KEY first, fallback to test-key-123
        api_key = os.getenv("REACT_APP_ARTEMIS_API_KEY", "test-key-123")
        os.environ["API_KEY"] = api_key
        if api_key == "test-key-123":
            print("🔑 Using default API key: test-key-123")
        else:
            print("🔑 Using API key from REACT_APP_ARTEMIS_API_KEY environment variable")
    else:
        print("🔑 Using API key from API_KEY environment variable")

    uvicorn.run(
        "artemis.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
