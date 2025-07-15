import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Set up logging early
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

from artemis.api.routes import chat
from artemis.config import settings

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Artemis Personal Chatbot",
    description="A personal AI assistant powered by Claude",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://peterewills.github.io",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to Artemis Personal Chatbot"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
