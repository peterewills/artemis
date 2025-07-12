import uvicorn
from artemis.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "artemis.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )