import os
import uvicorn
from artemis.config import settings

if __name__ == "__main__":
    # Set default API key if not already set
    if not os.getenv("API_KEY"):
        os.environ["API_KEY"] = "test-key-123"
        print("🔑 Using default API key: test-key-123")

    uvicorn.run(
        "artemis.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
